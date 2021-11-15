import { configureStore } from "@reduxjs/toolkit";
import { useSelector } from "react-redux";
import { AnyAction } from "redux";
import { ThunkAction } from "redux-thunk";
import rootReducer, { ApplicationState } from "./rootReducer";

export const store = configureStore({
  reducer: rootReducer,
});

export type AppDispatch = typeof store.dispatch;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  ApplicationState,
  unknown,
  AnyAction
>;

export default store;
