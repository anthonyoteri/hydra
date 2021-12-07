import { FormikProps } from "formik";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { FormikField, FormikFieldInput } from "../Shared/Form/FormikField";
import { CategorySelect } from "./CategorySelect";

export interface ProjectFormData {
  category: number | undefined;
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
      <FormikField
        name="category"
        label={t("projects.createDialog.categoryLabel")}
      >
        {({ field }) => (
          <CategorySelect
            value={field.value}
            onChange={(value: number) =>
              formik.setFieldValue("category", value)
            }
            placeholder={t("projects.createDialog.categoryPlaceholder")}
          />
        )}
      </FormikField>

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
