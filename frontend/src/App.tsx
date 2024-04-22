import { BrowserRouter, Routes, Route } from 'react-router-dom';

import ScrollToTop from './components/config/ScrollToTop';
import Header from './components/Header'
import Home from './components/Home'
import Heroes from './components/hero/Heroes';
import Hero from './components/hero/Hero';
import Teams from './components/team/Teams';
import Team from './components/team/Team';
import Players from './components/player/Players';
import Player from './components/player/Player';
import Matches from './components/match/Matches';
import Match from './components/match/Match';
import Admin from './components/admin/Admin';
import Logs from './components/dashboard/Logs';
import PageNotFound from './components/error/PageNotFound';
import useTokenExpiration from './components/hook/AuthHook';
import ProtectedRoute from './components/route/AuthRoute';
import './App.css'

function App() {
  useTokenExpiration();
  return (
    <BrowserRouter>
      <ScrollToTop />
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/heroes" element={<Heroes />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/players" element={<Players />} />
          <Route path="/matches" element={<Matches />} />
          <Route path="/logs" element={<ProtectedRoute outlet={<Logs />} />} />
          <Route path='/matches/:id' element={<Match />} />
          <Route path='/players/:id' element={<Player />} />
          <Route path='/teams/:id' element={<Team />} />
          <Route path='/heroes/:id' element={<Hero />} />
          <Route path='*' element={<PageNotFound />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
