import { AxiosResponse } from 'axios';
import api from './api';

export const subscribeApi = (email: string): Promise<AxiosResponse> => {
  return api.post(`api/v1/user/subscribe`, { email });
};
