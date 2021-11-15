import { combineReducers } from "@reduxjs/toolkit";

import { categoryReducer } from "./categories";
import { projectReducer } from "./projects";
import { timeRecordReducer } from "./timeRecords";

const rootReducer = combineReducers({
  categories: categoryReducer,
  projects: projectReducer,
  records: timeRecordReducer,
});

export type ApplicationState = ReturnType<typeof rootReducer>;
export default rootReducer;
