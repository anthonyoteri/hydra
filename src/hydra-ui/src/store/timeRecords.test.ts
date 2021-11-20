import timeRecordReducer, { fetchSuccess } from "./timeRecords";

describe("TimeRecord reducers", () => {
  it("should handle setting an initial state", () => {
    const reducer = timeRecordReducer(undefined, { type: "VOID" });
    expect(reducer).toEqual({
      byId: {},
      allIds: [],
    });
  });

  it("should handle setting a list of resources", () => {
    const reducer = timeRecordReducer(
      undefined,
      fetchSuccess([
        {
          id: 1,
          project: 1,
          start_time: new Date("2021-11-01T09:00:00-05:00"),
          stop_time: new Date("2021-11-01T11:00:00-05:00"),
          total_seconds: 7200,
        },
      ])
    );
    expect(reducer).toEqual({
      byId: {
        "1": {
          id: 1,
          project: 1,
          start_time: new Date("2021-11-01T09:00:00-05:00"),
          stop_time: new Date("2021-11-01T11:00:00-05:00"),
          total_seconds: 7200,
        },
      },
      allIds: [1],
    });
  });
});
