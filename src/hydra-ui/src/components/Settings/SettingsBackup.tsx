import { DownloadOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { format } from "date-fns";
import { FC, useState } from "react";
import { useTranslation } from "react-i18next";
import { downloadConfiguration } from "../../api/Settings";

type Props = {};

export const SettingsBackup: FC<Props> = (props) => {
  const { t } = useTranslation();
  const [isDownloading, setIsDownloading] = useState<boolean>(false);

  const download = async () => {
    try {
      setIsDownloading(true);
      const json = await downloadConfiguration();
      const timestamp = format(new Date(), "yyyyLLddkkmmss");
      const url = window.URL.createObjectURL(
        new Blob([JSON.stringify(json.data, null, 2)])
      );
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `config-${timestamp}.json`);
      document.body.appendChild(link);
      link.click();
      link.parentNode!.removeChild(link);
      setIsDownloading(false);
    } catch (err) {
      console.log(err);
      setIsDownloading(false);
    }
  };

  return (
    <Button onClick={download} loading={isDownloading}>
      <DownloadOutlined /> {t("settings.backup.downloadButton")}
    </Button>
  );
};
