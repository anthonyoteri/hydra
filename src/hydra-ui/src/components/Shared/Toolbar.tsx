import clsx from "clsx";
import React, { ReactElement } from "react";

type Props = {};

export function Toolbar({ children }: React.PropsWithChildren<Props>) {
  return (
    <div className="toolbar">
      {React.Children.map(children, (child) => {
        if ((child as ReactElement).type! !== ToolbarGroup) {
          return <ToolbarGroup>{child}</ToolbarGroup>;
        }
        return child;
      })}
    </div>
  );
}

type ToolbarGroupProps = {
  align?: "left" | "right" | "center";
  style?: React.CSSProperties;
};

export function ToolbarGroup({
  children,
  align = "left",
  ...rest
}: React.PropsWithChildren<ToolbarGroupProps>) {
  return (
    <div
      className={clsx(
        "toolbar-group",
        align === "right" && "toolbar-group-right",
        align === "center" && "toolbar-group-center"
      )}
      {...rest}
    >
      {React.Children.map(children, (child) => {
        if (!child) return child;

        if ((child as ReactElement).type === ToolbarItem) {
          return child;
        }

        return <ToolbarItem>{child}</ToolbarItem>;
      })}
    </div>
  );
}

type ToolbarItemProps = {
  label?: string;
};

export const ToolbarItem = ({
  children,
  label,
}: React.PropsWithChildren<ToolbarItemProps>) => {
  return (
    <div className="toolbar-item">
      {label && <div className="toolbar-item-label">{label || "\u00A0"}</div>}
      {children}
    </div>
  );
};
