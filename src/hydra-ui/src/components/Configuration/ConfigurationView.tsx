import { FC, useEffect } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Category } from "../../api/TimeReporting";

import * as actions from "../../store/categories";

import { CategoriesTable } from "./Categories/CategoriesTable";
import { AppDispatch } from "../../store";
import { useTranslation } from "react-i18next";
import { message, Modal, notification } from "antd";

/* 
const emptyCategory = (): Category => {
  return {
    id: 0,
    name: "",
    description: "",
  };
};
*/

export const ConfigurationView: FC = () => {
  const categories = useSelector(actions.selectAllCategories);
  const dispatch = useDispatch<AppDispatch>();

  const { t } = useTranslation();

  useEffect(() => {
    dispatch(actions.fetchCategories());
  }, [dispatch]);

  const deleteCategory = (category: Category) => {
    const { confirm } = Modal;
    confirm({
      title: t("common.deleteConfirmation.title", {
        type: "Category",
        name: category.name,
      }),
      okText: t("common.delete"),
      content: t("common.deleteConfirmation.content"),
      async onOk() {
        try {
          await dispatch(actions.deleteCategory(category.id as number));
          message.success(
            t("common.deleteConfirmation.notification", {
              type: "Category",
              name: category.name,
            })
          );
        } catch (err: any) {
          notification.error({
            message: t("common.deleteConfirmation.failNotification", {
              type: "Category",
              name: category.name,
            }),
          });
        }
      },
    });
  };

  return (
    <>
      <CategoriesTable categories={categories} onDelete={deleteCategory} />
      <Outlet />
    </>
  );
};
