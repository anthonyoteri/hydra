import React, { FC } from "react";

type Props = {
  title: string;
  subtitle?: string;
  icon?: React.ReactNode;
};

export const ModalTitle: FC<Props> = ({ title, subtitle, icon }) => {
  return (
    <div style={{ display: "flex" }}>
      <div style={{ fontSize: "32px", marginRight: "8px" }}>{icon && icon}</div>
      <div>
        {subtitle && <small>{subtitle}</small>}
        {title}
      </div>
    </div>
  );
};
