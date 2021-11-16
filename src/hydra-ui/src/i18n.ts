import i18n, { InitOptions } from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import Backend from "i18next-http-backend";
import { initReactI18next } from "react-i18next";
import config from "./config";

const debug = process.env.NODE_ENV === "development";

// https://www.i18next.com/overview/configuration-options
const options: InitOptions = {
  load: "languageOnly",
  fallbackLng: "en",
  debug: debug,
  nsSeparator: "#",
  keySeparator: ".",
  interpolation: {
    escapeValue: false,
  },
  backend: {
    crossDomain: true,
    loadPath: config.STACK_BASE_URL + "/locales/{{lng}}/{{ns}}.json",
    addPath: config.STACK_BASE_URL + "/locales/add/{{lng}}/{{ns}}",
  },
};

i18n.use(Backend).use(LanguageDetector).use(initReactI18next).init(options);

export default i18n;
