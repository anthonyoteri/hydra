import {
  CheckCircleOutlined,
  CloseCircleOutlined,
  DeleteOutlined,
  EditOutlined,
  EllipsisOutlined,
  PauseOutlined,
  PlayCircleOutlined,
  WarningOutlined,
} from "@ant-design/icons";
import { ColumnProps } from "antd/lib/table";
import { Table, Menu, Button, Dropdown } from "antd";
import { FC } from "react";
import { useTranslation } from "react-i18next";
import { TimeRecord } from "../../api/TimeReporting";
import { CategoryProject } from "../Projects/CategoryProject";

import moment from "moment";

type Props = {
  records: TimeRecord[];
  onEdit: (record: TimeRecord) => void;
  toggleApproved: (record: TimeRecord) => void;
  onDelete: (record: TimeRecord) => void;
  onStart: (record: TimeRecord) => void;
  onStop: (record: TimeRecord) => void;
};

export const RecordTable: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { records, onEdit, toggleApproved, onDelete, onStart, onStop } = props;

  const dropdown = (record: TimeRecord, index: number) => {
    return (
      <Menu>
        {record.stop_time && (
          <Menu.Item
            key={`record_${index}_start`}
            onClick={() => onStart(record)}
            data-testid={`record_${index}_start`}
          >
            <PlayCircleOutlined />
            {t("common.start")}
          </Menu.Item>
        )}

        {!record.stop_time && (
          <Menu.Item
            key={`record_${index}_stop`}
            onClick={() => onStop(record)}
            data-testid={`record_${index}_stop`}
          >
            <PauseOutlined />
            {t("common.stop")}
          </Menu.Item>
        )}
        <Menu.Item
          key={`record_${index}_edit`}
          onClick={() => onEdit(record)}
          data-testid={`record_${index}_edit`}
        >
          <EditOutlined />
          {t("common.edit")}
        </Menu.Item>
        {moment(record.start_time) <= moment() && (
          <Menu.Item
            key={`record_${index}_approve`}
            onClick={() => toggleApproved(record)}
            data-testid={`record_${index}_approve`}
          >
            {(record?.approved && (
              <>
                <CloseCircleOutlined />
                {t("records.declineAction")}
              </>
            )) || (
              <>
                <CheckCircleOutlined />
                {t("records.approveAction")}
              </>
            )}
          </Menu.Item>
        )}

        <Menu.Item
          key={`record_${index}_delete`}
          onClick={() => onDelete(record)}
          data-testid={`record_${index}_delete`}
        >
          <DeleteOutlined />
          {t("common.delete")}
        </Menu.Item>
      </Menu>
    );
  };

  const columns: ColumnProps<TimeRecord>[] = [
    {
      title: () => <>{t("records.table.dateLabel")}</>,
      className: "column--description",
      render: (value: any, record: TimeRecord, index: number) => {
        return <span>{moment(record.start_time).format("LL")}</span>;
      },
      sorter: (a, b) => moment(a.start_time).diff(moment(b.start_time)),
      defaultSortOrder: "descend",
    },
    {
      title: () => <>{t("records.table.projectLabel")}</>,
      className: "column--title",
      render: (value: any, record: TimeRecord, index: number) => {
        return <CategoryProject pid={record.project} />;
      },
    },
    {
      title: () => <>{t("records.table.startTimeLabel")}</>,
      className: "column--description",
      render: (value: any, record: TimeRecord, index: number) => {
        return <span>{moment(record.start_time).format("LT")}</span>;
      },
    },
    {
      title: () => <>{t("records.table.stopTimeLabel")}</>,
      className: "column--description",
      render: (value: any, record: TimeRecord, index: number) => {
        return (
          <span>
            {record.stop_time ? moment(record.stop_time).format("LT") : ""}
          </span>
        );
      },
    },
    {
      title: () => <>{t("records.table.durationLabel")}</>,
      className: "column--description",
      render: (value: any, record: TimeRecord, index: number) => {
        return (
          <span>
            {record.stop_time
              ? moment.duration(record.total_seconds, "seconds").humanize()
              : moment(record.start_time) <= moment()
              ? moment(record.start_time).fromNow(true)
              : null}
          </span>
        );
      },
    },
    {
      className: "column--actions",
      render: (value: any, record: TimeRecord, index: number) => {
        return (
          <Button.Group size="small">
            <Dropdown overlay={dropdown(record, index)} trigger={["click"]}>
              <Button
                data-testid={`record_${index}_dropdown`}
                icon={
                  !record.approved && moment(record.start_time) <= moment() ? (
                    <WarningOutlined />
                  ) : (
                    <EllipsisOutlined />
                  )
                }
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
      dataSource={records}
      rowKey={(record) => `${record.id}`}
      rowClassName={(record, index) => {
        if (!record?.approved) {
          return "row--disabled";
        }
        if (!record.stop_time) {
          return "record-table-row-current";
        }
        return "record-table-row";
      }}
    />
  );
};
