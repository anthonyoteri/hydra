import { Alert } from "antd";
import React, { FC, useState } from "react";
import { ApiError } from "../../../api/errors";
import { CaretRightOutlined, CaretDownOutlined } from "@ant-design/icons";

export type FormErrorProps = {
  error: ApiError | null;
  summary?: string | React.ReactNode;
};

export const FormError: FC<FormErrorProps> = ({ error, summary }) => {
  const [expanded, setExpanded] = useState(false);
  if (!error) return null;

  const getMessage = (err: ApiError) => {
    switch (err.type) {
      case "network":
        return err.error;
      case "server":
        return err.errors.length
          ? err.errors
              .map((e) => (e.field ? e.field + ": " : "") + e.message)
              .join("\n")
          : null;
    }
  };

  const message = getMessage(error);

  const content = summary ? (
    <>
      <span
        onClick={() => setExpanded((exp) => !exp)}
        style={{ cursor: "pointer" }}
      >
        {expanded ? <CaretDownOutlined /> : <CaretRightOutlined />}
      </span>{" "}
      {summary}
      {expanded && <div>{message}</div>}
    </>
  ) : (
    message
  );

  return message ? (
    <div style={{ marginTop: "12px" }}>
      <Alert type="error" message={content} />
    </div>
  ) : null;
};
