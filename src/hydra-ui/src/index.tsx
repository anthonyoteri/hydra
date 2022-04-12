import axios from "axios";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import "resize-observer-polyfill";
import { axiosConfig } from "./api/axios-instance";
import App from "./App";
import "./i18n";
import store from "./store";

Object.assign(axios.defaults, axiosConfig);

axios.interceptors.request.use(
  (config) => {
    config.withCredentials = true;

    // Only POST,DELETE, PUT, PATCH requires csrf-tokens. Requests trigger a
    // preflight-request of this header is always set.
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

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
