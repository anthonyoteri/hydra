import { Layout } from "antd";
import React, { FC } from "react";
import { Route, Routes } from "react-router";
import Initializer from "./Initializer";
import Loading from "./Loading";

interface Props {}

export const MainApp: FC<Props> = (props) => {
  return (
    <Initializer>
      <Layout style={{ height: "100vh" }}>
        <Layout>
          <React.Suspense fallback={<Loading />}>
            <Routes>
              <Route path="/" element={<p>Hello World!</p>} />
            </Routes>
          </React.Suspense>
        </Layout>
      </Layout>
    </Initializer>
  );
};
