import moment from "moment";
import { TimeRecord } from "../../api/TimeReporting";

export const dateRange = (year: number, week: number) => {
  let days = [];
  const range_begin = moment().isoWeekYear(year).isoWeek(week).startOf("week");
  const range_end = range_begin.clone().add(1, "week");
  for (var m = range_begin; m.isBefore(range_end); m.add(1, "days")) {
    days.push(m.clone());
  }
  return days;
};

export const recordsForDay = (records: TimeRecord[], target: moment.Moment) => {
  return records.filter((r) =>
    moment(r.start_time).isBetween(
      target.clone().startOf("day"),
      target.clone().endOf("day")
    )
  );
};

export const recordsForWeek = (
  records: TimeRecord[],
  target: moment.Moment
) => {
  return records.filter((r) =>
    moment(r.start_time).isBetween(
      target.clone().startOf("week"),
      target.clone().endOf("week")
    )
  );
};

export const recordsForMonth = (
  records: TimeRecord[],
  target: moment.Moment
) => {
  return records.filter((r) =>
    moment(r.start_time).isBetween(
      target.clone().startOf("month"),
      target.clone().endOf("month")
    )
  );
};

export const aggregate = (records: TimeRecord[]) => {
  return records.reduce((agg, current) => {
    const o: any = { ...agg };
    const duration = current.total_seconds;

    if (!duration) {
      return o;
    }

    /* Skip unapproved records */
    if (!current?.approved) {
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

export const summarize = (records: TimeRecord[], days: moment.Moment[]) => {
  const data: { [key: string]: number }[] = days.map((d) =>
    aggregate(recordsForDay(records, d))
  );
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

export const totalTime = (records: TimeRecord[]) => {
  return (
    records?.reduce(
      (total, record) => (total += record.total_seconds || 0),
      0
    ) || 0
  );
};
