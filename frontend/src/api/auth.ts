import { AxiosResponse } from 'axios';
import api from './api';

export const getUser = (): Promise<AxiosResponse> => {
  return api.get(`api/v1/users/`, {
    headers: {
      Authorization: '',
    },
  });
};

export const login = (email: string, password: string) => {
  return api.post(`api/v1/users/login/`, { email, password });
};

export const register = (
  email: string,
  password: string,
  first_name: string,
  last_name: string,
) => {
  return api.post(`api/v1/users/register/`, {
    email,
    password,
    first_name,
    last_name,
  });
};
