import { Typography } from "antd";
import { ReactNode } from "react";

type Props = {
  title: string | ReactNode;
  extra?: ReactNode;
};

export function MainHeader({ title, extra }: Props) {
  return (
    <header className="main-header">
      <div className="main-header-title">
        <Typography.Title level={4}>{title}</Typography.Title>
      </div>

      {extra}
    </header>
  );
}
