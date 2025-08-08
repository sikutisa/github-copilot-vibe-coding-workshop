import React, { useState } from "react";

type CommentInputProps = {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
};

const CommentInput: React.FC<CommentInputProps> = ({ value, onChange, onSubmit, disabled }) => (
  <div className="flex items-center gap-2 bg-blue-400 rounded-lg px-4 py-2 mt-4">
    <input
      className="bg-transparent outline-none flex-1 text-lg text-white placeholder-gray-200"
      type="text"
      value={value}
      onChange={e => onChange(e.target.value)}
      placeholder="Enter comment"
      aria-label="댓글 입력"
      disabled={disabled}
    />
    <button
      className="bg-white text-blue-500 rounded px-4 py-1 font-bold hover:bg-blue-100 disabled:opacity-50"
      onClick={onSubmit}
      disabled={disabled || !value.trim()}
      aria-label="댓글 등록"
      tabIndex={0}
    >
      등록
    </button>
  </div>
);

export default CommentInput;
