import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_PET_API_BASE_URL,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export default api;
