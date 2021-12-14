import React, { FC } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./assets/less/main.less";
import { MainApp } from "./components/Core/MainApp";
import { ErrorBoundary } from "./components/Core/ErrorBoundary";
import Loading from "./components/Core/Loading";
import { WaitForAuthCheck } from "./components/Core/WaitForAuthCheck";
import { Login } from "./components/Login/Login";
import RequireAuth from "./components/Shared/RequireAuth";

import { Error404 } from "./components/Core/Error404";
import { CategoryView } from "./components/Categories/CategoryView";
import { CategoryDetailView } from "./components/Categories/CategoriesDetailView";
import { ProjectView } from "./components/Projects/ProjectView";
import { ProjectDetailView } from "./components/Projects/ProjectDetailView";
import { RecordView } from "./components/Records/RecordView";
import { RecordDetailView } from "./components/Records/RecordDetailView";

const App: FC<{}> = () => {
  return (
    <React.Suspense fallback={<Loading />}>
      <ErrorBoundary>
        <BrowserRouter>
          <WaitForAuthCheck>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<RequireAuth path="/login" />}>
                <Route path="/" element={<MainApp />}>
                  <Route path="home" element={<p>Home</p>} />
                  <Route path="categories" element={<CategoryView />}>
                    <Route path=":id" element={<CategoryDetailView />} />
                  </Route>
                  <Route path="projects" element={<ProjectView />}>
                    <Route path=":id" element={<ProjectDetailView />} />
                  </Route>
                  <Route path="records" element={<RecordView />}>
                    <Route path=":id" element={<RecordDetailView />} />
                  </Route>
                  <Route path="history" element={<p>History</p>} />
                  <Route path="timecards" element={<p>Timecards</p>} />
                </Route>
              </Route>
              <Route path="*" element={<Error404 />} />
            </Routes>
          </WaitForAuthCheck>
        </BrowserRouter>
      </ErrorBoundary>
    </React.Suspense>
  );
};

export default App;
