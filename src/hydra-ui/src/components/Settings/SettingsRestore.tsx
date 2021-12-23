import { UploadOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { FC, useState } from "react";
import { useTranslation } from "react-i18next";
import { SettingsRestoreDialog } from "./SettingsRestoreDialog";

type Props = {
  disabled: boolean;
};

export const SettingsRestore: FC<Props> = ({ disabled }) => {
  const { t } = useTranslation();
  const [showUpload, setShowUpload] = useState(false);

  return (
    <div>
      {showUpload && (
        <SettingsRestoreDialog onAfterClose={() => setShowUpload(false)} />
      )}
      <Button onClick={() => setShowUpload(true)} disabled={disabled}>
        <UploadOutlined /> {t("settings.restore.showUploadButton")}
      </Button>
    </div>
  );
};
