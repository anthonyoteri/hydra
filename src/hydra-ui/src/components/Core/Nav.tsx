import {
  CalendarOutlined,
  ClusterOutlined,
  HistoryOutlined,
  HomeOutlined,
  OrderedListOutlined,
} from "@ant-design/icons";
import { Layout, Menu } from "antd";
import { FC } from "react";
import { useLocation } from "react-router";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

const { Sider } = Layout;

export const Nav: FC = () => {
  const { t } = useTranslation();
  const location = useLocation();

  return (
    <Sider>
      <Menu
        theme="dark"
        mode="inline"
        className="nice-scrollbars"
        selectedKeys={[location.pathname]}
      >
        <Menu.Item key="/home" icon={<HomeOutlined />}>
          <Link to="/home">
            <span>{t("navigation.home")}</span>
          </Link>
        </Menu.Item>

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

        <Menu.Item key="/history" icon={<HistoryOutlined />}>
          <Link to="/history">
            <span>{t("navigation.history")}</span>
          </Link>
        </Menu.Item>

        <Menu.Item key="/timecards" icon={<CalendarOutlined />}>
          <Link to="/timecards">
            <span>{t("navigation.timecards")}</span>
          </Link>
        </Menu.Item>
      </Menu>
    </Sider>
  );
};
