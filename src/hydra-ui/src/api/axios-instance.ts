import axios, { AxiosError, AxiosRequestConfig } from "axios";
import config from "../config";
import { ApiError } from "./errors";

export const axiosConfig: AxiosRequestConfig = {
  baseURL: config.STACK_BASE_URL + config.API_BASE_URL,
  timeout: 15000,
};

export const instance = axios.create(axiosConfig);

instance.interceptors.request.use(
  (config) => {
    config.withCredentials = true;

    // Only POST, DELETE, PUT, PATCH requiries csrf-tokens. Requests trigger a
    // preflight-request fo this header is always set.
    if (config.method !== "get") {
      config.xsrfHeaderName = "X-CSRFToken";
      config.xsrfCookieName = "csrftoken";
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (axios.isCancel(error)) {
      return Promise.reject(error);
    }

    // Sentry.captureException(error);

    if (
      error.response &&
      [401, 403].includes(error.response.status) &&
      !window.location.href.endsWith("/login")
    ) {
      window.location.href = "/login";
      return Promise.reject(createApiError(error));
    } else {
      return Promise.reject(createApiError(error));
    }
  }
);

export const createApiError = (error: AxiosError): ApiError => {
  if (error.response) {
    if (error.response.data?.errors) {
      return {
        type: "server",
        errors: error.response.data.errors,
        status: error.response.status,
      };
    } else {
      return {
        type: "server",
        errors: [
          {
            code: "internal_error",
            message: "Server Error",
          },
        ],
        status: error.response.status,
      };
    }
  } else if (error.request) {
    return {
      type: "network",
      error: error.message,
    };
  }

  return {
    type: "unknown",
    error: error.message,
  };
};
