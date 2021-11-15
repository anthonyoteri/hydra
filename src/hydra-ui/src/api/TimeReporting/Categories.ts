import { instance as axios } from "../axios-instance";
import { Category } from "./types";

export const getCategory = async (id: number): Promise<Category> => {
  const response = axios.get<Category>(`/categories/${id}/`);
  return response.data;
};

export const createCategory = async (
  data: Category | {}
): Promise<Category> => {
  const response = await axios.post<Category>("/categories/", data);
  return response.data;
};

export const listCategories = async (): Promise<Category[]> => {
  const response = await axios.get<Category[]>("/categories/");
  return response.data.map((d) => {
    return { ...d };
  });
};

export const deleteCategory = async (id: number) => {
  const response = axios.delete<void>(`/categories/${id}/`);
  return response;
};

export const updateCategory = async (
  id: number,
  data: Category
): Promise<Category> => {
  const response = axoios.put<void>(`/categories/${id}/`, data);
  return response;
};

export const patchCategory = async (
  id: number,
  data: Partial<Category> | {}
): Promise<Category> => {
  const response = axios.patch<void>(`/categories/${id}/`, data);
  return response;
};
