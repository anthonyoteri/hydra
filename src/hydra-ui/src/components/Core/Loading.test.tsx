import React from "react";
import { render, screen } from "@testing-library/react";
import Loading from "./Loading";

test("<Loading> renders without crashing", () => {
  render(<Loading />);
});
