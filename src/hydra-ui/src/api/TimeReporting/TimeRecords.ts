import { instance as axios } from "../axios-instance";
import { TimeRecord } from "./types";

export const getRecord = async (id: number): Promise<TimeRecord> => {
  const response = axios.get<TimeRecord>(`/records/${id}/`);
  return response.data;
};

export const createRecord = async (
  data: TimeRecord | {}
): Promise<TimeRecord> => {
  const response = await axios.post<TimeRecord>("/records/", data);
  return response.data;
};

export const listRecords = async (): Promise<TimeRecord[]> => {
  const response = await axios.get<TimeRecord[]>("/records/");
  return response.data.map((d) => {
    return { ...d };
  });
};

export const deleteRecord = async (id: number) => {
  const response = axios.delete<void>(`/records/${id}/`);
  return response;
};

export const updateRecord = async (
  id: number,
  data: TimeRecord
): Promise<TimeRecord> => {
  const response = axoios.put<void>(`/records/${id}/`, data);
  return response;
};

export const patchRecord = async (
  id: number,
  data: Partial<TimeRecord> | {}
): Promise<TimeRecord> => {
  const response = axios.patch<void>(`/records/${id}/`, data);
  return response;
};
