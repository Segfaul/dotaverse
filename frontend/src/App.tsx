import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header'
import Home from './components/Home'
import PageNotFound from './components/error/PageNotFound';
import './App.css'

function App() {

  return (
    <BrowserRouter>
      <Header />
      <main>
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path='*' element={<PageNotFound />}/>
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
