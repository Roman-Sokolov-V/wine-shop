import { AxiosResponse } from 'axios';
import api from './api';

export const subscribeApi = (email: string): Promise<AxiosResponse> => {
  //TODO: check API endpoint from Backend when implemented
  return api.post(`api/v1/user/subscribe`, { email });
};
