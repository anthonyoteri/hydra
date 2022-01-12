import { FormikProps } from "formik";
import { FC } from "react";
import { Button, Card } from "antd";
import { SaveOutlined } from "@ant-design/icons";

import { useTranslation } from "react-i18next";
import {
  FormikFieldCheckbox,
  FormikFieldInputNumber,
} from "../Shared/Form/FormikField";
import { CardHeader } from "../Shared/CardHeader";

export interface SettingsFormData {
  retention_period_days?: number;
  align_timestamps?: boolean;
}

type Props = {
  formik: FormikProps<SettingsFormData>;
  isLoading: boolean;
  hideAdvanced: boolean;
};

export const SettingsForm: FC<Props> = (props: Props) => {
  const { t } = useTranslation();

  const { formik, isLoading, hideAdvanced } = props;

  return (
    <form
      data-testid="settings_form"
      onSubmit={formik.handleSubmit}
      className="ant-form ant-form-vertical"
      id={"settingsForm"}
    >
      <fieldset style={{ marginBottom: 0 }}>
        <Card
          className="settings-card"
          bordered={true}
          title={
            <CardHeader
              title={t("settings.dialog.general.title")}
              description={t("settings.dialog.general.description")}
            />
          }
        >
          <FormikFieldInputNumber
            name="retention_period_days"
            label={t("settings.dialog.retentionPeriodDaysLabel")}
          />
        </Card>

        {!hideAdvanced && (
          <Card
            className="settings-card"
            bordered={true}
            title={
              <CardHeader
                title={t("settings.dialog.advanced.title")}
                description={t("settings.dialog.advanced.description")}
              />
            }
          >
            <FormikFieldCheckbox name="align_timestamps">
              {t("settings.dialog.alignTimestampsLabel")}
            </FormikFieldCheckbox>
          </Card>
        )}
      </fieldset>

      <Button type="primary" htmlType="submit" loading={isLoading}>
        <SaveOutlined /> {t("settings.saveButton")}
      </Button>
    </form>
  );
};
