import { Layout } from "antd";
import { FC } from "react";
import { Outlet } from "react-router";
import Initializer from "./Initializer";

import { Nav } from "./Nav";

interface Props {}

export const MainApp: FC<Props> = (props) => {
  return (
    <Initializer>
      <Layout style={{ height: "100vh" }}>
        <Nav />
        <Layout>
          <Outlet />
        </Layout>
      </Layout>
    </Initializer>
  );
};
