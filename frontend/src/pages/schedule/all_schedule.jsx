import { useLocation, useNavigate } from 'react-router-dom';
import BottomNavigation from '../../components/common/bottom_navigation';

function AllSchedule() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const generatedItems = state?.generatedSchedule?.items || [];

  return (
    <main className="app-screen">
      <header className="screen-header">
        <h1 className="screen-title">모든 일정</h1>
        {state?.generatedSchedule && <p className="muted">새 일정이 생성되었습니다.</p>}
      </header>
      {generatedItems.length > 0 && (
        <section className="section" aria-label="생성된 일정">
          <h2 className="section-title">생성된 시간표</h2>
          <div className="schedule-list">
            {generatedItems.map((item, index) => (
              <article className="schedule-card" key={`${item.type}-${item.id || index}`}>
                <strong className="schedule-number">{index + 1}</strong>
                <div>
                  <h2 className="section-title">{item.name || item.location?.name || item.type}</h2>
                  <p className="muted">
                    {item.arrival_time ? new Date(item.arrival_time).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }) : ''}
                    {item.congestion_warning ? ' · 혼잡할 가능성 높음' : ''}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
      <button className="button-primary button-full" type="button" onClick={() => navigate('/schedule/add')}>
        일정 추가하기
      </button>
      <BottomNavigation />
    </main>
  );
}

export default AllSchedule;