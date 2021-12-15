import { useTranslation } from "react-i18next";
import { Modal } from "antd";
import { Formik, FormikHelpers } from "formik";
import { FC, useState } from "react";
import { useSelector } from "react-redux";
import { TimeRecord, TimeRecordDraft } from "../../api/TimeReporting";
import { RecordForm, RecordFormData } from "./RecordForm";
import { selectAllProjects } from "../../store/projects";
import { Project } from "../../api/TimeReporting";
import useModalForm from "../../hooks/useModalForm";
import { parseErrors } from "../../utils/formHelpers";
import { ModalFormFooter } from "../Shared/ModalFormFooter";
import { ModalTitle } from "../Shared/ModalTitle";
import { AppstoreOutlined } from "@ant-design/icons";
import { FormError } from "../Shared/Form/FormError";

interface Props {
  type: "create" | "update";
  onOk: (project: TimeRecord) => Promise<any>;
  onComplete: () => void;
  onCancel: () => void;
  record: TimeRecordDraft;
}

export const RecordDialog: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { onOk, onComplete, onCancel, type } = props;
  const projects = useSelector(selectAllProjects);
  const [formData] = useState<RecordFormData>({
    category:
      props.record.project !== 0
        ? projects.find((p: Project) => p.id === props.record.project)?.category
        : undefined,
    project: props.record.project !== 0 ? props.record.project : undefined,
    start_time: props.record.start_time,
    stop_time: props.record.stop_time,
  });
  const { isVisible, isSaving, error, setStatus, setError, handleAfterClose } =
    useModalForm({ onCancel: onCancel, onComplete: onComplete });

  const handleCancel = () => {
    setStatus("cancelled");
  };

  const compileRecord = (formData: RecordFormData): TimeRecord => {
    return {
      project: formData.project,
      start_time: formData.start_time,
      stop_time: formData.stop_time,
    } as TimeRecord;
  };

  const handleSubmit = async (
    record: RecordFormData,
    formikHelpers: FormikHelpers<RecordFormData>
  ) => {
    setStatus("saving");
    setError(null);

    try {
      await onOk(compileRecord(record));
      setStatus("completed");
    } catch (err: any) {
      const { formErrors, error } = parseErrors<RecordFormData>(err);
      if (err.type === "server") {
        formErrors && formikHelpers.setErrors(formErrors);
        setError(err);
      } else {
        setError(error);
      }
      setStatus("error");
    }
  };

  const Footer = (
    <ModalFormFooter
      formName="recordForm"
      onCancel={handleCancel}
      isLoading={isSaving}
      submitButtonText={
        type === "create" ? t("common.create") : t("common.saveChanges")
      }
    />
  );

  return (
    <Modal
      title={
        <ModalTitle
          icon={<AppstoreOutlined />}
          title={type === "create" ? t("common.createNew") : t("common.edit")}
          subtitle={t("records.createDialog.subTitle")}
        />
      }
      width={640}
      visible={isVisible}
      confirmLoading={isSaving}
      onCancel={handleCancel}
      footer={Footer}
      maskClosable={false}
      afterClose={handleAfterClose}
    >
      <Formik initialValues={formData} onSubmit={handleSubmit}>
        {(props) => <RecordForm formik={props} />}
      </Formik>

      <FormError error={error} />
    </Modal>
  );
};
