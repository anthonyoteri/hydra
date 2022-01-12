import { Button, Modal } from "antd";
import { FC, ReactNode, useCallback, useEffect, useState } from "react";
import { connect, useDispatch } from "react-redux";
import { apiErrorMessage } from "../../api/errors";
import { fetchCategories } from "../../store/categories";
import { fetchProjects } from "../../store/projects";
import { fetchRecords } from "../../store/timeRecords";
import { fetchSettings } from "../../store/settings";

import Loading from "./Loading";

interface Props {
  children: ReactNode;
}

type InitializerState = "loading" | "complete" | "error";

export const Initializer: FC<Props> = (props) => {
  const { children } = props;
  const [state, setState] = useState<InitializerState>("loading");
  const [errorMessage, setErrorMessage] = useState("");
  const dispatch = useDispatch();

  const load = useCallback(() => {
    setState("loading");
    Promise.all([
      dispatch(fetchSettings()),
      dispatch(fetchCategories()),
      dispatch(fetchProjects()),
      dispatch(fetchRecords()),
    ])
      .then(() => {
        setState("complete");
      })
      .catch((err) => {
        setErrorMessage(apiErrorMessage(err));
        setState("error");
      });
  }, [dispatch]);

  useEffect(() => {
    load();
  }, [load]);

  if (state === "loading") {
    return <Loading message="Loading data..." data-testid="Init_loader" />;
  }

  if (state === "error") {
    const footer = (
      <>
        <Button type="primary" onClick={load}>
          Try again
        </Button>
      </>
    );

    return (
      <Modal visible={true} footer={footer} closable={false}>
        <h3>Error loading application data</h3>
        <span className="text-muted">{errorMessage}</span>
      </Modal>
    );
  }

  return <>{children}</>;
};

export default connect()(Initializer);
