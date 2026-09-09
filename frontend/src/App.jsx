import { Navigate, Route, Routes } from 'react-router-dom';
import MyPage from './pages/account/mypage';
import Login from './pages/auth/login';
import Home from './pages/home/main';
import AllSchedule from './pages/schedule/all_schedule';
import AddSchedule from './pages/schedule/add_schedule';
import AddTouristSpot from './pages/schedule/add_tourist_spot';
import RealTimeSchedule from './pages/schedule/realtime_schedule';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/main" element={<Home />} />
      <Route path="/schedule/all" element={<AllSchedule />} />
      <Route path="/schedule/add" element={<AddSchedule />} />
      <Route path="/schedule/add/tourist" element={<AddTouristSpot />} />
      <Route path="/schedule/realtime" element={<RealTimeSchedule />} />
      <Route path="/mypage" element={<MyPage />} />
    </Routes>
  );
}