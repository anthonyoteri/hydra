import { FC } from "react";
import { useSelector } from "react-redux";
import { Navigate, useLocation, RouteProps, Outlet } from "react-router-dom";
import { AuthStatus } from "../../store/auth";
import { ApplicationState } from "../../store/rootReducer";

interface Props extends RouteProps {
  path: string;
}

const RequireAuth: FC<Props> = (props: Props) => {
  const { path } = props;
  const status = useSelector((state: ApplicationState) => state.auth);
  const location = useLocation();

  if (status.status !== AuthStatus.AUTHENTICATED) {
    return <Navigate to={path} state={{ from: location }} />;
  }

  return <Outlet />;
};

export default RequireAuth;
