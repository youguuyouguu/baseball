import { useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { deleteScheduleDetail, updateScheduleDetail } from '../../api';
import BottomNavigation from '../../components/common/bottom_navigation';

function formatTime(value) {
  if (!value) return '--:--';
  if (/^\d{2}:\d{2}(:\d{2})?$/.test(value)) return value.slice(0, 5);
  return new Intl.DateTimeFormat('ko-KR', { hour: '2-digit', minute: '2-digit' }).format(new Date(value));
}

function toDbTime(time) {
  const timePart = String(time).split('T').pop().slice(0, 8);
  return timePart.length === 5 ? `${timePart}:00` : timePart;
}

function toInputTime(value) {
  if (!value) return '';
  if (/^\d{2}:\d{2}/.test(value)) return value.slice(0, 5);
  const date = new Date(value);
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
}

function minutesBetween(start, end) {
  if (!start || !end) return 60;
  if (/^\d{2}:\d{2}/.test(start) && /^\d{2}:\d{2}/.test(end)) {
    const toMinutes = (value) => Number(value.slice(0, 2)) * 60 + Number(value.slice(3, 5));
    return Math.max(30, toMinutes(end) - toMinutes(start));
  }
  return Math.max(30, Math.round((new Date(end) - new Date(start)) / 60000));
}

function overlaps(candidate, details, currentId) {
  const toMinutes = (value) => {
    if (/^\d{2}:\d{2}/.test(value)) return Number(value.slice(0, 2)) * 60 + Number(value.slice(3, 5));
    return new Date(value).getHours() * 60 + new Date(value).getMinutes();
  };
  return details.some((detail) => {
    if (detail.detail_id === currentId || !detail.start_at || !detail.end_at) return false;
    return toMinutes(candidate.start_at) < toMinutes(detail.end_at)
      && toMinutes(candidate.end_at) > toMinutes(detail.start_at);
  });
}

function RealTimeSchedule() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const [details, setDetails] = useState(state?.details || []);
  const [editing, setEditing] = useState(null);
  const [message, setMessage] = useState('');
  const generatedItems = state?.generatedSchedule?.items || [];

  const timelineItems = useMemo(() => details.map((detail) => ({ ...detail, title: detail.custom_name || '세부 일정' })), [details]);
  const fallbackItems = generatedItems.filter((item) => item.type === 'place').map((item) => ({
    title: item.name || item.location?.name || '세부 일정',
    start_at: toDbTime(item.arrival_time),
    end_at: toDbTime(item.departure_time),
  }));
  const items = timelineItems.length > 0 ? timelineItems : fallbackItems;

  const openEdit = (detail) => {
    setMessage('');
    setEditing({ ...detail, startTime: toInputTime(detail.start_at), endTime: toInputTime(detail.end_at) });
  };

  const saveEdit = async () => {
    const start = new Date(editing.start_at);
    const end = new Date(editing.end_at);
    const [startHour, startMinute] = editing.startTime.split(':').map(Number);
    const [endHour, endMinute] = editing.endTime.split(':').map(Number);
    start.setHours(startHour, startMinute, 0, 0);
    end.setHours(endHour, endMinute, 0, 0);
    if (start >= end) {
      setMessage('종료 시간은 시작 시간보다 늦어야 합니다.');
      return;
    }
    const candidate = { start_at: toDbTime(editing.startTime), end_at: toDbTime(editing.endTime) };
    if (overlaps(candidate, details, editing.detail_id)) {
      setMessage('다른 세부 일정과 시간이 겹칩니다.');
      return;
    }
    try {
      const updated = await updateScheduleDetail(editing.detail_id, candidate);
      setDetails((current) => current.map((detail) => detail.detail_id === editing.detail_id ? updated : detail));
      setEditing(null);
      setMessage('세부 일정이 수정되었습니다.');
    } catch (error) {
      setMessage(error.message);
    }
  };

  const removeDetail = async (detailId) => {
    try {
      await deleteScheduleDetail(detailId);
      setDetails((current) => current.filter((detail) => detail.detail_id !== detailId));
      setMessage('세부 일정이 삭제되었습니다.');
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <main className="app-screen">
      <header className="screen-header">
        <button className="button-ghost timeline-back" type="button" onClick={() => navigate(-1)}>뒤로</button>
        <h1 className="screen-title">실시간 일정표</h1>
        <p className="muted">시간 순서에 따른 방문 일정</p>
      </header>
      <section className="section" aria-labelledby="itinerary-title">
        <h2 className="section-title" id="itinerary-title">현재 일정</h2>
        {message && <p className="alert" role="alert">{message}</p>}
        <div className="timeline-scroll">
          <div className="timeline">
            {items.map((item, index) => {
              const duration = minutesBetween(item.start_at, item.end_at);
              return (
                <article className="timeline-row" key={item.detail_id || `${item.title}-${index}`}>
                  <time className="timeline-time">{formatTime(item.start_at)}</time>
                  <div className="timeline-rail" aria-hidden="true"><span /></div>
                  <div className="timeline-card" style={{ minHeight: `${Math.min(260, Math.max(108, duration * 2))}px` }}>
                    <h3>{item.title}</h3>
                    <p>{formatTime(item.start_at)} - {formatTime(item.end_at)}</p>
                    {item.detail_id && <div className="timeline-actions">
                      <button className="detail-edit-button" type="button" onClick={() => openEdit(item)}>수정</button>
                      <button className="detail-delete-button" type="button" onClick={() => removeDetail(item.detail_id)}>삭제</button>
                    </div>}
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      </section>
      {editing && <div className="dialog-backdrop" role="presentation">
        <form className="edit-dialog" onSubmit={(event) => { event.preventDefault(); saveEdit(); }}>
          <h2>시간 수정</h2>
          <label className="form-label" htmlFor="detail-start-time">시작 시간</label>
          <input className="form-input" id="detail-start-time" type="time" value={editing.startTime} onChange={(event) => setEditing({ ...editing, startTime: event.target.value })} />
          <label className="form-label" htmlFor="detail-end-time">종료 시간</label>
          <input className="form-input" id="detail-end-time" type="time" value={editing.endTime} onChange={(event) => setEditing({ ...editing, endTime: event.target.value })} />
          <div className="dialog-actions">
            <button className="button-ghost" type="button" onClick={() => setEditing(null)}>취소</button>
            <button className="button-primary" type="submit">저장</button>
          </div>
        </form>
      </div>}
      <BottomNavigation />
    </main>
  );
}

export default RealTimeSchedule;