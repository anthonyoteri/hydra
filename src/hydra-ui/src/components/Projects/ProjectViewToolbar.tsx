import { PlusOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { useTranslation } from "react-i18next";
import { Toolbar, ToolbarGroup, ToolbarItem } from "../Shared/Toolbar";

type Props = {
  onAddClick: () => void;
};

export function ProjectViewToolbar({ onAddClick }: Props) {
  const { t } = useTranslation();

  return (
    <Toolbar>
      <ToolbarGroup align="right">
        <ToolbarItem>
          <Button
            data-testid="project_add_button"
            onClick={onAddClick}
            type="primary"
          >
            <PlusOutlined /> {t("projects.createButton")}
          </Button>
        </ToolbarItem>
      </ToolbarGroup>
    </Toolbar>
  );
}
