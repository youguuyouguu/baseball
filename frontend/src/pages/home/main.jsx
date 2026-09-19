import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import BottomNavigation from '../../components/common/bottom_navigation';
import { getUpcomingLeagues } from '../../api';

function formatMonth(monthKey) {
  const [year, month] = monthKey.split('-');
  return `${year}년 ${Number(month)}월`;
}

function formatDate(gameDate) {
  const date = new Date(`${gameDate}T00:00:00`);
  return new Intl.DateTimeFormat('ko-KR', {
    month: 'long',
    day: 'numeric',
    weekday: 'short',
  }).format(date);
}

function Home() {
  const navigate = useNavigate();
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [monthIndex, setMonthIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;

    getUpcomingLeagues()
      .then((result) => {
        if (isMounted) setGames(result);
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
  }, []);

  const gamesByMonth = useMemo(() => {
    const grouped = games.reduce((months, game) => {
      const monthKey = game.game_date.slice(0, 7);
      if (!months[monthKey]) months[monthKey] = [];
      months[monthKey].push(game);
      return months;
    }, {});

    return Object.entries(grouped).sort(([left], [right]) => left.localeCompare(right));
  }, [games]);

  const currentMonth = gamesByMonth[monthIndex];
  const currentMonthGames = currentMonth ? currentMonth[1] : [];

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
        {gamesByMonth.length > 0 && (
          <div className="month-navigation" aria-label="경기 일정 월 선택">
            <button
              className="button-ghost"
              type="button"
              disabled={monthIndex === 0}
              onClick={() => setMonthIndex((index) => index - 1)}
            >
              이전 달
            </button>
            <strong>{formatMonth(currentMonth[0])}</strong>
            <button
              className="button-ghost"
              type="button"
              disabled={monthIndex === gamesByMonth.length - 1}
              onClick={() => setMonthIndex((index) => index + 1)}
            >
              다음 달
            </button>
          </div>
        )}

        {isLoading && <p className="muted">경기 일정을 불러오는 중입니다.</p>}
        {!isLoading && error && <p className="alert">{error}</p>}
        {!isLoading && !error && gamesByMonth.length === 0 && (
          <div className="empty-card">
            <p className="muted">예정된 정규 시즌 경기가 없습니다.</p>
          </div>
        )}
        <div className="game-list">
          {currentMonthGames.map((game) => {
            const isSelected = selectedGame === game.League_id;

            return (
            <article
              className={`game-card${isSelected ? ' is-selected' : ''}`}
              key={game.League_id}
              onClick={() => setSelectedGame(game.League_id)}
            >
              <h3>{formatDate(game.game_date)}</h3>
              <p>{game.game_time}</p>
              <p>{game.game_name}</p>
              <p>{game.stadium_name}</p>
              {isSelected && (
                <button className="button-primary button-full" type="button" onClick={() => navigate('/schedule/add', { state: { game } })}>
                  일정표 생성
                </button>
              )}
            </article>
            );
          })}
        </div>
      </section>

      <BottomNavigation />
    </main>
  );
}

export default Home;