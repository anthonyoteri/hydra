import { FC, useState } from "react";
import { useTranslation } from "react-i18next";
import { Button, Card, Drawer, Layout } from "antd";
import { MenuFoldOutlined } from "@ant-design/icons";
import { MainHeader } from "../Shared/MainHeader/MainHeader";
import { Toolbar, ToolbarGroup } from "../Shared/Toolbar";
import { CardHeader } from "../Shared/CardHeader";
import { SettingsBackup } from "./SettingsBackup";
import { SettingsRestore } from "./SettingsRestore";
import { SettingsDialog } from "./SettingsDialog";

export const SettingsView: FC = () => {
  const { t } = useTranslation();
  const [drawerOpen, showDrawer] = useState<boolean>(false);
  const [advancedOpen, showAdvanced] = useState(false);

  const toggleAdvanced = () => {
    showAdvanced(!advancedOpen);
  };

  return (
    <Layout.Content>
      <MainHeader title={t("settings.pageTitle")} />

      <Toolbar>
        <ToolbarGroup align="left">
          <Button type="ghost" onClick={() => toggleAdvanced()}>
            {advancedOpen ? (
              <>{t("settings.hideAdvancedButtonLabel")}</>
            ) : (
              <>{t("settings.showAdvancedButtonLabel")}</>
            )}
          </Button>
        </ToolbarGroup>
        <ToolbarGroup align="right">
          <Button onClick={() => showDrawer(true)}>
            <MenuFoldOutlined />
            {t("settings.showDrawerButtonLabel")}
          </Button>
        </ToolbarGroup>
      </Toolbar>

      <Drawer
        title={t("settings.backupRestoreDrawerTitle")}
        placement="right"
        closable={true}
        width={720}
        afterVisibleChange={(visible) => {
          visible !== drawerOpen && showDrawer(visible);
        }}
        onClose={() => showDrawer(false)}
        visible={drawerOpen}
      >
        <Card
          className="settings-card"
          bordered={true}
          title={
            <CardHeader
              title={t("settings.backup.title")}
              description={t("settings.backup.description")}
            />
          }
        >
          <SettingsBackup />
        </Card>

        {true && (
          <Card
            className="settings-card"
            bordered={true}
            title={
              <CardHeader
                title={t("settings.restore.title")}
                description={t("settings.restore.description")}
              />
            }
          >
            <SettingsRestore disabled={false} />
          </Card>
        )}
      </Drawer>
      <SettingsDialog hideAdvanced={!advancedOpen} />
    </Layout.Content>
  );
};
