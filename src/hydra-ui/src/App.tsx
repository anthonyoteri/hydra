import React, { FC } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
//import './assets/less/main.less';
import { MainApp } from "./components/Core/MainApp";
import { ErrorBoundary } from "./components/Core/ErrorBoundary";
import Loading from "./components/Core/Loading";
import { WaitForAuthCheck } from "./components/Core/WaitForAuthCheck";

const App: FC<{}> = () => {
  return (
    <React.Suspense fallback={<Loading />}>
      <ErrorBoundary>
        <BrowserRouter>
          <WaitForAuthCheck>
            <Routes>
              <Route path="/" element={<MainApp />} />
            </Routes>
          </WaitForAuthCheck>
        </BrowserRouter>
      </ErrorBoundary>
    </React.Suspense>
  );
};

export default App;
