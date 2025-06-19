import { createSlice } from '@reduxjs/toolkit';
import { accessLocalStorage } from '../utils/accessLocalStorage';
import { LocalAccessKeys } from '../types/LocalAccessKeys';

const initialValue = {
  loggedIn: accessLocalStorage.get(LocalAccessKeys.LOGGEDIN),
  user: undefined,
};

const AuthSlice = createSlice({
  name: 'auth',
  initialState: initialValue,
  reducers: {
    init: state => {
      state.loggedIn = accessLocalStorage.get(LocalAccessKeys.LOGGEDIN);
    },

    login: (state, action: { payload: string }) => {
      if (action.payload) {
        state.loggedIn = action.payload;
        accessLocalStorage.set(LocalAccessKeys.LOGGEDIN, action.payload);
      }
    },

    logout: state => {
      state.loggedIn = undefined;
      accessLocalStorage.clearKey(LocalAccessKeys.LOGGEDIN);
    },
  },
});

export default AuthSlice.reducer;
export const { actions } = AuthSlice;
