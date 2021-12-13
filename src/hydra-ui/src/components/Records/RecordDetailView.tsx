import { FC } from "react";
import { useSelector } from "react-redux";
import { useParams, Navigate } from "react-router-dom";
import { ApplicationState } from "../../store/rootReducer";

export const RecordDetailView: FC<{}> = () => {
  const { id } = useParams();
  const { byId } = useSelector((state: ApplicationState) => state.records);

  if (id === undefined) {
    return <Navigate to="/records" />;
  }

  const record = byId[+id];
  if (record === undefined) {
    return <Navigate to="/records" />;
  }

  return (
    <div className="record--details">
      <span>This is record {record}</span>
    </div>
  );
};
