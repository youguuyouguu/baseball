import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import BottomNavigation from '../../components/common/bottom_navigation';
import { getToursByUser } from '../../api';

function formatTime(value) {
  return value ? value.slice(0, 5) : '--:--';
}

function MyPage() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const [tours, setTours] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!user?.User_id) {
      setIsLoading(false);
      return undefined;
    }
    let isMounted = true;
    getToursByUser(user.User_id)
      .then((result) => {
        if (isMounted) setTours(result);
      })
      .catch((requestError) => {
        if (isMounted) setError(requestError.message);
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });
    return () => {
      isMounted = false;
    };
  }, [user?.User_id]);

  return (
    <main className="app-screen">
      <header className="screen-header">
        <h1 className="screen-title">마이페이지</h1>
        <p className="muted">{user?.nickname || '사용자'}님의 원정 일정</p>
      </header>
      <section className="section" aria-labelledby="profile-title">
        <h2 className="section-title" id="profile-title">내 정보</h2>
        <div className="profile-card">
          <strong>{user?.nickname || '사용자'}</strong>
          <p>{user?.email || '로그인 정보를 찾을 수 없습니다.'}</p>
        </div>
      </section>
      <section className="section" aria-labelledby="tour-title">
        <div className="section-heading-row">
          <h2 className="section-title" id="tour-title">내 일정</h2>
          <span className="muted">{tours.length}개</span>
        </div>
        {isLoading && <p className="muted">일정을 불러오는 중입니다.</p>}
        {!isLoading && error && <p className="alert">{error}</p>}
        {!isLoading && !error && tours.length === 0 && <div className="empty-card"><p className="muted">생성한 일정이 없습니다.</p></div>}
        <div className="tour-list">
          {tours.map((tour) => (
            <article className="tour-card" key={tour.schedule_id}>
              <div>
                <span className="tour-status">경기 원정</span>
                <h3>일정 #{tour.schedule_id}</h3>
                <p>{formatTime(tour.starting_time)} - {formatTime(tour.end_time)}</p>
                <p>참여 인원 {tour.people_num}명</p>
              </div>
              <button className="button-secondary" type="button" onClick={() => navigate('/schedule/realtime', { state: { tour } })}>보기</button>
            </article>
          ))}
        </div>
      </section>
      <BottomNavigation />
    </main>
  );
}

export default MyPage;