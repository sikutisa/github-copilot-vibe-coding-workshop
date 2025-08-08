import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import FloatingButton from "../components/FloatingButton";
import ApiStatusIndicator from "../components/ApiStatusIndicator";
import CommentList from "../components/CommentList";
import CommentInput from "../components/CommentInput";
import { Post, Comment } from "../api/types";
// TODO: 실제 API 연동 필요

const dummyPost: Post = {
  id: "1",
  username: "john_doe",
  content: "Just had an amazing hike in the mountains! #outdoorlife",
  createdAt: "2025-06-01T10:30:00Z",
  updatedAt: "2025-06-01T10:30:00Z",
  likesCount: 15,
  commentsCount: 3,
};
const dummyComments: Comment[] = [
  { id: "c1", postId: "1", username: "jane_smith", content: "Nice to meet you!", createdAt: "2025-06-01T11:15:00Z", updatedAt: "2025-06-01T11:15:00Z" },
  { id: "c2", postId: "1", username: "alex", content: "Great post!", createdAt: "2025-06-01T11:20:00Z", updatedAt: "2025-06-01T11:20:00Z" },
];

const PostDetailPage: React.FC = () => {
  const [post] = useState<Post>(dummyPost);
  const [comments, setComments] = useState<Comment[]>(dummyComments);
  const [comment, setComment] = useState("");
  const [apiAvailable] = useState(true);

  const handleCommentSubmit = () => {
    if (!comment.trim()) return;
    setComments([
      ...comments,
      {
        id: Math.random().toString(),
        postId: post.id,
        username: "me",
        content: comment,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
    ]);
    setComment("");
  };

  return (
    <div className="flex h-screen bg-white">
      <Sidebar />
      <main className="flex-1 flex flex-col items-center justify-start p-8 overflow-y-auto">
        <ApiStatusIndicator isAvailable={apiAvailable} />
        <div className="bg-white rounded-xl shadow p-6 flex flex-col gap-2 mb-6 w-full max-w-2xl">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center text-2xl font-bold">
              {post.username[0].toUpperCase()}
            </div>
            <div className="font-bold text-xl">{post.username}</div>
          </div>
          <div className="text-lg text-gray-800 mt-2 mb-2 break-words">{post.content}</div>
          <div className="flex items-center gap-6 mt-2">
            <button aria-label="Like post" className="flex items-center gap-1 text-pink-500 hover:text-pink-600">
              <span>❤️</span>
              <span>{post.likesCount}</span>
            </button>
            <button aria-label="Comment on post" className="flex items-center gap-1 text-blue-500 hover:text-blue-600">
              <span>💬</span>
              <span>{post.commentsCount}</span>
            </button>
          </div>
        </div>
        <div className="w-full max-w-2xl">
          <CommentList comments={comments} />
          <CommentInput value={comment} onChange={setComment} onSubmit={handleCommentSubmit} />
        </div>
      </main>
      <FloatingButton onClick={() => {}} />
    </div>
  );
};

export default PostDetailPage;
