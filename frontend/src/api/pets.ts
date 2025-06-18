import { AxiosResponse } from 'axios';
import { Pet } from '../types/Pet';
import api from './api';

export const getPetsData = (): Promise<AxiosResponse> => {
  return api.get(`api/v1/pets/`);
};

export const getPetsFiler = (): Promise<Pet[]> => {
  return api.get(`api/v1/pets/`);
};
