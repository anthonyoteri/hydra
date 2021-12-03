import { FC, useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Category, CategoryDraft } from "../../api/TimeReporting";

import * as actions from "../../store/categories";

import { CategoriesTable } from "./Categories/CategoriesTable";
import { AppDispatch } from "../../store";
import { useTranslation } from "react-i18next";
import { Layout, message, Modal, notification } from "antd";
import { MainHeader } from "../Shared/MainHeader/MainHeader";
import { ConfigurationPageToolbar } from "./ConfigurationPageToolbar";
import { CategoryDialog } from "./Categories/CategoryDialog";

const emptyCategory = (): CategoryDraft => {
  return {
    name: "",
    description: "",
  };
};

export const ConfigurationView: FC = () => {
  const categories = useSelector(actions.selectAllCategories);
  const dispatch = useDispatch<AppDispatch>();
  const { t } = useTranslation();
  const [addModalOpen, setAddModalOpen] = useState<boolean>(false);
  const [editModalOpen, setEditModalOpen] = useState<boolean>(false);
  const [editingCategory, setEditingCategory] = useState<Category | undefined>(
    undefined
  );
  const [createComplete, setCreatedCompleted] = useState(false);
  const [redirectCategory, setRedirectCategory] = useState<number | null>(null);

  useEffect(() => {
    dispatch(actions.fetchCategories());
  }, [dispatch]);

  const createCategory = async (category: Category) => {
    const newCategory = await dispatch(actions.createCategory(category));
    setRedirectCategory(newCategory.id);
    return Promise.resolve();
  };

  const closeUpdateModal = () => {
    setEditModalOpen(false);
    setEditingCategory(undefined);
  };

  const closeAddModal = () => {
    setAddModalOpen(false);
  };

  const onCreateComplete = () => {
    setAddModalOpen(false);
    message.success(t("configuration.categories.createSuccessNotification"));
    setCreatedCompleted(true);
  };

  const onUpdateComplete = () => {
    setEditModalOpen(false);
    setEditingCategory(undefined);
    message.success(t("configuration.categories.updateSuccessNotification"));
  };

  const updateCategory = (category: Category) => {
    return dispatch(actions.patchCategory(editingCategory!.id, category));
  };

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

  const openAddModal = () => {
    setAddModalOpen(true);
  };

  if (redirectCategory && createComplete)
    return <Navigate to={`/configuration/category/${redirectCategory}`} />;

  return (
    <Layout.Content>
      {addModalOpen && (
        <CategoryDialog
          type="create"
          category={emptyCategory()}
          onOk={createCategory}
          onComplete={onCreateComplete}
          onCancel={closeAddModal}
        />
      )}

      {editModalOpen && (
        <CategoryDialog
          type="update"
          category={editingCategory!}
          onOk={updateCategory}
          onComplete={onUpdateComplete}
          onCancel={closeUpdateModal}
        />
      )}

      <MainHeader title={t("navigation.configuration")} />
      <ConfigurationPageToolbar onAddClick={openAddModal} />
      <CategoriesTable categories={categories} onDelete={deleteCategory} />
      <Outlet />
    </Layout.Content>
  );
};
