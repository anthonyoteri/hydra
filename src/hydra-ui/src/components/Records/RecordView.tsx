import { FC, useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { TimeRecord, TimeRecordDraft } from "../../api/TimeReporting";

import * as actions from "../../store/timeRecords";

import { RecordTable } from "./RecordTable";
import { AppDispatch } from "../../store";
import { useTranslation } from "react-i18next";
import { Layout, message, Modal, notification } from "antd";
import { MainHeader } from "../Shared/MainHeader/MainHeader";
import { RecordViewToolbar } from "./RecordViewToolbar";
import { RecordDialog } from "./RecordDialog";

const emptyRecord = (): TimeRecordDraft => {
  return {
    project: 0,
    start_time: undefined,
    stop_time: undefined,
  };
};

export const RecordView: FC = () => {
  const records = useSelector(actions.selectAllRecords);
  const dispatch = useDispatch<AppDispatch>();
  const { t } = useTranslation();
  const [addModalOpen, setAddModalOpen] = useState<boolean>(false);
  const [editModalOpen, setEditModalOpen] = useState<boolean>(false);
  const [editingRecord, setEditingRecord] = useState<TimeRecord | undefined>(
    undefined
  );

  useEffect(() => {
    dispatch(actions.fetchRecords());
  }, [dispatch]);

  const createRecord = async (record: TimeRecord) => {
    await dispatch(actions.createRecord(record));
    return Promise.resolve();
  };

  const closeUpdateModal = () => {
    setEditModalOpen(false);
    setEditingRecord(undefined);
  };

  const closeAddModal = () => {
    setAddModalOpen(false);
  };

  const onCreateComplete = () => {
    setAddModalOpen(false);
    message.success(t("records.createSuccessNotification"));
  };

  const onUpdateComplete = () => {
    setEditModalOpen(false);
    message.success(t("records.updateSuccessNotification"));
  };

  const updateRecord = (record: TimeRecord) => {
    return dispatch(actions.patchRecord(editingRecord!.id, record));
  };

  const handleEdit = (record: TimeRecord) => {
    setEditingRecord(record);
    setEditModalOpen(true);
  };

  const deleteRecord = (record: TimeRecord) => {
    const { confirm } = Modal;
    confirm({
      title: t("common.deleteConfirmation.title", {
        type: "Record",
        name: record.id,
      }),
      okText: t("common.delete"),
      content: t("common.deleteConfirmation.content"),
      async onOk() {
        try {
          await dispatch(actions.deleteRecord(record.id as number));
          message.success(
            t("common.deleteConfirmation.notification", {
              type: "Record",
              name: record.project,
            })
          );
        } catch (err: any) {
          notification.error({
            message: t("common.deleteConfirmation.failNotification", {
              type: "Record",
              name: record.project,
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
        <RecordDialog
          type="create"
          record={emptyRecord()}
          onOk={createRecord}
          onComplete={onCreateComplete}
          onCancel={closeAddModal}
        />
      )}

      {editModalOpen && (
        <RecordDialog
          type="update"
          record={editingRecord!}
          onOk={updateRecord}
          onComplete={onUpdateComplete}
          onCancel={closeUpdateModal}
        />
      )}

      <MainHeader title={t("navigation.records")} />
      <RecordViewToolbar onAddClick={openAddModal} />
      <RecordTable
        records={records}
        onEdit={handleEdit}
        onDelete={deleteRecord}
      />
      <Outlet />
    </Layout.Content>
  );
};
