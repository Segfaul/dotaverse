import React from 'react'
import ReactDOM from 'react-dom/client'
import './components/plugin/i18n'
import App from './App.tsx'
import './index.css'
import './styles/style.css'
import './styles/media.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
