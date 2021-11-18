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
import { Category } from "../../../api/TimeReporting";

type Props = {
  categories: Category[];
  onDelete: (category: Category) => void;
};

export const CategoriesTable: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { categories, onDelete } = props;

  const dropdown = (category: Category, index: number) => {
    return (
      <Menu>
        <Menu.Item
          key={`category_${index}_delete`}
          onClick={() => onDelete(category)}
          data-testid={`category_${index}_delete`}
        >
          <DeleteOutlined />
          {t("common.delete")}
        </Menu.Item>
      </Menu>
    );
  };

  const columns: ColumnProps<Category>[] = [
    {
      title: () => <>{t("configuration.categories.table.nameLabel")}</>,
      className: "column--title",
      render: (value: any, category: Category, index: number) => {
        return (
          <Link to={`category/${category.id}`} style={{ display: "block" }}>
            <span>{category.name}</span>
          </Link>
        );
      },
    },
    {
      title: () => <>{t("configuration.categories.table.descriptionLabel")}</>,
      className: "column--description",
      render: (value: any, category: Category, index: number) => {
        return <span>{category.description}</span>;
      },
    },
    {
      className: "column--actions",
      render: (value: any, category: Category, index: number) => {
        return (
          <Button.Group size="small">
            <Link to={`category/${category.id}`} className="ant-btn ant-btn-sm">
              {t("common.configure")} <ArrowRightOutlined />
            </Link>
            <Dropdown overlay={dropdown(category, index)} trigger={["click"]}>
              <Button
                data-testid={`category_${index}_dropdown`}
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
      dataSource={categories}
      rowKey={(category) => `${category.id}`}
      pagination={false}
    />
  );
};
