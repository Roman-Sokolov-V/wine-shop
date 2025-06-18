import { createSlice } from '@reduxjs/toolkit';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';
import { ApiPet, Pet } from '../types/Pet';
import { Filters } from '../types/Filters';
import { searchPets } from '../utils/helperPet';

type Initial = {
  favorites: number[];
};
const initialValue: Initial = {
  favorites: [],
};

const FavoritesSlice = createSlice({
  name: 'favorite',
  initialState: initialValue,
  reducers: {
    init: state => {
      const curLocalVals = accessLocalStorage.get(LocalAccessKeys.FAVORITES);
      if (curLocalVals) {
        try {
          state.favorites = JSON.parse(curLocalVals);
        } catch (error) {
          console.error('Error Occured ', error);
          state.favorites = [];
        }
      } else {
        accessLocalStorage.set(LocalAccessKeys.FAVORITES, JSON.stringify([]));
      }
    },

    toggle: (state, action: { payload: number }) => {
      if (state.favorites.includes(action.payload)) {
        state.favorites = state.favorites.filter(itm => itm !== action.payload);
        accessLocalStorage.set(
          LocalAccessKeys.FAVORITES,
          JSON.stringify(state.favorites),
        );
      } else {
        state.favorites.push(action.payload);
        accessLocalStorage.set(
          LocalAccessKeys.FAVORITES,
          JSON.stringify(state.favorites),
        );
      }
    },

    clear: state => {
      state.favorites = [];
      accessLocalStorage.clearKey(LocalAccessKeys.FAVORITES);
    },
  },
});

export default FavoritesSlice.reducer;
export const { actions } = FavoritesSlice;
