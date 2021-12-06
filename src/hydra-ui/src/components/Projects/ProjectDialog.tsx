import { useTranslation } from "react-i18next";
import { Modal } from "antd";
import { Formik, FormikHelpers } from "formik";
import { FC, useState } from "react";
import { Project, ProjectDraft } from "../../api/TimeReporting";
import { ProjectForm, ProjectFormData } from "./ProjectForm";
import useModalForm from "../../hooks/useModalForm";
import { parseErrors } from "../../utils/formHelpers";
import { ModalFormFooter } from "../Shared/ModalFormFooter";
import { ModalTitle } from "../Shared/ModalTitle";
import { AppstoreOutlined } from "@ant-design/icons";
import { FormError } from "../Shared/Form/FormError";

interface Props {
  type: "create" | "update";
  onOk: (project: Project) => Promise<any>;
  onComplete: () => void;
  onCancel: () => void;
  project: ProjectDraft;
}

export const ProjectDialog: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { onOk, onComplete, onCancel, type } = props;
  const [formData] = useState<ProjectFormData>({
    name: props.project.name,
    description: props.project.description,
  });
  const { isVisible, isSaving, error, setStatus, setError, handleAfterClose } =
    useModalForm({ onCancel: onCancel, onComplete: onComplete });

  const handleCancel = () => {
    setStatus("cancelled");
  };

  const compileProject = (formData: ProjectFormData): Project => {
    return {
      name: formData.name,
      description: formData.description,
    } as Project;
  };

  const handleSubmit = async (
    project: ProjectFormData,
    formikHelpers: FormikHelpers<ProjectFormData>
  ) => {
    setStatus("saving");
    setError(null);

    try {
      await onOk(compileProject(project));
      setStatus("completed");
    } catch (err: any) {
      const { formErrors, error } = parseErrors<ProjectFormData>(err);
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
      formName="projectForm"
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
          title={type === "create" ? t("common.createNew") : props.project.name}
          subtitle={t("projects.createDialog.subTitle")}
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
        {(props) => <ProjectForm formik={props} />}
      </Formik>

      <FormError error={error} />
    </Modal>
  );
};
