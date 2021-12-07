import { PlusOutlined } from "@ant-design/icons";
import { Button } from "antd";
import { useTranslation } from "react-i18next";
import { Toolbar, ToolbarGroup, ToolbarItem } from "../Shared/Toolbar";

type Props = {
  onAddClick: () => void;
};

export function CategoryViewToolbar({ onAddClick }: Props) {
  const { t } = useTranslation();

  return (
    <Toolbar>
      <ToolbarGroup align="right">
        <ToolbarItem>
          <Button
            data-testid="category_add_button"
            onClick={onAddClick}
            type="primary"
          >
            <PlusOutlined /> {t("categories.createButton")}
          </Button>
        </ToolbarItem>
      </ToolbarGroup>
    </Toolbar>
  );
}
