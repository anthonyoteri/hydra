import { combineReducers } from "@reduxjs/toolkit";
import authReducer from "./auth";
import categoryReducer from "./categories";
import projectReducer from "./projects";
import timeRecordReducer from "./timeRecords";
import settingsReducer from "./settings";

const rootReducer = combineReducers({
  auth: authReducer,
  categories: categoryReducer,
  projects: projectReducer,
  records: timeRecordReducer,
  settings: settingsReducer,
});

export type ApplicationState = ReturnType<typeof rootReducer>;
export default rootReducer;
