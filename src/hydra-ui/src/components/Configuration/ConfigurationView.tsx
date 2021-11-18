import { FC } from "react";
import { Outlet } from "react-router-dom";
import { useSelector } from "react-redux";
import { Category } from "../../api/TimeReporting";

import * as actions from "../../store/categories";

import { CategoriesTable } from "./Categories/CategoriesTable";

export const ConfigurationView: FC = () => {
  const categories = useSelector(actions.selectAllCategories);

  const handleDeleteCategory = (category: Category) => {
    console.log(`Deleting category ${category.name}`);
  };

  return (
    <>
      <CategoriesTable
        categories={categories}
        onDelete={handleDeleteCategory}
      />
      <Outlet />
    </>
  );
};
