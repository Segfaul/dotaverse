import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header'
import Home from './components/Home'
import './App.css'

function App() {

  return (
    <BrowserRouter>
      <Header />
      <main>
        <Routes>
            <Route path="/" element={<Home />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
