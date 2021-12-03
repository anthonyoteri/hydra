import { Button } from "antd";
import React, { FC } from "react";
import { useTranslation } from "react-i18next";

interface Props {
  onCancel: (e: any) => void;
  formName: string;
  submitButtonText: string;
  isLoading: boolean;
  extra?: React.ReactNode;
}

export const ModalFormFooter: FC<Props> = ({
  onCancel,
  formName,
  isLoading,
  submitButtonText,
  extra,
}) => {
  const { t } = useTranslation();

  return (
    <>
      {extra}
      <Button onClick={onCancel} key="cancel" data-testid="modal_form_cancel">
        {t("common.cancel")}
      </Button>
      <Button
        type="primary"
        form={formName}
        htmlType="submit"
        key="submit"
        loading={isLoading}
        data-testid="modal_form_ok"
      >
        {submitButtonText}
      </Button>
    </>
  );
};
