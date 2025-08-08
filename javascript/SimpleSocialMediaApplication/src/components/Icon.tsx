import React from "react";

type IconProps = {
  name: "home" | "search" | "person" | "close" | "plus" | "heart" | "comment";
  className?: string;
};

const icons: Record<string, JSX.Element> = {
  home: <span>🏠</span>,
  search: <span>🔍</span>,
  person: <span>👤</span>,
  close: <span>❌</span>,
  plus: <span>➕</span>,
  heart: <span>❤️</span>,
  comment: <span>💬</span>,
};

const Icon: React.FC<IconProps> = ({ name, className }) => (
  <span className={className}>{icons[name]}</span>
);

export default Icon;
