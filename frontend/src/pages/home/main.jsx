import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHello } from '../../api';
import BottomNavigation from '../../components/common/bottom_navigation';

const games = [
  { label: '오늘 | 사직', home: 'SSG', away: '롯데' },
  { label: '내일 | 사직', home: 'SSG', away: '롯데' },
];

function Home() {
  const navigate = useNavigate();
  const [selectedGame, setSelectedGame] = useState(null);
  const [apiMessage, setApiMessage] = useState('');

  const callBackend = async () => {
    try {
      const data = await getHello();
      setApiMessage(data.message);
    } catch (error) {
      setApiMessage(error.message);
    }
  };

  return (
    <main className="app-screen">
      <header className="screen-header">
        <h1 className="screen-title">메인 화면</h1>
      </header>

      <section className="section" aria-labelledby="upcoming-title">
        <h2 className="section-title" id="upcoming-title">다가오는 일정</h2>
        <div className="empty-card">
          <p className="muted">현재 진행 중인 여행이 없습니다.</p>
        </div>
      </section>

      <section className="section" aria-labelledby="games-title">
        <h2 className="section-title" id="games-title">KBO 경기 일정</h2>
        <div className="game-list">
          {games.map((game) => {
            const isSelected = selectedGame === game.label;

            return (
            <article
              className={`game-card${isSelected ? ' is-selected' : ''}`}
              key={game.label}
              onClick={() => setSelectedGame(game.label)}
            >
              <h3>{game.label}</h3>
              <p>{game.home} vs {game.away}</p>
              {isSelected && (
                <button className="button-primary button-full" type="button" onClick={() => navigate('/schedule/add')}>
                  일정표 생성
                </button>
              )}
            </article>
            );
          })}
        </div>
      </section>

      <section className="section" aria-labelledby="api-example-title">
        <h2 className="section-title" id="api-example-title">백엔드 API 예제</h2>
        <button className="button-primary" type="button" onClick={callBackend}>
          API 호출
        </button>
        {apiMessage && <p className="muted">{apiMessage}</p>}
      </section>

      <BottomNavigation />
    </main>
  );
}

export default Home;
