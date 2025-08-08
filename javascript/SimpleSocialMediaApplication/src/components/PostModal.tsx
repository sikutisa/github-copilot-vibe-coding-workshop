import React, { useState } from "react";

type PostModalProps = {
  open: boolean;
  onClose: () => void;
  onSubmit: (content: string) => void;
  loading?: boolean;
};

const PostModal: React.FC<PostModalProps> = ({ open, onClose, onSubmit, loading }) => {
  const [content, setContent] = useState("");
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-2xl shadow-lg w-[500px] max-w-full p-8 flex flex-col gap-6">
        <div className="text-2xl font-semibold text-gray-700 mb-2">How do you feel today?</div>
        <textarea
          className="w-full h-32 rounded-lg bg-gray-200 p-4 text-lg text-gray-800 resize-none outline-none"
          placeholder="Write your post..."
          value={content}
          onChange={e => setContent(e.target.value)}
          maxLength={2000}
        />
        <div className="flex gap-4 justify-end">
          <button
            className="px-8 py-2 rounded-lg bg-blue-400 text-white text-lg font-bold hover:bg-blue-500 disabled:opacity-50"
            onClick={() => { setContent(""); onSubmit(content); }}
            disabled={loading || !content.trim()}
            aria-label="Submit post"
          >
            Submit
          </button>
          <button
            className="px-8 py-2 rounded-lg bg-blue-100 text-black text-lg font-bold hover:bg-blue-200"
            onClick={() => { setContent(""); onClose(); }}
            aria-label="Cancel post"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostModal;
