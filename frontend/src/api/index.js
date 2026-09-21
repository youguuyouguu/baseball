const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export async function createUser(user) {
	const response = await fetch(`${API_BASE_URL}/users/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(user),
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '회원가입에 실패했습니다.');
	}

	return response.json();
}

export async function getUser(userId) {
	const response = await fetch(`${API_BASE_URL}/users/${userId}`);

	if (!response.ok) {
		throw new Error('아이디가 일치하지 않습니다.');
	}

	return response.json();
}

export async function generateSchedule(requestBody) {
	const response = await fetch(`${API_BASE_URL}/schedules/generate`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(requestBody),
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '일정 생성에 실패했습니다.');
	}

	return response.json();
}

export async function createTour(tour) {
	const response = await fetch(`${API_BASE_URL}/tours/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(tour),
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '일정 저장에 실패했습니다.');
	}

	return response.json();
}

export async function getToursByUser(UserId) {
	const response = await fetch(`${API_BASE_URL}/tours/user/${UserId}`);
	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '일정 목록을 불러오지 못했습니다.');
	}
	return response.json();
}

export async function createScheduleDetail(detail) {
	const response = await fetch(`${API_BASE_URL}/schedule-details/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(detail),
	});
	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '세부 일정 저장에 실패했습니다.');
	}
	return response.json();
}

export async function updateScheduleDetail(detailId, detail) {
	const response = await fetch(`${API_BASE_URL}/schedule-details/${detailId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(detail),
	});
	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '세부 일정 수정에 실패했습니다.');
	}
	return response.json();
}

export async function deleteScheduleDetail(detailId) {
	const response = await fetch(`${API_BASE_URL}/schedule-details/${detailId}`, { method: 'DELETE' });
	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '세부 일정 삭제에 실패했습니다.');
	}
	return response.json();
}

export async function getUpcomingLeagues() {
	const response = await fetch(`${API_BASE_URL}/leagues/upcoming`);

	if (!response.ok) {
		const error = await response.json().catch(() => ({}));
		throw new Error(error.detail || '경기 일정을 불러오지 못했습니다.');
	}

	const result = await response.json();
	return result.data || [];
}