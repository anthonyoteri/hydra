import categoryReducer, { fetchSuccess } from "./categories";

describe("Category reducers", () => {
  it("should handle setting an initial state", () => {
    const reducer = categoryReducer(undefined, { type: "VOID" });
    expect(reducer).toEqual({
      byId: {},
      allIds: [],
    });
  });

  it("should handle setting a list of resources", () => {
    const reducer = categoryReducer(
      undefined,
      fetchSuccess([
        {
          id: 1,
          name: "Category 1",
          description: "A sample test category",
          created: new Date("2021-05-22T11:15:59-05:00"),
          updated: new Date("2021-06-01T00:00:00-00:00"),
        },
        {
          id: 2,
          name: "Category 2",
          description: "Another sample test category",
          created: new Date("2021-05-22T11:16:59-05:00"),
          updated: new Date("2021-05-22T11:16:59-05:00"),
        },
      ])
    );
    expect(reducer).toEqual({
      byId: {
        "1": {
          id: 1,
          name: "Category 1",
          description: "A sample test category",
          created: new Date("2021-05-22T11:15:59-05:00"),
          updated: new Date("2021-06-01T00:00:00-00:00"),
        },
        "2": {
          id: 2,
          name: "Category 2",
          description: "Another sample test category",
          created: new Date("2021-05-22T11:16:59-05:00"),
          updated: new Date("2021-05-22T11:16:59-05:00"),
        },
      },
      allIds: [1, 2],
    });
  });
});
