/* eslint-disable no-param-reassign */
import { createSlice } from '@reduxjs/toolkit';
// import { AuthData } from '../types/AuthData';
// import { getAuthDataClient } from '../api/authCheck';
// import { getAccessLevel, getMaxCapibility } from '../utils/userManagmentHelper';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';
import { Pet } from '../types/Pet';
import { Filters } from '../types/Filters';
import { searchPets } from '../utils/helperPet';
import { SortOrder } from '../types/ViewControlle';

type Initial = {
  pets: Pet[];
  filteredPets: Pet[];
};
const initialValue: Initial = {
  pets: [],
  filteredPets: [],
};

const PetSlice = createSlice({
  name: 'pet',
  initialState: initialValue,
  reducers: {
    setPets: (state, action: { payload: Pet[] }) => {
      state.pets = action.payload;
      state.filteredPets = action.payload;
      accessLocalStorage.set(LocalAccessKeys.PETS, action.payload);
    },

    searchFilted(state, action: { payload: string }) {
      if (action.payload) {
        state.filteredPets = searchPets(state.pets, action.payload);
      }
    },

    sortFiltered(state, action: { payload: string }) {
      if (action.payload === 'acc') {
        state.filteredPets = state.filteredPets
          .slice()
          .toSorted((a, b) => a.name.localeCompare(b.name));
      } else if (action.payload === 'dec') {
        state.filteredPets = state.filteredPets
          .slice()
          .toSorted((a, b) => b.name.localeCompare(a.name));
      }
    },
  },
});

export default PetSlice.reducer;
export const { actions } = PetSlice;
