import { FormikProps } from "formik";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { FormikFieldInput } from "../Shared/Form/FormikField";

export interface ProjectFormData {
  name: string;
  description: string;
}

type Props = {
  formik: FormikProps<ProjectFormData>;
};

export const ProjectForm: FC<Props> = ({ formik }) => {
  const { t } = useTranslation();
  return (
    <form
      data-testid="project_form"
      onSubmit={formik.handleSubmit}
      className="ant-form ant-form-vertical"
      id={"projectForm"}
    >
      <FormikFieldInput
        name="name"
        label={t("projects.createDialog.nameLabel")}
        required={true}
        autoFocus
      />

      <FormikFieldInput
        name="description"
        label={t("projects.createDialog.descriptionLabel")}
      />
    </form>
  );
};
