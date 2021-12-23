import { instance as axios } from "../axios-instance";

export const downloadConfiguration = () => {
  const response = axios.get<any>(`/config/`);
  return response;
};

export const uploadConfiguration = (data: any) => {
  const response = axios.put<any>(`/config/`, data);
  return response;
};
