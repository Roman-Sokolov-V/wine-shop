import { AxiosResponse } from 'axios';
import api from './api';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';

export const getUserData = (): Promise<AxiosResponse> => {
  return api.get(`api/v1/users/me`, {
    headers: {
      Authorization: `Token ${accessLocalStorage.get(LocalAccessKeys.LOGGEDIN)?.token}`,
    },
  });
};

export const getUserMe = (): Promise<AxiosResponse> => {
  return api.get(`api/v1/users/me`, {
    headers: {
      Authorization: `Token ${accessLocalStorage.get(LocalAccessKeys.LOGGEDIN)?.token}`,
    },
  });
};
