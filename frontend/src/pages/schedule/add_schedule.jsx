import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const initialForm = {
	match: '',
	startDate: '',
	endDate: '',
	departure: '',
	address: '',
	people: 1,
};

function AddSchedule() {
	const navigate = useNavigate();
	const [form, setForm] = useState(initialForm);
	const [message, setMessage] = useState('');

	const updateField = (event) => {
		const { name, value } = event.target;
		setForm((current) => ({ ...current, [name]: value }));
		setMessage('');
	};

	const changePeople = (amount) => {
		setForm((current) => ({
			...current,
			people: Math.max(1, current.people + amount),
		}));
		setMessage('');
	};

	const handleSubmit = (event) => {
		event.preventDefault();

		if (!form.match || !form.startDate || !form.endDate || !form.departure) {
			setMessage('경기, 일정, 출발지를 모두 입력해 주세요.');
			return;
		}

		navigate('/schedule/add/tourist', { state: { schedule: form } });
	};

	return (
		<main className="app-screen">
			<header className="screen-header">
				<h1 className="screen-title">일정 생성 화면</h1>
				<h2 className="section-title">원정 일정 만들기</h2>
			</header>

			<form className="form-stack" onSubmit={handleSubmit}>
				<fieldset className="form-fieldset">
					<legend>경기 선택</legend>
					<label className="form-label" htmlFor="match">관람할 경기</label>
					<select className="form-select" id="match" name="match" value={form.match} onChange={updateField}>
						<option value="">경기를 선택해 주세요</option>
						<option value="home-match">홈 경기</option>
						<option value="away-match">원정 경기</option>
					</select>
				</fieldset>

				<fieldset className="form-fieldset">
					<legend>일정</legend>
					<div className="date-row">
						<label className="form-label" htmlFor="startDate">출발일
							<input className="form-input" id="startDate" name="startDate" type="date" value={form.startDate} onChange={updateField} />
						</label>
						<label className="form-label" htmlFor="endDate">귀가일
							<input className="form-input" id="endDate" name="endDate" type="date" value={form.endDate} onChange={updateField} />
						</label>
					</div>
				</fieldset>

				<fieldset className="form-fieldset">
					<legend>출발지</legend>
					<label className="form-label" htmlFor="departure">출발 지역</label>
					<input className="form-input" id="departure" name="departure" value={form.departure} onChange={updateField} placeholder="출발 지역을 입력해 주세요" />
					<label className="form-label" htmlFor="address">주소 검색</label>
					<input className="form-input" id="address" name="address" value={form.address} onChange={updateField} placeholder="주소 검색" />
				</fieldset>

				<fieldset className="form-fieldset">
					<legend>여행 인원</legend>
					<label className="form-label" htmlFor="people">동행 인원</label>
					<div className="stepper">
						<input className="form-input" id="people" name="people" value={`${form.people}명`} readOnly />
						<button className="stepper-button" type="button" onClick={() => changePeople(1)} aria-label="인원 늘리기">+</button>
						<button className="stepper-button" type="button" onClick={() => changePeople(-1)} aria-label="인원 줄이기">-</button>
					</div>
				</fieldset>

				{message && <p className="alert" role="alert">{message}</p>}
				<button className="button-primary button-full" type="submit">일정 생성</button>
			</form>
		</main>
	);
}

export default AddSchedule;
