import { PlusOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { useTranslation } from "react-i18next";
import { Toolbar, ToolbarGroup, ToolbarItem } from "../Shared/Toolbar";

type Props = {
  onAddClick: () => void;
};

export function RecordViewToolbar({ onAddClick }: Props) {
  const { t } = useTranslation();

  return (
    <Toolbar>
      <ToolbarGroup align="right">
        <ToolbarItem>
          <Button
            data-testid="record_add_button"
            onClick={onAddClick}
            type="primary"
          >
            <PlusOutlined /> {t("records.createButton")}
          </Button>
        </ToolbarItem>
      </ToolbarGroup>
    </Toolbar>
  );
}
