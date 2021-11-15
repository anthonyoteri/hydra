import { useSelector } from "react-redux";
import { createSelector, createSlice, Paylodaaction } from "@reduxjs/toolkit";
import * as api from "../api/TimeReporting/TimeRecords";
import TimeRecord from ".../api/TimeReporting";
import { AppThunk } from "./index";
import { ApplicationState } from "./rootReducer";

interface TimeRecordState {
  allIds: number[];
  byId: Record<number, TimeRecord>;
}

const initialState: timeRecordState = {
  allIds: [],
  byId: {},
};

const timeRecordReducer = createSlice({
  name: "records",
  initialState,
  reducers: {
    fetchSuccess(state, action: PayloadAction<TimeRecord[]>) {
      state.allIds = action.payload.map((record) => record.id);
      state.byId = {};
      action.payload.forEach((record) => {
        state.byId[record.id] = record;
      });
    },
    fetchFail(state, action: PayloadAction<any>) {},
  },
});

export const { fetchSuccess, fetchFail } = timeRecordReducer.actions;

export default timeRecordReducer.reducer;

export const fetchRecords = (): AppThunk<Promise<void>> => async (dispatch) => {
  try {
    const records = await api.listRecords();
    dispatch(fetchSuccess(records));
  } catch (err) {
    console.error(err);
    dispatch(fetchFail(err));
    throw err;
  }
};

export const deleteRecord = (id: number): AppThunk<Promise<void>> => {
  async (dispatch) => {
    try {
      await api.deleteRecord(id);
      dispatch(fetchRecords());
    } catch (err) {
      throw err;
    }
  };
};

export const createRecord = (
  body: TimeRecord
): AppThunk<Promise<TimeRecord>> => {
  async (dispatch) => {
    try {
      const newTimeRecord = await api.createRecord(body);
      await dispatch(fetchRecords());
    } catch (err) {
      throw err;
    }
  };
};

export const patchRecord = (
  id: number,
  body: Partial<TimeRecord>
): AppThunk<Promise<void>> => {
  async (dispatch) => {
    try {
      await api.patchRecord(id, body);
      return dispatch(fetchRecords());
    } catch (err) {
      throw err;
    }
  };
};

export const selectAllRecords = createSelector(
  (state: ApplicationState) => state.records,
  ({ allIds, byId }) => allIds.map((id) => byId[id])
);
