const parseDomain = (baseUrl: string) => {
  try {
    return new URL(baseUrl).hostname;
  } catch {
    return window.location.hostname;
  }
};

const REACT_APP_BASE_URL = process.env.REACT_APP_BASE_URL ?? "/t1/v1";

const config = {
  API_BASE_URL: REACT_APP_BASE_URL,
  API_DOMAIN: parseDomain(REACT_APP_BASE_URL),
  STACK_BASE_URL: window.env?.STACK_BASE_URL,
  ENVIRONMENT: window.env?.APP_ENVIRONMENT,
  VERSION: window.env?.APP_VERSION,
};

export default config;
