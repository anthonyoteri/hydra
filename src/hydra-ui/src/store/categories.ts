import { createSelector, createSlice, PayloadAction } from "@reduxjs/toolkit";
import * as api from "../api/TimeReporting/Categories";
import { Category } from "../api/TimeReporting";
import { AppThunk } from "./index";
import { ApplicationState } from "./rootReducer";

interface CategoryState {
  allIds: number[];
  byId: Record<number, Category>;
}

const initialState: CategoryState = {
  allIds: [],
  byId: {},
};

export const categoryReducer = createSlice({
  name: "categories",
  initialState,
  reducers: {
    fetchSuccess(state, action: PayloadAction<Category[]>) {
      state.allIds = action.payload.map((category) => category.id);
      state.byId = {};
      action.payload.forEach((category) => {
        state.byId[category.id] = category;
      });
    },
    fetchFail(state, action: PayloadAction<any>) {},
  },
});

export const { fetchSuccess, fetchFail } = categoryReducer.actions;

export default categoryReducer.reducer;

export const fetchCategories =
  (): AppThunk<Promise<void>> => async (dispatch) => {
    try {
      const categories = await api.listCategories();
      dispatch(fetchSuccess(categories));
    } catch (err) {
      console.error(err);
      dispatch(fetchFail(err));
      throw err;
    }
  };

export const deleteCategory =
  (id: number): AppThunk<Promise<void>> =>
  async (dispatch) => {
    try {
      await api.deleteCategory(id);
      dispatch(fetchCategories());
    } catch (err) {
      throw err;
    }
  };

export const createCategory =
  (body: Category): AppThunk<Promise<Category>> =>
  async (dispatch) => {
    try {
      const newCategory = await api.createCategory(body);
      await dispatch(fetchCategories());
      return newCategory;
    } catch (err) {
      throw err;
    }
  };

export const patchCategory =
  (id: number, body: Partial<Category>): AppThunk<Promise<void>> =>
  async (dispatch) => {
    try {
      await api.patchCategory(id, body);
      return dispatch(fetchCategories());
    } catch (err) {
      throw err;
    }
  };

export const selectAllCategories = createSelector(
  (state: ApplicationState) => state.categories,
  ({ allIds, byId }) => allIds.map((id) => byId[id])
);
