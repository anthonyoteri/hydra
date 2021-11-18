import React, { FC } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./assets/less/main.less";
import { MainApp } from "./components/Core/MainApp";
import { ErrorBoundary } from "./components/Core/ErrorBoundary";
import Loading from "./components/Core/Loading";
import { WaitForAuthCheck } from "./components/Core/WaitForAuthCheck";
import { Login } from "./components/Login/Login";
import RequireAuth from "./components/Shared/RequireAuth";

const App: FC<{}> = () => {
  return (
    <React.Suspense fallback={<Loading />}>
      <ErrorBoundary>
        <BrowserRouter>
          <WaitForAuthCheck>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<RequireAuth path="/login" />}>
                <Route path="/" element={<MainApp />} />
              </Route>
            </Routes>
          </WaitForAuthCheck>
        </BrowserRouter>
      </ErrorBoundary>
    </React.Suspense>
  );
};

export default App;
