import { createSelector, createSlice, PayloadAction } from "@reduxjs/toolkit";
import * as api from "../api/TimeReporting/Projects";
import { Project } from "../api/TimeReporting";
import { AppThunk } from "./index";
import { ApplicationState } from "./rootReducer";

interface ProjectState {
  allIds: number[];
  byId: Record<number, Project>;
}

const initialState: ProjectState = {
  allIds: [],
  byId: {},
};

export const projectReducer = createSlice({
  name: "projects",
  initialState,
  reducers: {
    fetchSuccess(state, action: PayloadAction<Project[]>) {
      state.allIds = action.payload.map((Project) => Project.id);
      state.byId = {};
      action.payload.forEach((Project) => {
        state.byId[Project.id] = Project;
      });
    },
    fetchFail(state, action: PayloadAction<any>) {},
  },
});

export const { fetchSuccess, fetchFail } = projectReducer.actions;

export default projectReducer.reducer;

export const fetchProjects =
  (): AppThunk<Promise<void>> => async (dispatch) => {
    try {
      const projects = await api.listProjects();
      dispatch(fetchSuccess(projects));
    } catch (err) {
      console.error(err);
      dispatch(fetchFail(err));
      throw err;
    }
  };

export const deleteProject =
  (id: number): AppThunk<Promise<void>> =>
  async (dispatch) => {
    try {
      await api.deleteProject(id);
      dispatch(fetchProjects());
    } catch (err) {
      throw err;
    }
  };

export const createProject =
  (body: Project): AppThunk<Promise<Project>> =>
  async (dispatch) => {
    try {
      const newProject = await api.createProject(body);
      await dispatch(fetchProjects());
      return newProject;
    } catch (err) {
      throw err;
    }
  };

export const patchProject =
  (id: number, body: Partial<Project>): AppThunk<Promise<void>> =>
  async (dispatch) => {
    try {
      await api.patchProject(id, body);
      return dispatch(fetchProjects());
    } catch (err) {
      throw err;
    }
  };

export const selectAllProjects = createSelector(
  (state: ApplicationState) => state.projects.allIds,
  (state: ApplicationState) => state.projects.byId,
  (allIds, byId) => allIds.map((id) => byId[id])
);

export const selectProjectsForCategory = createSelector(
  [
    selectAllProjects,
    (state: ApplicationState, category: number | undefined) => category,
  ],
  (projects, category) =>
    category
      ? projects.filter((p: Project) => p.category === category)
      : projects
);
