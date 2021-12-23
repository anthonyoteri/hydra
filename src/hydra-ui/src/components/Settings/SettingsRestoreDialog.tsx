import {
  CaretDownOutlined,
  CaretRightOutlined,
  LoadingOutlined,
  UploadOutlined,
} from "@ant-design/icons";
import { Alert, Button, Modal } from "antd";
import Upload, { UploadChangeParam } from "antd/lib/upload";
import { FC, useState } from "react";
import { useTranslation } from "react-i18next";
import { uploadConfiguration } from "../../api/Settings";
import { ModalTitle } from "../Shared/ModalTitle";
const { Dragger } = Upload;

export enum UploadStatus {
  NONE = "None",
  CANCELLED = "Cancelled",
  LOADING = "Loading",
  LOAD_ERROR = "LoadError",
  LOADED = "Loaded",
  IMPORTING = "Importing",
  IMPORT_ERROR = "ImportError",
  COMPLETE = "Complete",
}

export type UploadedFile = {
  filename: string;
  size: number;
};

type Props = {
  onAfterClose: () => void;
};

export const SettingsRestoreDialog: FC<Props> = ({ onAfterClose }) => {
  const { t } = useTranslation();
  const [status, setStatus] = useState<UploadStatus>(UploadStatus.NONE);
  const [file, setFile] = useState<UploadedFile | null>(null);
  const [importError, setImportError] = useState<string>("");
  const [data, setData] = useState<any>(null);

  const customRequest = () => {};

  const importConfiguration = async () => {
    setStatus(UploadStatus.IMPORTING);
    try {
      await uploadConfiguration(data);
      setStatus(UploadStatus.COMPLETE);
      window.location.reload();
    } catch (err: any) {
      setImportError(JSON.stringify(err.errors, null, 4));
      setStatus(UploadStatus.IMPORT_ERROR);
    }
  };

  const onUploadChange = (info: UploadChangeParam) => {
    function onReaderLoad(event: ProgressEvent<FileReader>) {
      try {
        const json = JSON.parse(event.target!.result! as string);
        setStatus(UploadStatus.LOADED);
        setData(json);
      } catch (err) {
        setStatus(UploadStatus.LOAD_ERROR);
      }
    }

    setStatus(UploadStatus.LOADING);
    setFile({
      filename: info.file.name!,
      size: info.file.originFileObj?.size!,
    });
    var reader = new FileReader();
    reader.onload = onReaderLoad;
    reader.readAsText(info.file.originFileObj!);
  };

  const canImport = [UploadStatus.LOADED, UploadStatus.IMPORT_ERROR].includes(
    status
  );

  const footer = [
    <Button key="cancel" onClick={() => setStatus(UploadStatus.CANCELLED)}>
      {t("common.cancel")}
    </Button>,
    <Button
      key="import"
      type="primary"
      onClick={importConfiguration}
      disabled={!canImport}
      loading={status === UploadStatus.IMPORTING}
    >
      {t("settings.restoreDialog.uploadButton")}
    </Button>,
  ];

  return (
    <Modal
      title={
        <ModalTitle
          icon={<UploadOutlined />}
          title={t("settings.restoreDialog.restore")}
          subtitle={t("settings.restoreDialog.configuration")}
        />
      }
      footer={footer}
      width={640}
      visible={
        status !== UploadStatus.COMPLETE && status !== UploadStatus.CANCELLED
      }
      confirmLoading={false}
      onCancel={() => {}}
      maskClosable={true}
      afterClose={onAfterClose}
    >
      {[UploadStatus.NONE, UploadStatus.LOAD_ERROR].includes(status) && (
        <Dragger
          style={{ backgroundColor: "transparent", marginBottom: "8px" }}
          multiple={false}
          accept=".json"
          customRequest={customRequest}
          onChange={onUploadChange}
          showUploadList={false}
        >
          <UploadOutlined style={{ fontSize: "16px", marginBottom: "8px" }} />
          <p>{t("settings.restoreDialog.restoreLabel1")}</p>
        </Dragger>
      )}
      {file && status !== UploadStatus.LOAD_ERROR && (
        <div className="import-json-file">{file.filename}</div>
      )}
      {status === UploadStatus.LOADING && (
        <div style={{ textAlign: "center" }}>
          <LoadingOutlined />
        </div>
      )}
      {status === UploadStatus.LOAD_ERROR && (
        <Alert
          type="error"
          message={t("settings.restore.errorLoading", {
            file: file?.filename,
          })}
        />
      )}
      {status === UploadStatus.IMPORT_ERROR && (
        <ImportError error={importError} />
      )}
    </Modal>
  );
};

type ImportErrorProps = {
  error: string;
};

const ImportError: FC<ImportErrorProps> = ({ error }) => {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(false);
  if (!error) return null;

  const content = (
    <>
      <span
        onClick={() => setExpanded((exp) => !exp)}
        style={{ cursor: "pointer" }}
      >
        {expanded ? <CaretDownOutlined /> : <CaretRightOutlined />}
      </span>
      {t("settings.restore.errorImporting")}
      {expanded && <div>{error}</div>}
    </>
  );

  return (
    <div style={{ marginTop: "12px" }}>
      <Alert type="error" message={content} />
    </div>
  );
};
