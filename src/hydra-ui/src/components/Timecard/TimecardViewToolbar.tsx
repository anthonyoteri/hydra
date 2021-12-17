import {
  CalendarOutlined,
  StepBackwardOutlined,
  StepForwardOutlined,
} from "@ant-design/icons";
import { Button } from "antd";
import { Toolbar, ToolbarGroup, ToolbarItem } from "../Shared/Toolbar";

type Props = {
  onNext: () => void;
  onToday: () => void;
  onPrevious: () => void;
};

export function TimecardViewToolbar(props: Props) {
  const { onNext, onToday, onPrevious } = props;

  return (
    <Toolbar>
      <ToolbarGroup align="left">
        <ToolbarItem>
          <Button
            data-testid="timecard_prev_button"
            onClick={onPrevious}
            type="ghost"
          >
            <StepBackwardOutlined />
          </Button>

          <Button
            data-testid="timecard_today_button"
            onClick={onToday}
            type="ghost"
          >
            <CalendarOutlined />
          </Button>

          <Button
            data-testid="timecard_next_button"
            onClick={onNext}
            type="ghost"
          >
            <StepForwardOutlined />
          </Button>
        </ToolbarItem>
      </ToolbarGroup>
    </Toolbar>
  );
}
