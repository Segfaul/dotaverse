import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header'
import Home from './components/Home'
import './App.css'

function App() {
  const menuItems = ['faq', 'hero', 'player'];

  return (
    <BrowserRouter>
      <div>
        <Header title="Dotaverse" menuItems={menuItems} />
        <main>
          <Routes>
              <Route path="/" element={<Home />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
