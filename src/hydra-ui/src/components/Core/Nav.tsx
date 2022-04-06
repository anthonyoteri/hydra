import {
  CalendarOutlined,
  ClusterOutlined,
  FormOutlined,
  HistoryOutlined,
  HomeOutlined,
  OrderedListOutlined,
  PrinterOutlined,
  SettingOutlined,
} from "@ant-design/icons";
import { Layout, Menu, Typography } from "antd";
import { FC } from "react";
import { useLocation } from "react-router";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { AppVersion } from "./AppVersion";
import Logo from "../../assets/images/logo.png";

const { Sider } = Layout;

export const Nav: FC = () => {
  const { t } = useTranslation();
  const location = useLocation();

  return (
    <Sider>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "24px",
          width: "100%",
        }}
      >
        <img style={{ height: 48 }} src={Logo} title="" alt="" />
        <Typography.Title level={5}>Hydra</Typography.Title>
      </div>
      <Menu
        theme="dark"
        mode="inline"
        className="nice-scrollbars"
        selectedKeys={[location.pathname]}
      >
        {false && (
          <Menu.Item key="/home" icon={<HomeOutlined />}>
            <Link to="/home">
              <span>{t("navigation.home")}</span>
            </Link>
          </Menu.Item>
        )}

        <Menu.Item key="/records" icon={<FormOutlined />}>
          <Link to="/records">
            <span>{t("navigation.records")}</span>
          </Link>
        </Menu.Item>

        <Menu.ItemGroup
          key="configuration"
          title={
            <>
              <SettingOutlined /> {t("navigation.configuration")}
            </>
          }
        >
          <Menu.Item key="/categories" icon={<OrderedListOutlined />}>
            <Link to="/categories">
              <span>{t("navigation.categories")}</span>
            </Link>
          </Menu.Item>

          <Menu.Item key="/projects" icon={<ClusterOutlined />}>
            <Link to="/projects">
              <span>{t("navigation.projects")}</span>
            </Link>
          </Menu.Item>

          <Menu.Item key="/settings" icon={<SettingOutlined />}>
            <Link to="/settings">
              <span>{t("navigation.settings")}</span>
            </Link>
          </Menu.Item>
        </Menu.ItemGroup>

        <Menu.ItemGroup
          key="reporting"
          title={
            <>
              <PrinterOutlined /> {t("navigation.reporting")}
            </>
          }
        >
          {false && (
            <Menu.Item key="/history" icon={<HistoryOutlined />}>
              <Link to="/history">
                <span>{t("navigation.history")}</span>
              </Link>
            </Menu.Item>
          )}

          <Menu.Item key="/timecards" icon={<CalendarOutlined />}>
            <Link to="/timecards">
              <span>{t("navigation.timecards")}</span>
            </Link>
          </Menu.Item>
        </Menu.ItemGroup>
        <Menu.Divider />
      </Menu>

      <AppVersion />
    </Sider>
  );
};
