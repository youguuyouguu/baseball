export async function getHello() {
  const response = await fetch('/api/hello');

  if (!response.ok) {
    throw new Error('API 요청에 실패했습니다.');
  }

  return response.json();
}
