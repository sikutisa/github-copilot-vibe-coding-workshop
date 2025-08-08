import React from "react";
import { Comment } from "../api/types";
import CommentCard from "./CommentCard";

type CommentListProps = {
  comments: Comment[];
};

const CommentList: React.FC<CommentListProps> = ({ comments }) => (
  <div className="flex flex-col gap-2 mt-4">
    {comments.map(comment => (
      <CommentCard key={comment.id} comment={comment} />
    ))}
  </div>
);

export default CommentList;
