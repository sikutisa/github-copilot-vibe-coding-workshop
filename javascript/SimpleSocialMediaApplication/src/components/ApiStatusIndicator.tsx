import React from "react";

type ApiStatusIndicatorProps = {
  isAvailable: boolean;
};

const ApiStatusIndicator: React.FC<ApiStatusIndicatorProps> = ({ isAvailable }) => (
  <div className={
    `fixed top-2 right-2 px-4 py-2 rounded-lg text-white text-sm font-bold z-50 ` +
    (isAvailable ? "bg-green-500" : "bg-red-500 animate-pulse")
  }>
    {isAvailable ? "API 연결됨" : "API 연결 불가"}
  </div>
);

export default ApiStatusIndicator;
