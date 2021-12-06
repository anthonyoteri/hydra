import { FC } from "react";
import { useSelector } from "react-redux";
import { useParams, Navigate } from "react-router-dom";
import { ApplicationState } from "../../store/rootReducer";

export const ProjectDetailView: FC<{}> = () => {
  const { id } = useParams();
  const { byId } = useSelector((state: ApplicationState) => state.projects);

  if (id === undefined) {
    return <Navigate to="/projects" />;
  }

  const project = byId[+id];
  if (project === undefined) {
    return <Navigate to="/projects" />;
  }

  return (
    <div className="project--details">
      <span>This is project {project.name}</span>
    </div>
  );
};
