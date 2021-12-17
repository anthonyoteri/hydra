import { FC, useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Outlet } from "react-router-dom";
import { AppDispatch } from "../../store";
import * as actions from "../../store/timeRecords";
import { selectAllRecords } from "../../store/timeRecords";
import { TimecardTable } from "./TimecardTable";
import moment from "moment";
import { Layout } from "antd";
import { TimecardViewToolbar } from "./TimecardViewToolbar";
import { MainHeader } from "../Shared/MainHeader/MainHeader";
import { useTranslation } from "react-i18next";
import { dateRange, recordsForWeek, summarize, totalTime } from "./helpers";

export const TimecardView: FC = () => {
  const { t } = useTranslation();

  const dispatch = useDispatch<AppDispatch>();
  const records = useSelector(selectAllRecords);

  const [target, setTarget] = useState<moment.Moment>(moment());

  useEffect(() => {
    dispatch(actions.fetchRecords());
  }, [dispatch]);

  const todayClicked = () => {
    setTarget(moment());
  };

  const nextClicked = () => {
    setTarget(target.clone().add(1, "week"));
  };

  const previousClicked = () => {
    setTarget(target.clone().subtract(1, "week"));
  };

  return (
    <Layout.Content>
      <MainHeader title={t("navigation.timecards")} />
      <TimecardViewToolbar
        onNext={nextClicked}
        onToday={todayClicked}
        onPrevious={previousClicked}
      />
      <TimecardTable
        weekNumber={target.isoWeek()}
        days={dateRange(target.isoWeekYear(), target.isoWeek())}
        dataSource={summarize(
          recordsForWeek(records, target),
          dateRange(target.isoWeekYear(), target.isoWeek())
        )}
        totalSeconds={totalTime(recordsForWeek(records, target))}
      />
      <Outlet />
    </Layout.Content>
  );
};
