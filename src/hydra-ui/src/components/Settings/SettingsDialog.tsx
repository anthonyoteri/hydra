import { FC, useState } from "react";
import { Formik } from "formik";
import { useSelector, useDispatch } from "react-redux";
import { useTranslation } from "react-i18next";
import { message, notification } from "antd";
import * as actions from "../../store/settings";
import { Settings } from "../../api/Settings";
import { selectSettings } from "../../store/settings";
import { SettingsForm } from "./SettingsForm";
import { AppDispatch } from "../../store";

interface Props {
  hideAdvanced: boolean;
}

export const SettingsDialog: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const dispatch = useDispatch<AppDispatch>();
  const { hideAdvanced } = props;

  const [isLoading, setIsLoading] = useState(false);

  const activeSettings = useSelector(selectSettings);

  const handleSubmit = async (values: Settings) => {
    setIsLoading(true);
    message.loading({
      content: t("settings.saveProgressNotification"),
      key: "save",
      duration: 0,
    });
    try {
      await dispatch(actions.saveSettings(values));
      message.success({
        content: t("settings.saveSuccessNotification"),
        key: "save",
      });
    } catch (err) {
      notification.error({
        message: t("settings.saveFailNotification"),
        key: "save",
      });
    }
    setIsLoading(false);
  };

  return (
    <Formik initialValues={activeSettings} onSubmit={handleSubmit}>
      {(props) => (
        <SettingsForm
          formik={props}
          isLoading={isLoading}
          hideAdvanced={hideAdvanced}
        />
      )}
    </Formik>
  );
};
