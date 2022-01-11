import { FormikProps } from "formik";
import { FC, useState } from "react";
import { useSelector } from "react-redux";
import { useTranslation } from "react-i18next";
import { CategorySelect } from "../Projects/CategorySelect";
import {
  FormikField,
  FormikFieldCheckbox,
  FormikFieldDatePicker,
} from "../Shared/Form/FormikField";
import { ProjectSelect } from "./ProjectSelect";
import { selectAllCategories } from "../../store/categories";
import { Category } from "../../api/TimeReporting";
import moment from "moment";

export interface RecordFormData {
  category: number | undefined;
  project: number | undefined;
  start_time: Date | undefined;
  stop_time: Date | undefined;
  approved: boolean | undefined;
}

type Props = {
  formik: FormikProps<RecordFormData>;
  type: string;
};

export const RecordForm: FC<Props> = ({ formik, type }) => {
  const { t } = useTranslation();
  const categories = useSelector(selectAllCategories);

  const [selectedCategory, setSelectedCategory] = useState<
    Category | undefined
  >(undefined);

  return (
    <form
      data-testid="record_form"
      onSubmit={formik.handleSubmit}
      className="ant-form ant-form-vertical"
      id={"recordForm"}
    >
      <FormikField
        name="category"
        label={t("records.createDialog.categoryLabel")}
      >
        {({ field }) => (
          <CategorySelect
            value={field.value}
            onChange={(value: number) => {
              setSelectedCategory(categories.find((c) => c.id === value));
              formik.setFieldValue("project", undefined);
              formik.setFieldValue("category", value);
            }}
            placeholder={t("records.createDialog.categoryPlaceholder")}
          />
        )}
      </FormikField>

      <FormikField
        name="project"
        label={t("records.createDialog.projectLabel")}
      >
        {({ field }) => (
          <ProjectSelect
            category={
              selectedCategory ||
              categories.find(
                (c) => c.id === formik.getFieldProps("category").value
              )
            }
            value={field.value}
            disabled={
              !selectedCategory && !formik.getFieldProps("category").value
            }
            onChange={(value: number) => formik.setFieldValue("project", value)}
            placeholder={t("records.createDialog.projectPlaceholder")}
          />
        )}
      </FormikField>

      <FormikFieldDatePicker
        name="start_time"
        label={t("records.createDialog.startTimeLabel")}
        required={true}
        autoFocus
        showTime={{ format: "HH:mm" }}
      />

      <FormikFieldDatePicker
        name="stop_time"
        label={t("records.createDialog.stopTimeLabel")}
        showTime={{ format: "HH:mm" }}
      />

      {type === "update" && (
        <FormikFieldCheckbox
          name="approved"
          disabled={
            formik.getFieldProps("start_time").value &&
            moment(formik.getFieldProps("start_time").value) > moment()
          }
        >
          {t("records.createDialog.approvedLabel")}
        </FormikFieldCheckbox>
      )}
    </form>
  );
};
