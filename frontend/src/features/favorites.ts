import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';
import { deletPetFavorite, setPetFavorite } from '../api/pets';

type Initial = {
  favorites: number[];
  loading: boolean;
  error: string;
};

const initialValue: Initial = {
  favorites: [],
  loading: false,
  error: '',
};

const toggle = createAsyncThunk<
  // This thunk doesn't need to return anything on success
  void,
  number,
  {
    state: { favorite: Initial };
    rejectValue: string;
  }
>('favorite/toggle', async (petId, { getState, rejectWithValue }) => {
  try {
    const state = getState();
    const { favorites: currentFavorites } = state.favorite;
    const isFavorite = currentFavorites.includes(petId);

    currentFavorites.forEach(async id => {
      await setPetFavorite(id);
    });

    await (!isFavorite ? deletPetFavorite(petId) : setPetFavorite(petId));
  } catch (err: unknown) {
    const errorMessage = 'API to toggle favorites call failed.';
    return rejectWithValue(errorMessage);
  }
});

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
    init: state => {
      const localFavs = accessLocalStorage.get(LocalAccessKeys.FAVORITES);
      console.log('ppp', Array.isArray(localFavs));
      if (localFavs && Array.isArray(localFavs)) {
        state.favorites = localFavs;
      } else {
        accessLocalStorage.set(LocalAccessKeys.FAVORITES, []);
        state.favorites = [];
      }
    },
  },

  extraReducers: builder => {
    builder
      .addCase(toggle.pending, (state, action) => {
        state.loading = true;
        const petId = action.meta.arg;
        const isFavorite = state.favorites.includes(petId);

        if (isFavorite) {
          // Remove from favorites
          state.favorites = state.favorites.filter(id => id !== petId);
        } else {
          // Add to favorites
          state.favorites.push(petId);
        }
        accessLocalStorage.set(LocalAccessKeys.FAVORITES, state.favorites);
      })
      .addCase(toggle.fulfilled, state => {
        state.loading = false;
      })
      .addCase(toggle.rejected, state => {
        state.loading = false;
      });
    builder
      // Handle the `clear` thunk states
      .addCase(clear.pending, state => {
        state.loading = true;
      })
      .addCase(clear.fulfilled, state => {
        state.loading = false;
        state.favorites = [];
        accessLocalStorage.clearKey(LocalAccessKeys.FAVORITES);
      })
      .addCase(clear.rejected, (state, action) => {
        state.loading = false;
        if (action.payload) {
          state.error = action.payload;
        }
      });
  },
});

export default FavoritesSlice.reducer;
export const { init } = FavoritesSlice.actions;
export { toggle, clear };
