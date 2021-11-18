import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AxiosError } from "axios";
import { isArray } from "lodash";
import { useSelector } from "react-redux";
import * as api from "../api/Auth/Auth";
import { LoginResponse } from "../api/Auth/Auth";
import { ApiError } from "../api/errors";
import { createApiError } from "./../api/axios-instance";
import { AppThunk } from "./index";
import { ApplicationState } from "./rootReducer";

export enum AuthStatus {
  ANONYMOUS,
  AUTHENTICATED,
  PENDING,
  VERIFIED,
  WAITING,
}

export type Permission = string;

export interface AuthState {
  status: AuthStatus;
  returnUrl: string | null;
  isLoading: boolean;
  user: api.User | null;
}

const initialState: AuthState = {
  status: AuthStatus.WAITING,
  returnUrl: null,
  isLoading: false,
  user: null,
};

const auth = createSlice({
  name: "auth",
  initialState,
  reducers: {
    clear(state, action: PayloadAction<void>) {
      state.user = null;
      state.status = AuthStatus.ANONYMOUS;
    },
    setStatus(state, action: PayloadAction<AuthStatus>) {
      state.status = action.payload;
    },
    loginSetLoading(state, action: PayloadAction<boolean>) {
      state.isLoading = action.payload;
    },
    loginSuccess(state, action: PayloadAction<LoginResponse>) {
      state.status = AuthStatus.WAITING;
    },
    loginFailed(state, action: PayloadAction<string>) {},
    authCheckSuccess(state, action: PayloadAction<any>) {
      state.status = AuthStatus.AUTHENTICATED;
      state.user = action.payload;
    },
    authCheckFail(state, action: PayloadAction<void>) {
      state.status = AuthStatus.ANONYMOUS;
    },
    privateRouteAccessFail(state, action: PayloadAction<string>) {
      state.returnUrl = action.payload;
    },
  },
});

export const {
  loginFailed,
  loginSuccess,
  loginSetLoading,
  setStatus,
  authCheckSuccess,
  authCheckFail,
  privateRouteAccessFail,
  clear,
} = auth.actions;

export default auth.reducer;

export const attemptLogin =
  (username: string, password: string): AppThunk =>
  async (dispatch) => {
    try {
      dispatch(clear());
      dispatch(loginSetLoading(true));
      const authDetails = await api.login(username, password);
      dispatch(loginSuccess(authDetails));
    } catch (err) {
      throw createApiError(err as AxiosError<ApiError>);
    }

    dispatch(loginSetLoading(false));
  };

export const logout = (): AppThunk => async (dispatch) => {
  try {
    await api.logout();
    dispatch(clear());
  } catch (err) {
    dispatch(clear());
  }
};

export const checkAuth = (): AppThunk => async (dispatch, getState) => {
  dispatch(setStatus(AuthStatus.PENDING));
  const authDetails = await api.checkAuth();
  if (!authDetails) {
    return dispatch(authCheckFail());
  }
  dispatch(authCheckSuccess(authDetails));
};

export const usePermissions = () =>
  useSelector((state: ApplicationState) => {
    return state.auth.user!.permissions;
  });

export function useCheckPermissions(permission: string): boolean;
export function useCheckPermissions(permission: string[]): boolean[];
export function useCheckPermissions(permission: any): any {
  const userPermissions = useSelector(
    (state: ApplicationState) => state.auth.user?.permissions
  );

  if (isArray(permission)) {
    return permission.map((p) => userPermissions?.includes(p));
  }

  return userPermissions?.includes(permission);
}
