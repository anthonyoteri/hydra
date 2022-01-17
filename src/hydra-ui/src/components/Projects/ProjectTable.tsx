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
import { selectAllCategories } from "../../store/categories";
import { useSelector } from "react-redux";

type Props = {
  projects: Project[];
  onEdit: (project: Project) => void;
  onDelete: (project: Project) => void;
};

export const ProjectTable: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { projects, onEdit, onDelete } = props;
  const categories = useSelector(selectAllCategories);

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
          disabled={
            project.num_records && project.num_records >= 0 ? true : false
          }
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
      sorter: (a: Project, b: Project) => a.name.localeCompare(b.name),
    },
    {
      title: () => <>{t("projects.table.categoryLabel")}</>,
      className: "column--description",
      render: (value: any, project: Project, index: number) => {
        return (
          <span>{categories.find((c) => c.id === project.category)?.name}</span>
        );
      },
      sorter: (a: Project, b: Project) => {
        const aCategory =
          categories.find((c) => c.id === a.category)?.name || "";
        const bCategory =
          categories.find((c) => c.id === b.category)?.name || "";
        return aCategory.localeCompare(bCategory);
      },
    },
    {
      title: () => <>{t("projects.table.numRecordsLabel")}</>,
      className: "column--num-records",
      render: (value: any, project: Project, index: number) => {
        return <span>{project.num_records || t("projects.table.unused")}</span>;
      },
      sorter: (a: Project, b: Project) =>
        (a.num_records || 0) - (b?.num_records || 0),
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
