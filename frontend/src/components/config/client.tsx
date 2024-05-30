import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const backend_url = import.meta.env.VITE_BACKEND_URL;

const client = axios.create({
  baseURL: backend_url,
  withCredentials: true,
});

export default client;