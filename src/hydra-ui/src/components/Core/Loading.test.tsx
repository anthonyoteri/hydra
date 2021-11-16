import { render } from "@testing-library/react";
import Loading from "./Loading";

test("<Loading> renders without crashing", () => {
  render(<Loading />);
});
