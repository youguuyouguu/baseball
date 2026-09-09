import { useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const places = [
  { id: 1, name: '부산 자갈치시장', category: '관광', tags: ['시장', '먹거리'], distance: '경기장까지 도보 10분', x: 26, y: 32 },
  { id: 2, name: '해운대원조할매국밥', category: '식당', tags: ['국밥', '맛집'], distance: '경기장까지 도보 5분', x: 68, y: 24 },
  { id: 3, name: '더베이101', category: '관광', tags: ['야경', '바다'], distance: '경기장까지 차량 12분', x: 48, y: 56 },
  { id: 4, name: '광안리 오션뷰 카페', category: '카페', tags: ['카페', '바다'], distance: '경기장까지 차량 15분', x: 78, y: 66 },
  { id: 5, name: '부산역 근처 숙소', category: '숙소', tags: ['숙소', '역세권'], distance: '경기장까지 차량 20분', x: 18, y: 72 },
];

const categories = ['전체', '관광', '식당', '숙소', '카페'];

function AddTouristSpot() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('전체');
  const [view, setView] = useState('list');
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [addedPlaces, setAddedPlaces] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [stadiumFocused, setStadiumFocused] = useState(false);

  const filteredPlaces = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    return places.filter((place) => {
      const matchesCategory = category === '전체' || place.category === category;
      const searchableText = [place.name, place.category, ...place.tags].join(' ').toLowerCase();
      return matchesCategory && (!normalizedQuery || searchableText.includes(normalizedQuery));
    });
  }, [category, query]);

  const togglePlace = (place) => {
    setAddedPlaces((current) => (
      current.some((item) => item.id === place.id)
        ? current.filter((item) => item.id !== place.id)
        : [...current, place]
    ));
  };

  const isAdded = (place) => addedPlaces.some((item) => item.id === place.id);

  return (
    <main className="app-screen">
      <header className="screen-header">
        <h1 className="screen-title">관광지 추가 화면</h1>
        <p className="muted">일정에 추가할 장소를 검색하고 선택해 주세요.</p>
        {state?.schedule && <p className="muted">선택한 경기: {state.schedule.match}</p>}
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
          {filteredPlaces.length === 0 && <p>검색 결과가 없습니다.</p>}
          {filteredPlaces.map((place) => (
            <article className="place-card" key={place.id}>
              <div className="place-image" aria-label={`${place.name} 이미지`}>사진</div>
              <div>
                <h2>{place.name}</h2>
                <div className="tag-list">{place.tags.map((tag) => <span className="tag" key={tag}>#{tag}</span>)}</div>
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
            <p>지도 영역</p>
            <div className="map-controls">
              <button className="button-secondary" type="button" onClick={() => setStadiumFocused(true)}>경기장 위치</button>
              <button className="button-secondary" type="button" onClick={() => setZoom((current) => Math.min(3, current + 1))} aria-label="지도 확대">+</button>
              <button className="button-secondary" type="button" onClick={() => setZoom((current) => Math.max(1, current - 1))} aria-label="지도 축소">-</button>
            </div>
            <p>확대 단계: {zoom}</p>
            {stadiumFocused && <p>경기장 위치를 중심으로 표시 중입니다.</p>}
            <div className="map-marker-list">
              {filteredPlaces.map((place) => (
                <button className={`map-marker${isAdded(place) ? ' is-added' : ''}`} key={place.id} type="button" onClick={() => setSelectedPlace(place)} aria-label={`${place.name} 마커`}>
                  {isAdded(place) ? '선택된 마커' : '마커'}: {place.name}
                </button>
              ))}
            </div>
          </div>

          {selectedPlace && (
            <article className="detail-card">
              <div className="drag-bar" role="separator" aria-label="상세정보 카드 드래그 바" />
              <h2>{selectedPlace.name}</h2>
              <p>{selectedPlace.category} · {selectedPlace.tags.join(', ')}</p>
              <p>{selectedPlace.distance}</p>
              <button className={isAdded(selectedPlace) ? 'button-secondary' : 'button-primary'} type="button" onClick={() => togglePlace(selectedPlace)}>
                {isAdded(selectedPlace) ? '취소' : '추가'}
              </button>
            </article>
          )}
        </section>
      )}

      <p>선택한 장소: {addedPlaces.length}곳</p>
      <button className="button-primary button-full" type="button" onClick={() => navigate('/schedule/all', { state: { schedule: state?.schedule, places: addedPlaces } })}>
        완료
      </button>
    </main>
  );
}

export default AddTouristSpot;