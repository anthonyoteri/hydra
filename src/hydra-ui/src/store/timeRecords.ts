import { createSlice, createSelector, PayloadAction } from "@reduxjs/toolkit";
import * as api from "../api/TimeReporting/TimeRecords";
import { TimeRecord } from "../api/TimeReporting";
import { AppThunk } from "./index";
import { ApplicationState } from "../store/rootReducer";
import moment from "moment";

interface TimeRecordState {
  allIds: number[];
  byId: Record<number, TimeRecord>;
}

const initialState: TimeRecordState = {
  allIds: [],
  byId: {},
};

export const timeRecordReducer = createSlice({
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

export const deleteRecord =
  (id: number): AppThunk<Promise<void>> =>
  async (dispatch) => {
    try {
      await api.deleteRecord(id);
      dispatch(fetchRecords());
    } catch (err) {
      throw err;
    }
  };

export const createRecord =
  (body: TimeRecord): AppThunk<Promise<TimeRecord>> =>
  async (dispatch) => {
    try {
      const newTimeRecord = await api.createRecord(body);
      await dispatch(fetchRecords());
      return newTimeRecord;
    } catch (err) {
      throw err;
    }
  };

export const patchRecord =
  (id: number, body: Partial<TimeRecord>): AppThunk<Promise<void>> =>
  async (dispatch) => {
    try {
      await api.patchRecord(id, body);
      return dispatch(fetchRecords());
    } catch (err) {
      throw err;
    }
  };

export const selectAllRecords = createSelector(
  (state: ApplicationState) => state.records.allIds,
  (state: ApplicationState) => state.records.byId,
  (allIds, byId) => allIds.map((id) => byId[id])
);

export const selectRecordsForWeek = createSelector(
  [selectAllRecords, (state: ApplicationState, week: number) => week],
  (records, week) => {
    return records.filter(
      (r: TimeRecord) => moment(r.start_time).isoWeek() === week
    );
  }
);
