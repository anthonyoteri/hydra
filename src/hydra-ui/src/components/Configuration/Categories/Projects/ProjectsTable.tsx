import {
  ArrowRightOutlined,
  DeleteOutlined,
  EllipsisOutlined,
} from "@ant-design/icons";
import { ColumnProps } from "antd/lib/table";
import { Table, Menu, Button, Dropdown } from "antd";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { Project } from "../../../../api/TimeReporting";

type Props = {
  projects: Project[];
  onDelete: (project: Project) => void;
};

export const ProjectsTable: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { projects, onDelete } = props;

  const dropdown = (project: Project, index: number) => {
    return (
      <Menu>
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
      title: () => (
        <>{t("configuration.categories.projects.table.nameLabel")}</>
      ),
      className: "column--title",
      render: (value: any, project: Project, index: number) => {
        return (
          <Link to={`project/${project.id}`} style={{ display: "block" }}>
            <span>{project.name}</span>
          </Link>
        );
      },
    },
    {
      title: () => (
        <>{t("configuration.categories.projects.table.descriptionLabel")}</>
      ),
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
            <Link to={`project/${project.id}`} className="ant-btn ant-btn-sm">
              {t("common.configure")} <ArrowRightOutlined />
            </Link>
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
