const itinerary = [
  { title: '자갈치시장 방문', time: '17:00', detail: '50분 체류', type: 'current' },
  { title: '자갈치시장 → 경기장', time: '17:50', detail: '10분 이동', type: 'next' },
  { title: '롯데 VS 한화 경기', time: '18:00', detail: '18:20 경기 시작', type: 'event' },
  { title: '경기장 → 해운대원조할매국밥', time: '21:20', detail: '5분 이동', type: 'next' },
];

function RealTimeSchedule() {
  return (
    <main className="app-screen">
      <header className="screen-header">
        <h1 className="screen-title">실시간 일정표 화면</h1>
        <p className="muted">
          2026년 7월 22일 <time dateTime="2026-07-22T17:20">17:20</time>
        </p>
      </header>

      <section className="section" aria-labelledby="itinerary-title">
        <h2 className="section-title" id="itinerary-title">현재 일정</h2>
        <div>
          {itinerary.map((item) => (
            <article className="realtime-item" key={`${item.title}-${item.time}`} data-type={item.type}>
              <h3>{item.title}</h3>
              <div className="realtime-meta">
                <p>{item.detail}</p>
                <time dateTime={`2026-07-22T${item.time}`}>{item.time}</time>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default RealTimeSchedule;