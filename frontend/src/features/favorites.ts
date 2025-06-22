import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';
import { ApiPet, Pet } from '../types/Pet';
import { Filters } from '../types/Filters';
import { searchPets } from '../utils/helperPet';
import api from '../api/api';
import { deletPetFavorite, setPetFavorite } from '../api/pets';

type Initial = {
  favorites: number[];
};

const initialValue: Initial = {
  favorites: [],
};

const toggle = createAsyncThunk(
  'favorite/toggle',
  async (petId: number, { getState }) => {
    // We can get the current state to see if the pet is already a favorite.
    const state = getState() as { favorites: Initial };
    const currentFavorites = state.favorites.favorites;
    const isFavorite = currentFavorites.includes(petId);

    let updatedFavoritesResponse;

    if (isFavorite) {
      updatedFavoritesResponse = await setPetFavorite(petId);
    } else {
      updatedFavoritesResponse = await deletPetFavorite(petId);
    }

    // Ensure you return the data property, which should be the number[]
    return updatedFavoritesResponse.data;
  },
);

const clear = createAsyncThunk('favorite/clear', async (_, { getState }) => {
  const state = getState() as { favorites: Initial };
  const favorites = state.favorites.favorites;
  await Promise.all(favorites.map(petId => deletPetFavorite(petId)));
  return [];
});

const FavoritesSlice = createSlice({
  name: 'favorite',
  initialState: initialValue,
  reducers: {
    init: (state, action: { payload: number[] }) => {
      state.favorites = action.payload;
      accessLocalStorage.set(
        LocalAccessKeys.FAVORITES,
        JSON.stringify(action.payload),
      );
    },
  },

  extraReducers: builder => {
    builder
      .addCase(toggle.fulfilled, (state, action: { payload: number[] }) => {
        state.favorites = action.payload;
        accessLocalStorage.set(
          LocalAccessKeys.FAVORITES,
          JSON.stringify(action.payload),
        );
      })
      .addCase(toggle.rejected, (state, action) => {
        console.error(action.error.message || 'Failed to toggle favorite.');
      });

    builder
      .addCase(clear.fulfilled, (state, action: { payload: number[] }) => {
        console.log('sssssssssss');
        state.favorites = action.payload;
        accessLocalStorage.clearKey(LocalAccessKeys.FAVORITES);
      })
      .addCase(clear.rejected, (state, action) => {
        console.error(action.error.message || 'Failed to clear favorite.');
      });
  },
});

export default FavoritesSlice.reducer;
export const { init } = FavoritesSlice.actions;
export { toggle, clear };
