import React from "react";
import { Button, Result } from "antd";

interface Props {}

interface State {
  hasError: boolean;
  eventId?: string;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <Result
          status="error"
          title="Error"
          subTitle="Sorry, something went wrong..."
          extra={
            <>
              <Button onClick={() => window.location.reload()}>
                Reload page
              </Button>
            </>
          }
        />
      );
    }

    return this.props.children;
  }
}
