import React from 'react'
import ReactDOM from 'react-dom/client'
import ReactGA from 'react-ga4'
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

// Initialize Google Analytics with environment variable
const trackingId = import.meta.env.VITE_APP_GA_KEY;
console.log(trackingId);
if (trackingId) {
  ReactGA.initialize(trackingId);
  ReactGA.send({ hitType: "pageview", page: window.location.href, title: "init page" });
}
