import axios from "axios";
export interface AppInfo {
  app_version: string;
  timezone: string;
  debug: boolean;
}

export const getAppInfo = async (): Promise<AppInfo | null> => {
  try {
    const response = await axios.get<AppInfo>("/about/");
    return response.data;
  } catch (err) {
    return null;
  }
};
