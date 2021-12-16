import { FC, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Outlet } from "react-router-dom";
import { AppDispatch } from "../../store";
import * as actions from "../../store/timeRecords";
import { selectRecordsForWeek } from "../../store/timeRecords";
import { TimecardTable } from "./TimecardTable";
import { ApplicationState } from "../../store/rootReducer";
import moment from "moment";
import { Layout } from "antd";

export const TimecardView: FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const year = moment().isoWeekYear();
  const week = moment().isoWeek();
  const records = useSelector((state: ApplicationState) =>
    selectRecordsForWeek(state, week)
  ).filter((r) => moment(r.start_time).isoWeekYear() === year);

  useEffect(() => {
    dispatch(actions.fetchRecords());
  }, [dispatch]);

  const daysInRange = (week: number) => {
    let days = [];
    const range_begin = moment().isoWeek(week).startOf("week");
    const range_end = range_begin.clone().add(1, "week");
    for (var m = range_begin; m.isBefore(range_end); m.add(1, "days")) {
      days.push(m.clone());
    }
    return days;
  };

  const recordsForDay = (day: moment.Moment) => {
    return records.filter(
      (r) => moment(r.start_time).dayOfYear() === day.dayOfYear()
    );
  };

  const aggregate = (day: moment.Moment) => {
    return recordsForDay(day)?.reduce((agg, current) => {
      const o: any = { ...agg };
      const duration = current.total_seconds;

      if (!duration) {
        return o;
      }

      if (o[current.project]) {
        o[current.project] += duration;
      } else {
        o[current.project] = duration;
      }
      return o;
    }, {});
  };

  const recordsForWeek = (week: number) => {
    const days = daysInRange(week);
    const data: { [key: string]: number }[] = days.map((d) => aggregate(d));
    const result: { [key: string]: { [key: string]: number } } = {};

    for (var i = 0; i < days.length; i++) {
      let d = days[i];
      for (var p of Object.keys(data[i])) {
        if (result.hasOwnProperty(p)) {
          result[p][d.format("YYYY-MM-DD")] = data[i][p];
        } else {
          result[p] = { [d.format("YYYY-MM-DD")]: data[i][p] };
        }
      }
    }

    return Object.keys(result).map((k) => {
      return { ...result[k], project: Number.parseInt(k) };
    });
  };

  return (
    <Layout.Content>
      <TimecardTable
        days={daysInRange(week)}
        dataSource={recordsForWeek(week)}
      />
      <Outlet />
    </Layout.Content>
  );
};
