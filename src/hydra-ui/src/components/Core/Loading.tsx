import { Layout } from "antd";
import React, { FC } from "react";
import styled from "styled-components";
import { LoadingOutlined } from "@ant-design/icons";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  font-size: 96px;
  p {
    font-size: 16px;
    margin-top: 16px;
  }
`;

type Props = {
  message?: string | React.ReactNode;
};

export const Loading: FC<Props> = ({ message }) => (
  <Layout>
    <Container data-testid="init_loader">
      <LoadingOutlined />
      {message && <p>{message}</p>}
    </Container>
  </Layout>
);

export default Loading;
