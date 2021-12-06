import { FC, useEffect, useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Project, ProjectDraft } from "../../api/TimeReporting";

import * as actions from "../../store/projects";

import { ProjectTable } from "./ProjectTable";
import { AppDispatch } from "../../store";
import { useTranslation } from "react-i18next";
import { Layout, message, Modal, notification } from "antd";
import { MainHeader } from "../Shared/MainHeader/MainHeader";
import { ProjectViewToolbar } from "./ProjectViewToolbar";
import { ProjectDialog } from "./ProjectDialog";

const emptyProject = (): ProjectDraft => {
  return {
    category: 0,
    name: "",
    description: "",
  };
};

export const ProjectView: FC = () => {
  const projects = useSelector(actions.selectAllProjects);
  const dispatch = useDispatch<AppDispatch>();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [addModalOpen, setAddModalOpen] = useState<boolean>(false);
  const [editModalOpen, setEditModalOpen] = useState<boolean>(false);
  const [editingProject, setEditingProject] = useState<Project | undefined>(
    undefined
  );
  const [redirectProject, setRedirectProject] = useState<number | null>(null);

  useEffect(() => {
    dispatch(actions.fetchProjects());
  }, [dispatch]);

  const createProject = async (project: Project) => {
    const newProject = await dispatch(actions.createProject(project));
    setRedirectProject(newProject.id);
    return Promise.resolve();
  };

  const closeUpdateModal = () => {
    setEditModalOpen(false);
    setEditingProject(undefined);
  };

  const closeAddModal = () => {
    setAddModalOpen(false);
  };

  const onCreateComplete = () => {
    setAddModalOpen(false);
    message.success(t("projects.createSuccessNotification"));
    if (redirectProject) {
      navigate(`./${redirectProject}`);
    }
  };

  const onUpdateComplete = () => {
    setEditModalOpen(false);
    setEditingProject(undefined);
    message.success(t("projects.updateSuccessNotification"));
    if (redirectProject) {
      navigate(`./${redirectProject}`);
    }
  };

  const updateProject = (project: Project) => {
    return dispatch(actions.patchProject(editingProject!.id, project));
  };

  const handleEdit = (project: Project) => {
    setEditingProject(project);
    setEditModalOpen(true);
  };

  const deleteProject = (project: Project) => {
    const { confirm } = Modal;
    confirm({
      title: t("common.deleteConfirmation.title", {
        type: "Project",
        name: project.name,
      }),
      okText: t("common.delete"),
      content: t("common.deleteConfirmation.content"),
      async onOk() {
        try {
          await dispatch(actions.deleteProject(project.id as number));
          message.success(
            t("common.deleteConfirmation.notification", {
              type: "Project",
              name: project.name,
            })
          );
        } catch (err: any) {
          notification.error({
            message: t("common.deleteConfirmation.failNotification", {
              type: "Project",
              name: project.name,
            }),
          });
        }
      },
    });
  };

  const openAddModal = () => {
    setAddModalOpen(true);
  };

  return (
    <Layout.Content>
      {addModalOpen && (
        <ProjectDialog
          type="create"
          project={emptyProject()}
          onOk={createProject}
          onComplete={onCreateComplete}
          onCancel={closeAddModal}
        />
      )}

      {editModalOpen && (
        <ProjectDialog
          type="update"
          project={editingProject!}
          onOk={updateProject}
          onComplete={onUpdateComplete}
          onCancel={closeUpdateModal}
        />
      )}

      <MainHeader title={t("navigation.projects")} />
      <ProjectViewToolbar onAddClick={openAddModal} />
      <ProjectTable
        projects={projects}
        onEdit={handleEdit}
        onDelete={deleteProject}
      />
      <Outlet />
    </Layout.Content>
  );
};
