import { Alert, Button } from "antd";
import Password from "antd/lib/input/Password";
import { Formik, FormikErrors } from "formik";
import { FC, useState } from "react";
import { useTranslation } from "react-i18next";
import { useDispatch, useSelector } from "react-redux";
import { Navigate } from "react-router";
import { ApiError, apiErrorMessage } from "../../api/errors";
import { AppDispatch } from "../../store";
import { attemptLogin, AuthStatus } from "../../store/auth";
import { ApplicationState } from "../../store/rootReducer";
import { AppVersion } from "../Core/AppVersion";
import { FormikField, FormikFieldInput } from "../Shared/Form/FormikField";

interface LoginProps {}

interface LoginFormData {
  username: string;
  password: string;
}

export const Login: FC<LoginProps> = () => {
  const { t } = useTranslation();
  const dispatch = useDispatch<AppDispatch>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const { status, returnUrl } = useSelector(
    (state: ApplicationState) => state.auth
  );

  const handleSubmit = async (values: LoginFormData) => {
    const { username, password } = values;
    setError(null);
    setIsLoading(true);
    try {
      await dispatch(attemptLogin(username, password));
    } catch (err: any) {
      setError(err);
      setIsLoading(false);
    }
  };

  switch (status) {
    case AuthStatus.AUTHENTICATED:
      return <Navigate to={returnUrl || "/"} />;
  }

  return (
    <div className="login-container">
      <div className="login-logo">
        <p>Logo goes here</p>
      </div>
      <div className="login-box">
        <Formik
          initialValues={{
            username: "",
            password: "",
          }}
          validateOnBlur={false}
          onSubmit={handleSubmit}
          validate={(values) => {
            const errors: FormikErrors<LoginFormData> = {};
            if (!values.username) {
              errors.username = "login.errors.usernameRequired";
            }

            if (!values.password) {
              errors.password = "login.errors.passwordRequired";
            }

            return errors;
          }}
        >
          {(props) => (
            <form
              className="ant-form ant-form-vertical"
              onSubmit={props.handleSubmit}
              data-testid="login_form"
            >
              <FormikFieldInput
                name="username"
                label={t("login.usernameLabel")}
                autoFocus
              />

              <FormikField name="password" label={t("login.passwordLabel")}>
                {({ field }) => (
                  <Password
                    value={field.value}
                    onChange={field.onChange}
                    name="password"
                    id="password"
                  />
                )}
              </FormikField>

              <Button
                type="primary"
                htmlType="submit"
                loading={isLoading}
                block={true}
              >
                {t("login.loginButton")}
              </Button>
            </form>
          )}
        </Formik>
      </div>
      {error && <Alert type="error" message={apiErrorMessage(error)} />}
      <AppVersion />
    </div>
  );
};
