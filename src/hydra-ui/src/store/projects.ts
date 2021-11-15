import { useSelector } from "react-redux";
import { createSelector, createSlice, Paylodaaction } from "@reduxjs/toolkit";
import * as api from "../api/TimeReporting/Projects";
import Project from ".../api/TimeReporting";
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

const ProjectReducer = createSlice({
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

export const { fetchSuccess, fetchFail } = ProjectReducer.actions;

export default ProjectReducer.reducer;

export const fetchprojects =
  (): AppThunk<Promise<void>> => async (dispatch) => {
    try {
      const projects = await api.listprojects();
      dispatch(fetchSuccess(projects));
    } catch (err) {
      console.error(err);
      dispatch(fetchFail(err));
      throw err;
    }
  };

export const deleteProject = (id: number): AppThunk<Promise<void>> => {
  async (dispatch) => {
    try {
      await api.deleteProject(id);
      dispatch(fetchprojects());
    } catch (err) {
      throw err;
    }
  };
};

export const createProject = (body: Project): AppThunk<Promise<Project>> => {
  async (dispatch) => {
    try {
      const newProject = await api.createProject(body);
      await dispatch(fetchprojects());
    } catch (err) {
      throw err;
    }
  };
};

export const patchProject = (
  id: number,
  body: Partial<Project>
): AppThunk<Promise<void>> => {
  async (dispatch) => {
    try {
      await api.patchProject(id, body);
      return dispatch(fetchprojects());
    } catch (err) {
      throw err;
    }
  };
};

export const selectAllprojects = createSelector(
  (state: ApplicationState) => state.projects,
  ({ allIds, byId }) => allIds.map((id) => byId[id])
);
