import axios, { AxiosResponse } from "axios";

export interface User {
  username: string;
  email: string;
  permissions: string[];
}

export interface LoginResponse {
  authenticated: boolean;
}

export const login = async (
  username: string,
  password: string
): Promise<LoginResponse> => {
  const response = await axios.post<
    { username: string; password: string },
    AxiosResponse<LoginResponse>
  >("/auth/login/", {
    username,
    password,
  });

  return response.data;
};

export const logout = async (): Promise<null> => {
  const response = await axios.post<null, AxiosResponse<null>>(
    "/auth/logout/",
    null,
    {
      withCredentials: true,
    }
  );
  return response.data;
};

export const checkAuth = async (): Promise<User | null> => {
  try {
    const response = await axios.get<User>("/auth/check/");
    return response.data;
  } catch (err) {
    return null;
  }
};

export const confirmPassword = async (password: string): Promise<void> => {
  await axios.post<{ password: string }>("/auth/confirm/", { password });
};

export interface PasswordResetResponse {
  success: boolean;
}

export const resetRequest = async (
  email: string
): Promise<PasswordResetResponse> => {
  const response = await axios.post<
    { email: string },
    AxiosResponse<PasswordResetResponse>
  >("/auth/reset/", { email });
  return response.data;
};

export const resetChange = async (
  new_password1: string,
  new_password2: string,
  uid: string,
  token: string
): Promise<PasswordResetResponse> => {
  const response = await axios.post<
    {
      new_password1: string;
      new_password2: string;
      uid: string;
      token: string;
    },
    AxiosResponse<PasswordResetResponse>
  >(`/auth/reset-confirm/${uid}/${token}/`, {
    new_password1,
    new_password2,
    uid,
    token,
  });
  return response.data;
};
