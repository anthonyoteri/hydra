import { instance as axios } from "../axios-instance";
import { Project } from "./types";

export const getProject = async (id: number): Promise<Project> => {
  const response = await axios.get<Project>(`/projects/${id}/`);
  return response.data;
};

export const createProject = async (data: Project | {}): Promise<Project> => {
  const response = await axios.post<Project>("/projects/", data);
  return response.data;
};

export const listProjects = async (): Promise<Project[]> => {
  const response = await axios.get<Project[]>("/projects/");
  return response.data.map((d) => {
    return { ...d };
  });
};

export const deleteProject = async (id: number) => {
  const response = axios.delete<void>(`/projects/${id}/`);
  return response;
};

export const updateProject = (id: number, data: Project) => {
  const response = axios.put<void>(`/projects/${id}/`, data);
  return response;
};

export const patchProject = (id: number, data: Partial<Project> | {}) => {
  const response = axios.patch<void>(`/projects/${id}/`, data);
  return response;
};
