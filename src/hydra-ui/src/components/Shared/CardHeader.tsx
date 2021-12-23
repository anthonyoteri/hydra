import { FC, ReactNode } from "react";
import { Outlet } from "react-router-dom";
import styled from "styled-components";
import { Typography } from "antd";

const CardHeaderDiv = styled.div``;
const CardHeaderLeft = styled.div``;
const CardHeaderActions = styled.div``;
const CardHeaderTitle = styled.div``;

interface Props {
  title: string | ReactNode;
  subtitle?: string;
  description?: string;
  dropdownMenu?: ReactNode;
}

export const CardHeader: FC<Props> = (props) => {
  const { title, subtitle, description } = props;

  return (
    <CardHeaderDiv className="card-header">
      <CardHeaderLeft>
        <CardHeaderTitle className="card-header-title">
          {title}
          {subtitle && <small>{subtitle}</small>}
        </CardHeaderTitle>
        {description && (
          <Typography.Text type="secondary">{description}</Typography.Text>
        )}
      </CardHeaderLeft>
      <CardHeaderActions className="card-header-actions">
        <Outlet />
      </CardHeaderActions>
    </CardHeaderDiv>
  );
};
