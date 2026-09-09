import { useNavigate } from 'react-router-dom';

function BottomNavigation() {
  const navigate = useNavigate();

  return (
    <nav className="bottom-navigation" aria-label="주요 메뉴">
      <button type="button" onClick={() => navigate('/schedule/all')}>
        일정표 관리
      </button>
      <button type="button" onClick={() => navigate('/main')}>
        메인 페이지
      </button>
      <button type="button" onClick={() => navigate('/mypage')}>
        마이페이지
      </button>
    </nav>
  );
}

export default BottomNavigation;