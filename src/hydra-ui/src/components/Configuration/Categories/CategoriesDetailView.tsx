import { FC } from "react";
import { useSelector } from "react-redux";
import { useParams, Navigate } from "react-router-dom";
import { Project } from "../../../api/TimeReporting";
import { ApplicationState } from "../../../store/rootReducer";
import * as actions from "../../../store/projects";

import { ProjectsTable } from "./Projects/ProjectsTable";

export const CategoryDetailView: FC<{}> = () => {
  const { id } = useParams();
  const { byId } = useSelector((state: ApplicationState) => state.categories);
  const allProjects = useSelector(actions.selectAllProjects);

  if (id === undefined) {
    return <Navigate to="/categories" />;
  }

  const category = byId[+id];

  const projects = allProjects.filter(
    (value) => value.category === category.name
  );

  const handleDeleteProject = (project: Project) => {
    console.log(`Deleting project ${project.name}`);
  };

  return (
    <div className="category--details">
      <ProjectsTable projects={projects} onDelete={handleDeleteProject} />
    </div>
  );
};
