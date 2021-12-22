import { FC, useEffect, useState } from "react";
import * as api from "../../api/About/About";

export const AppVersion: FC<{}> = () => {
  const [appVersion, setAppVersion] = useState<string | undefined>(undefined);

  useEffect(() => {
    const fetchData = async () => {
      const appInfo = await api.getAppInfo();
      console.log("Got version " + appInfo?.app_version);
      setAppVersion(appInfo?.app_version);
    };
    fetchData();
  });

  return (
    <div data-testid="app_version" className="app-version">
      <div className="app-version-number">V:{appVersion}</div>
    </div>
  );
};
