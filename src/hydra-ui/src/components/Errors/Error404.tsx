import React, { FC } from "react";
import { Result } from "antd";
import { useTranslation } from "react-i18next";
import { WarningFilled } from "@ant-design/icons";

type Props = {
  message?: string;
};

export const Error404: FC<Props> = ({ message }) => {
  const { t } = useTranslation();

  return (
    <>
      <Result
        status="warning"
        title="404"
        icon={<WarningFilled />}
        subTitle={message || t("errors.404text")}
      />
    </>
  );
};
