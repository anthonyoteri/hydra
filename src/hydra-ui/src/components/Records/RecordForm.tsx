import { FormikProps } from "formik";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { FormikField, FormikFieldDatePicker } from "../Shared/Form/FormikField";
import { ProjectSelect } from "./ProjectSelect";

export interface RecordFormData {
  project: number | undefined;
  start_time: Date | undefined;
  stop_time: Date | undefined;
}

type Props = {
  formik: FormikProps<RecordFormData>;
};

export const RecordForm: FC<Props> = ({ formik }) => {
  const { t } = useTranslation();
  return (
    <form
      data-testid="record_form"
      onSubmit={formik.handleSubmit}
      className="ant-form ant-form-vertical"
      id={"recordForm"}
    >
      <FormikField
        name="project"
        label={t("records.createDialog.projectLabel")}
      >
        {({ field }) => (
          <ProjectSelect
            value={field.value}
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
    </form>
  );
};
