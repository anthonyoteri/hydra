import { FC } from "react";

import { useSelector } from "react-redux";
import { selectAllProjects } from "../../store/projects";
import { selectAllCategories } from "../../store/categories";

export type Props = {
  pid: number;
};

export const CategoryProject: FC<Props> = (props) => {
  const { pid } = props;
  const categories = useSelector(selectAllCategories);
  const projects = useSelector(selectAllProjects);

  const project = projects.find((p) => p.id === pid);
  const category = categories.find((c) => c.id === project?.category);

  return (
    <span>
      {project?.name} ({category?.name})
    </span>
  );
};
