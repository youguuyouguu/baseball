const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

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