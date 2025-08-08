import React from "react";

const Sidebar: React.FC = () => {
  return (
    <aside className="flex flex-col items-center justify-center bg-yellow-500 rounded-2xl p-2 h-full w-[110px] gap-8">
      {/* TODO: Icon 컴포넌트로 대체 */}
      <div className="w-14 h-12 flex items-center justify-center"><span>🏠</span></div>
      <div className="w-14 h-14 flex items-center justify-center"><span>🔍</span></div>
      <div className="w-14 h-14 flex items-center justify-center"><span>👤</span></div>
      <div className="w-14 h-14 flex items-center justify-center"><span>❌</span></div>
    </aside>
  );
};

export default Sidebar;
