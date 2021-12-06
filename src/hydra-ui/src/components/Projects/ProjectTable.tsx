import {
  DeleteOutlined,
  EditOutlined,
  EllipsisOutlined,
} from "@ant-design/icons";
import { ColumnProps } from "antd/lib/table";
import { Table, Menu, Button, Dropdown } from "antd";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { Project } from "../../api/TimeReporting";

type Props = {
  projects: Project[];
  onEdit: (project: Project) => void;
  onDelete: (project: Project) => void;
};

export const ProjectTable: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { projects, onEdit, onDelete } = props;

  const dropdown = (project: Project, index: number) => {
    return (
      <Menu>
        <Menu.Item
          key={`project_${index}_edit`}
          onClick={() => onEdit(project)}
          data-testid={`project_${index}_edit`}
        >
          <EditOutlined />
          {t("common.edit")}
        </Menu.Item>
        <Menu.Item
          key={`project_${index}_delete`}
          onClick={() => onDelete(project)}
          data-testid={`project_${index}_delete`}
        >
          <DeleteOutlined />
          {t("common.delete")}
        </Menu.Item>
      </Menu>
    );
  };

  const columns: ColumnProps<Project>[] = [
    {
      title: () => <>{t("projects.table.nameLabel")}</>,
      className: "column--title",
      render: (value: any, project: Project, index: number) => {
        return (
          <Link to={`${project.id}`} style={{ display: "block" }}>
            <span>{project.name}</span>
          </Link>
        );
      },
    },
    {
      title: () => <>{t("projects.table.descriptionLabel")}</>,
      className: "column--description",
      render: (value: any, project: Project, index: number) => {
        return <span>{project.description}</span>;
      },
    },
    {
      className: "column--actions",
      render: (value: any, project: Project, index: number) => {
        return (
          <Button.Group size="small">
            <Dropdown overlay={dropdown(project, index)} trigger={["click"]}>
              <Button
                data-testid={`project_${index}_dropdown`}
                icon={<EllipsisOutlined />}
                size="small"
              />
            </Dropdown>
          </Button.Group>
        );
      },
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={projects}
      rowKey={(project) => `${project.id}`}
      pagination={false}
    />
  );
};
