import { useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { createScheduleDetail, createTour, generateSchedule } from '../../api';
import { loadKakao, searchKakaoPlaces, STADIUM } from '../../lib/kakao';

const DEFAULT_STADIUM = { id: 'stadium', name: '사직야구장', address: '부산광역시 동래구' };
const DEFAULT_RETURN_STATION = { id: 'busan-station', name: '부산역', address: '부산광역시 동구' };
const categories = ['전체', '관광', '식당', '숙소', '카페'];

function toDateTime(date, time) {
  return `${date}T${time}:00`;
}

function toDbTime(time) {
  const timePart = String(time).split('T').pop().slice(0, 8);
  return timePart.length === 5 ? `${timePart}:00` : timePart;
}

function createDetailPayload(scheduleId, item) {
  return {
    schedule_id: scheduleId,
    custom_name: item.name || item.location?.name || item.type,
    start_at: toDbTime(item.arrival_time),
    end_at: toDbTime(item.departure_time || item.arrival_time),
    state: '대기',
  };
}

function buildTravelTimes(schedule, game, selectedPlaces) {
  const stadiumId = game?.League_id || DEFAULT_STADIUM.id;
  const ids = ['departure', stadiumId, DEFAULT_RETURN_STATION.id, ...selectedPlaces.map((place) => place.id)];
  return Object.fromEntries(ids.map((source) => [
    source,
    Object.fromEntries(ids.filter((target) => target !== source).map((target) => [target, source === target ? 0 : 20])),
  ]));
}

function buildScheduleRequest(schedule, game, selectedPlaces) {
  const location = (id, name, address) => ({ id, name, address });
  const date = schedule.startDate;
  const gameDate = game?.game_date || date;
  const gameTime = game?.game_time?.slice(0, 5) || '18:30';
  const stadiumName = game?.stadium_name || DEFAULT_STADIUM.name;
  const stadiumAddress = game?.stadium_address || DEFAULT_STADIUM.address;

  return {
    participant_count: Number(schedule.people),
    game: {
      stadium: { id: String(game?.League_id) || DEFAULT_STADIUM.id, name: stadiumName, address: stadiumAddress },
      start_time: toDateTime(gameDate, gameTime),
    },
    start_point: {
      location: location('departure', schedule.departure, schedule.address || schedule.departure),
      arrival_time: toDateTime(date, schedule.arrivalTime),
    }, 
    end_point: {
      return_transport: {
        location: DEFAULT_RETURN_STATION,
        departure_time: toDateTime(schedule.endDate, schedule.returnTime),
      },
    },
    places: selectedPlaces.map((place) => ({
      id: place.id,
      name: place.name,
      location: location(place.id, place.name, place.address),
      address: place.address,
      category: place.category,
      visit_minutes: place.visit_minutes,
      opening_time: place.opening_time,
      closing_time: place.closing_time,
    })),
    travel_times: buildTravelTimes(schedule, game, selectedPlaces),
    congestion_cache: {},
  };
}

function AddTouristSpot() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const mapNode = useRef(null);
  const mapObj = useRef(null);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('전체');
  const [view, setView] = useState('list');
  const [places, setPlaces] = useState([]);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [addedPlaces, setAddedPlaces] = useState([]);
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      searchKakaoPlaces(query, category)
        .then((results) => {
          setPlaces(results);
          setSelectedPlace(null);
          setMessage('');
        })
        .catch((error) => {
          setPlaces([]);
          setMessage(error.message);
        });
    }, 300);

    return () => clearTimeout(timer);
  }, [query, category]);

  useEffect(() => {
    if (view !== 'map') return undefined;

    let cancelled = false;

    loadKakao()
      .then((kakao) => {
        if (cancelled || !mapNode.current) return;

        const map = new kakao.maps.Map(mapNode.current, {
          center: new kakao.maps.LatLng(STADIUM.lat, STADIUM.lng),
          level: 5,
        });
        mapObj.current = map;

        places.forEach((place) => {
          const marker = new kakao.maps.Marker({
            map,
            position: new kakao.maps.LatLng(place.lat, place.lng),
          });
          kakao.maps.event.addListener(marker, 'click', () => setSelectedPlace(place));
        });
      })
      .catch((error) => setMessage(error.message));

    return () => {
      cancelled = true;
      mapObj.current = null;
    };
  }, [view, places]);

  const togglePlace = (place) => {
    setAddedPlaces((current) => (
      current.some((item) => item.id === place.id)
        ? current.filter((item) => item.id !== place.id)
        : [...current, place]
    ));
  };

  const isAdded = (place) => addedPlaces.some((item) => item.id === place.id);

  const moveToStadium = () => {
    if (!mapObj.current || !window.kakao) return;
    mapObj.current.setCenter(new window.kakao.maps.LatLng(STADIUM.lat, STADIUM.lng));
    mapObj.current.setLevel(5);
  };

  const zoom = (amount) => {
    if (!mapObj.current) return;
    mapObj.current.setLevel(mapObj.current.getLevel() + amount);
  };

  const createSchedule = async () => {
    if (!state?.schedule || addedPlaces.length === 0) {
      setMessage('일정 정보와 방문할 장소를 선택해 주세요.');
      return;
    }

    setIsSubmitting(true);
    setMessage('일정을 계산하고 있습니다.');
    try {
      if (!state.game?.League_id) {
        throw new Error('관람할 경기를 먼저 선택해 주세요.');
      }

      const result = await generateSchedule(buildScheduleRequest(state.schedule, state.game, addedPlaces));
      const user = JSON.parse(localStorage.getItem('user') || 'null');
      if (!user?.User_id && !user?.user_id) {
        throw new Error('로그인한 사용자 정보를 찾을 수 없습니다.');
      }

      const tour = await createTour({
        User_id: user.User_id,
        League_id: state.game.League_id,
        starting_time: toDbTime(state.schedule.arrivalTime),
        end_time: toDbTime(state.schedule.returnTime),
        people_num: Number(state.schedule.people),
      });

      const scheduleId = tour.schedule_id ?? tour.Schdule_id;
      if (scheduleId == null) {
        console.log('Tour 생성 후 Schedule_id:', tour);
        throw new Error('생성된 일정의 schedule_id를 받지 못했습니다.');
      }
      const detailItems = result.items.filter((item) => item.type === 'place');
      const details = await Promise.all(
        detailItems.map((item) => createScheduleDetail(createDetailPayload(scheduleId, item))),
      );

      navigate('/schedule/all', { state: { schedule: state.schedule, game: state.game, places: addedPlaces, generatedSchedule: result, tour, details } });
    } catch (error) {
      setMessage(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="app-screen">
      <header className="screen-header">
        <h1 className="screen-title">관광지 추가 화면</h1>
        <p className="muted">일정에 추가할 장소를 검색하고 선택해 주세요.</p>
        {state?.game && <p className="muted">선택한 경기: {state.game.game_name} · {state.game.stadium_name}</p>}
      </header>

      <label className="form-label" htmlFor="place-search">장소 검색</label>
      <input
        className="search-input"
        id="place-search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="장소를 검색해 주세요 (예: 시장)"
      />

      <div className="tab-row" role="group" aria-label="화면 전환">
        <button className={`tab${view === 'list' ? ' is-active' : ''}`} type="button" onClick={() => setView('list')} aria-pressed={view === 'list'}>리스트</button>
        <button className={`tab${view === 'map' ? ' is-active' : ''}`} type="button" onClick={() => setView('map')} aria-pressed={view === 'map'}>지도</button>
      </div>

      <div className="filter-row" role="group" aria-label="장소 분류">
        {categories.map((item) => (
          <button
            className={`filter${category === item ? ' is-active' : ''}`}
            key={item}
            type="button"
            onClick={() => setCategory(item)}
            aria-pressed={category === item}
          >
            {item}
          </button>
        ))}
      </div>

      {view === 'list' ? (
        <section className="place-list" aria-label="장소 목록">
          {places.length === 0 && <p>검색 결과가 없습니다.</p>}
          {places.map((place) => (
            <article className="place-card" key={place.id}>
              <div>
                <h2>{place.name}</h2>
                <div className="tag-list">{place.tags.map((tag) => <span className="tag" key={tag}>#{tag}</span>)}</div>
                <p>{place.address}</p>
                <p>{place.distance}</p>
              </div>
              <button className={isAdded(place) ? 'button-secondary' : 'button-primary'} type="button" onClick={() => togglePlace(place)}>
                {isAdded(place) ? '취소' : '추가'}
              </button>
            </article>
          ))}
        </section>
      ) : (
        <section aria-label="장소 지도">
          <div className="map-panel">
            <div className="kakao-map" ref={mapNode} />
            <div className="map-controls">
              <button className="button-secondary" type="button" onClick={moveToStadium}>경기장 위치</button>
              <button className="button-secondary" type="button" onClick={() => zoom(-1)} aria-label="지도 확대">+</button>
              <button className="button-secondary" type="button" onClick={() => zoom(1)} aria-label="지도 축소">-</button>
            </div>
          </div>

          {selectedPlace && (
            <article className="detail-card">
              <div className="drag-bar" role="separator" aria-label="상세정보 카드 드래그 바" />
              <h2>{selectedPlace.name}</h2>
              <p>{selectedPlace.category} · {selectedPlace.address}</p>
              <p>{selectedPlace.distance}</p>
              <button className={isAdded(selectedPlace) ? 'button-secondary' : 'button-primary'} type="button" onClick={() => togglePlace(selectedPlace)}>
                {isAdded(selectedPlace) ? '취소' : '추가'}
              </button>
            </article>
          )}
        </section>
      )}

      {message && <p className="alert" role="alert">{message}</p>}
      <p>선택한 장소: {addedPlaces.length}곳</p>
      <button className="button-primary button-full" type="button" onClick={createSchedule} disabled={isSubmitting}>
        {isSubmitting ? '일정 생성 중...' : '일정 생성'}
      </button>
    </main>
  );
}

export default AddTouristSpot;
