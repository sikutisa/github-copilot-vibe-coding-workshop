import React from "react";
import { Comment } from "../api/types";

type CommentCardProps = {
  comment: Comment;
};

const CommentCard: React.FC<CommentCardProps> = ({ comment }) => (
  <div className="flex items-start gap-4 py-2">
    <div className="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center text-lg font-bold">
      {comment.username[0].toUpperCase()}
    </div>
    <div className="flex flex-col">
      <span className="font-bold text-base">{comment.username}</span>
      <span className="text-gray-700 text-base break-words">{comment.content}</span>
    </div>
  </div>
);

export default CommentCard;
