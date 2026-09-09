import { useNavigate } from 'react-router-dom';
import BottomNavigation from '../../components/common/bottom_navigation';

const schedules = [
  { number: 1, title: 'nc VS 두산', date: '2026년 8월 26일' },
  { number: 2, title: '키움 VS SSG', date: '2026년 9월 11일' },
  { number: 3, title: 'KIA VS 롯데', date: '2026년 9월 17일' },
];


function AllSchedule() {
  const navigate = useNavigate();

  return (
    <main className="app-screen">
      <header className="screen-header">
        <h1 className="screen-title">모든 일정</h1>
      </header>
      <section className="schedule-list" aria-label="일정 목록">
        {schedules.map((schedule) => (
          <article className="schedule-card" key={schedule.number}>
            <strong className="schedule-number">{schedule.number}</strong>
            <div>
              <h2 className="section-title">{schedule.title}</h2>
              <p className="muted">{schedule.date}</p>
            </div>
          </article>
        ))}
      </section>
      <button className="button-primary button-full" type="button" onClick={() => navigate('/schedule/add')}>
        일정 추가하기
      </button>
      <BottomNavigation />
    </main>
  );
}

export default AllSchedule;