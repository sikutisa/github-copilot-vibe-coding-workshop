import React, { useState } from "react";

type NameInputModalProps = {
  open: boolean;
  onSubmit: (username: string) => void;
  onClose: () => void;
  loading?: boolean;
  error?: string;
};

const NameInputModal: React.FC<NameInputModalProps> = ({ open, onSubmit, onClose, loading, error }) => {
  const [username, setUsername] = useState("");
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-2xl shadow-lg w-[538px] max-w-full p-8 flex flex-col gap-6">
        <div className="text-3xl font-normal text-black mb-2">Enter your username</div>
        <div className="relative flex flex-col gap-2">
          <input
            className="w-full h-14 rounded-xl bg-gray-300 px-6 text-2xl text-gray-700 outline-none placeholder-gray-400"
            placeholder="UserName"
            value={username}
            onChange={e => setUsername(e.target.value)}
            maxLength={50}
            aria-label="Username"
            autoFocus
          />
          {error && <div className="text-red-500 text-sm mt-1">{error}</div>}
        </div>
        <div className="flex gap-4 justify-center mt-4">
          <button
            className="px-16 py-2 rounded-xl bg-sky-400 text-white text-xl font-normal hover:bg-sky-500 disabled:opacity-50"
            onClick={() => onSubmit(username)}
            disabled={loading || !username.trim()}
            aria-label="OK"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default NameInputModal;
