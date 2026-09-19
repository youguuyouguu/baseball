import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createUser } from '../../api';

function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', nickname: '' });
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
    setMessage('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    try {
      await createUser({
        email: form.email.trim(),
        nickname: form.nickname.trim(),
      });
      navigate('/login', { replace: true, state: { message: '회원가입이 완료되었습니다. 로그인해 주세요.' } });
    } catch (error) {
      setMessage(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="app-screen auth-screen">
      <header className="screen-header">
        <h1 className="screen-title">회원가입</h1>
        <p className="muted">사용자 정보를 입력해 계정을 만들어 주세요.</p>
      </header>

      <form className="form-stack" onSubmit={handleSubmit}>
        <fieldset className="form-fieldset">
          <legend>계정 정보</legend>
          <label className="form-label" htmlFor="signup-email">이메일</label>
          <input className="form-input" id="signup-email" name="email" type="email" value={form.email} onChange={updateField} required />
          <label className="form-label" htmlFor="signup-nickname">닉네임</label>
          <input className="form-input" id="signup-nickname" name="nickname" value={form.nickname} onChange={updateField} required />
        </fieldset>

        {message && <p className="alert" role="alert">{message}</p>}
        <button className="button-primary button-full" type="submit" disabled={isSubmitting}>
          {isSubmitting ? '가입 중...' : '회원가입'}
        </button>
      </form>
      <button className="button-ghost button-full" type="button" onClick={() => navigate('/login')}>
        로그인으로 돌아가기
      </button>
    </main>
  );
}

export default Signup;