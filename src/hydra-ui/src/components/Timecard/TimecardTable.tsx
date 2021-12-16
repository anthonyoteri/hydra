import { Table } from "antd";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { useSelector } from "react-redux";
import { selectAllCategories } from "../../store/categories";
import { selectAllProjects } from "../../store/projects";
import moment from "moment";
import { ColumnProps } from "antd/lib/table";

export interface RecordType {
  projectName: string;
  categoryName: string;
}

type Props = {
  days: moment.Moment[];
  dataSource: any;
};

export const TimecardTable: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { days, dataSource } = props;
  const categories = useSelector(selectAllCategories);
  const projects = useSelector(selectAllProjects);

  const joinProjectCategory = (data: { [key: string]: number }[]) => {
    return data.map((row) => {
      const project = projects.find((p) => p.id === row.project);
      const category = categories.find((c) => c.id === project?.category);
      return {
        ...row,
        projectName: project?.name || "",
        categoryName: category?.name || "",
      };
    });
  };

  const columns: ColumnProps<RecordType>[] = [
    {
      title: () => <>{t("timecards.categoryLabel")}</>,
      className: "column--title",
      dataIndex: "categoryName",
      render: (category: string) => <span>{category}</span>,
      sorter: (a: RecordType, b: RecordType) =>
        a.categoryName.localeCompare(b.categoryName),
      defaultSortOrder: "ascend",
    },
    {
      title: () => <>{t("timecards.projectLabel")}</>,
      className: "column--title",
      dataIndex: "projectName",
      render: (project: string) => <span>{project}</span>,
      sorter: (a: RecordType, b: RecordType) =>
        a.projectName.localeCompare(b.projectName),
      defaultSortOrder: "ascend",
    },
    ...days.map((d) => ({
      key: d.unix(),
      title: d.format("dddd"),
      dataIndex: d.format("YYYY-MM-DD"),
      render: (totalSeconds: number) =>
        totalSeconds
          ? moment.duration(totalSeconds, "seconds").humanize()
          : null,
    })),
  ];

  return (
    <Table
      columns={columns}
      dataSource={joinProjectCategory(dataSource)}
      rowKey={(r) => `${r.categoryName}_${r.projectName}`}
      pagination={false}
    />
  );
};
