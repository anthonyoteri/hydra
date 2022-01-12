import { instance as axios } from "../axios-instance";
import { Settings } from "./types";

export * from "./types";

export const downloadConfiguration = () => {
  const response = axios.get<any>(`/config/`);
  return response;
};

export const uploadConfiguration = (data: any) => {
  const response = axios.put<any>(`/config/`, data);
  return response;
};

export const fetchSettings = async (): Promise<Settings> => {
  const response = await axios.get<Settings>(`/settings/`);
  return response.data;
};

export const updateSettings = (data: Settings) => {
  const response = axios.put<Settings>(`/settings/`, data);
  return response;
};
