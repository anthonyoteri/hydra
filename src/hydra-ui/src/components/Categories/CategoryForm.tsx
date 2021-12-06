import { FormikProps } from "formik";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { FormikFieldInput } from "../Shared/Form/FormikField";

export interface CategoryFormData {
  name: string;
  description: string;
}

type Props = {
  formik: FormikProps<CategoryFormData>;
};

export const CategoryForm: FC<Props> = ({ formik }) => {
  const { t } = useTranslation();
  return (
    <form
      data-testid="category_form"
      onSubmit={formik.handleSubmit}
      className="ant-form ant-form-vertical"
      id={"categoryForm"}
    >
      <FormikFieldInput
        name="name"
        label={t("categories.createDialog.nameLabel")}
        required={true}
        autoFocus
      />

      <FormikFieldInput
        name="description"
        label={t("categories.createDialog.descriptionLabel")}
      />
    </form>
  );
};
