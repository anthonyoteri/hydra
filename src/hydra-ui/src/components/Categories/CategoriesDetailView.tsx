import { FC } from "react";
import { useSelector } from "react-redux";
import { useParams, Navigate } from "react-router-dom";
import { ApplicationState } from "../../store/rootReducer";

export const CategoryDetailView: FC<{}> = () => {
  const { id } = useParams();
  const { byId } = useSelector((state: ApplicationState) => state.categories);

  if (id === undefined) {
    return <Navigate to="/categories" />;
  }

  const category = byId[+id];

  if (category === undefined) {
    return <Navigate to="/categories" />;
  }

  return (
    <div className="category--details">
      <h1>Project for category {category.name}</h1>
    </div>
  );
};
