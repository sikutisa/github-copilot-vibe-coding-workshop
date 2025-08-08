import React from "react";
import { Post } from "../api/types";

type PostCardProps = {
  post: Post;
  onLike: () => void;
  onComment: () => void;
};

const PostCard: React.FC<PostCardProps> = ({ post, onLike, onComment }) => (
  <div className="bg-white rounded-xl shadow p-6 flex flex-col gap-2 mb-6">
    <div className="flex items-center gap-4">
      <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center text-2xl font-bold">
        {post.username[0].toUpperCase()}
      </div>
      <div className="font-bold text-xl">{post.username}</div>
    </div>
    <div className="text-lg text-gray-800 mt-2 mb-2 break-words">{post.content}</div>
    <div className="flex items-center gap-6 mt-2">
      <button onClick={onLike} aria-label="Like post" className="flex items-center gap-1 text-pink-500 hover:text-pink-600">
        <span>❤️</span>
        <span>{post.likesCount}</span>
      </button>
      <button onClick={onComment} aria-label="Comment on post" className="flex items-center gap-1 text-blue-500 hover:text-blue-600">
        <span>💬</span>
        <span>{post.commentsCount}</span>
      </button>
    </div>
  </div>
);

export default PostCard;
