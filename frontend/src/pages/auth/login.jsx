import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getUser } from '../../api';

function Login() {
  const navigate = useNavigate();
  const { state } = useLocation();
  const [userId, setUserId] = useState('');
  const [email, setEmail] = useState('');
  const [nickname, setNickname] = useState('');
  const [message, setMessage] = useState(state?.message || '');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleLogin = async (event) => {
    event.preventDefault();
    if (!userId.trim() || !email.trim() || !nickname.trim()) {
      setMessage('사용자 ID, 이메일과 닉네임을 입력해 주세요.');
      return;
    }

    setIsSubmitting(true);
    setMessage('');
    try {
      const user = await getUser(Number(userId));
      if (user.email !== email.trim() || user.nickname !== nickname.trim()) {
        throw new Error('로그인 정보가 일치하지 않습니다.');
      }
      localStorage.setItem('user', JSON.stringify(user));
      navigate('/main', { replace: true, state: { user } });
    } catch (error) {
      setMessage(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="app-screen auth-screen">
      <header className="screen-header">
        <h1 className="screen-title">로그인</h1>
        <p className="muted">등록한 사용자 정보를 입력해 주세요.</p>
      </header>
      <form className="form-stack" onSubmit={handleLogin}>
        <label htmlFor="login-user-id">사용자 ID</label>
        <input id="login-user-id" type="number" min="1" value={userId} onChange={(event) => setUserId(event.target.value)} required />
        <label htmlFor="login-email">이메일</label>
        <input id="login-email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        <label htmlFor="login-nickname">닉네임</label>
        <input id="login-nickname" value={nickname} onChange={(event) => setNickname(event.target.value)} required />
        {message && <p role="alert">{message}</p>}
        <button className="button-primary button-full" type="submit" disabled={isSubmitting}>{isSubmitting ? '조회 중...' : '로그인'}</button>
      </form>
      <button className="button-secondary button-full auth-signup-button" type="button" onClick={() => navigate('/signup')}>
        회원가입
      </button>
    </main>
  );
}

export default Login