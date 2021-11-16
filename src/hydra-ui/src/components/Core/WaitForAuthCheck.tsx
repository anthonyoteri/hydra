import { FC, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { useDispatch, useSelector } from "react-redux";
import { AuthStatus, checkAuth } from "../../store/auth";
import { ApplicationState } from "../../store/rootReducer";
import Loading from "./Loading";

export const WaitForAuthCheck: FC<{}> = ({ children }) => {
  const { t } = useTranslation();
  const dispatch = useDispatch();
  const { status: authStatus } = useSelector(
    (state: ApplicationState) => state.auth
  );

  useEffect(() => {
    if (authStatus === AuthStatus.WAITING) {
      dispatch(checkAuth());
    }
  }, [dispatch, authStatus]);

  if (authStatus === AuthStatus.WAITING || authStatus === AuthStatus.PENDING) {
    return <Loading message={t("common.authenticating")} />;
  }

  return <>{children}</>;
};
