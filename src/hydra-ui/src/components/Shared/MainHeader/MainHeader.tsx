import { Typography } from "antd";
import { ReactNode } from "react";
import { Outlet } from "react-router-dom";

type Props = {
  title: string | ReactNode;
};

export function MainHeader({ title }: Props) {
  return (
    <header className="main-header">
      <div className="main-header-title">
        <Typography.Title level={4}>{title}</Typography.Title>
      </div>
      <Outlet />
    </header>
  );
}
