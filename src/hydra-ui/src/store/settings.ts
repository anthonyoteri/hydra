import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import * as api from "../api/Settings";
import { Settings } from "../api/Settings";
import { AppThunk } from "./index";
import { ApplicationState } from "./rootReducer";

interface SettingsState {
  active: Settings;
}

const initialState: SettingsState = {
  active: {},
};

export const settingsReducer = createSlice({
  name: "settings",
  initialState,
  reducers: {
    fetchSuccess(state, action: PayloadAction<Settings>) {
      state.active = action.payload;
    },
    fetchFail(state, action: PayloadAction<any>) {},
  },
});

export const { fetchSuccess, fetchFail } = settingsReducer.actions;

export default settingsReducer.reducer;

export const fetchSettings =
  (): AppThunk<Promise<void>> => async (dispatch) => {
    try {
      const settings = await api.fetchSettings();
      dispatch(fetchSuccess(settings));
    } catch (err) {
      console.error(err);
      dispatch(fetchFail(err));
      throw err;
    }
  };

export const saveSettings =
  (body: Settings): AppThunk<Promise<void>> =>
  async (dispatch) => {
    try {
      await api.updateSettings(body);
      return dispatch(fetchSettings());
    } catch (err) {
      throw err;
    }
  };

export const selectSettings = (state: ApplicationState) =>
  state.settings.active;
