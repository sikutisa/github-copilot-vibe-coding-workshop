import React from "react";

type FloatingButtonProps = {
  onClick: () => void;
  label?: string;
};

const FloatingButton: React.FC<FloatingButtonProps> = ({ onClick, label }) => (
  <button
    className="fixed right-8 bottom-8 bg-yellow-500 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-lg text-3xl hover:bg-yellow-400 focus:outline-none"
    onClick={onClick}
    aria-label={label || "Add"}
    tabIndex={0}
  >
    +
  </button>
);

export default FloatingButton;
