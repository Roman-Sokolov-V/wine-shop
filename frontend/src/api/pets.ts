import { AxiosResponse } from 'axios';
import { Pet } from '../types/Pet';
import api from './api';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';

export const getPetsData = (): Promise<AxiosResponse> => {
  return api.get(`api/v1/pets/`);
};

export const getPetsFilter = (): Promise<Pet[]> => {
  return api.get(`api/v1/pets/`);
};

export const getPetById = (id: string): Promise<AxiosResponse> => {
  return api.get(`api/v1/pets/${id}`);
};

export const setPetFavorite = (petId: number) => {
  return api.post(`/api/v1/pets/favorite/${petId}/`, {
    headers: {
      Authorization: `Token ${accessLocalStorage.get(LocalAccessKeys.LOGGEDIN)?.token}`,
    },
  });
};

export const deletPetFavorite = (petId: number) => {
  //TODO: repalce api then readys
  return api.post(`/api/v1/pets/favorite/${petId}/xxx`, {
    headers: {
      Authorization: `Token ${accessLocalStorage.get(LocalAccessKeys.LOGGEDIN)?.token}`,
    },
  });
};
