import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();
  const handleLogin = () => {
    navigate('/main', { replace: true });
  };

  return (
    <main>
      <h1>로그인</h1>
      <button type="button" onClick={handleLogin}>로그인</button>
    </main>
  );
}

export default Login