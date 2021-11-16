import "@testing-library/jest-dom/extend-expect";
import "jest-canvas-mock";
import "./i18n";
// import { server } from './mocks/server';

declare global {
  interface Window {
    env: any;
  }
}

process.env.REACT_APP_BASE_URL = "";
window.env = {
  APP_ENVIRONMENT: "test",
  APP_VERSION: "abc",
  SENTRY_TAGS: "",
  STACK_BASE_URL: "",
};

Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
// afterEach(() => server.resetHandlers());
// afterAll(() => server.close());

//@ts-ignore
window.IntersectionObserver = jest.fn(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

beforeEach(() => {
  // naive way to add SVGElement to window if it doesn't exist
  if (!window.SVGElement) {
    //@ts-ignore
    window.SVGElement = {};
  }

  //@ts-ignore
  window.SVGElement.prototype.transform = {
    baseVal: {
      consolidate: () => {},
    },
  };

  //@ts-ignore
  window.SVGElement.prototype.getBBox = () => ({
    x: 0,
    y: 0,
    // whatever other props you need
  });

  //@ts-ignore
  window.SVGElement.prototype.getComputedTextLength = () => ({
    x: 0,
    y: 0,
    // whatever other props you need
  });
});
