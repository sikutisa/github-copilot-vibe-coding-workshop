import React from "react";
import { Post } from "../api/types";
import PostCard from "./PostCard";

type PostListProps = {
  posts: Post[];
  onLike: (id: string) => void;
  onComment: (id: string) => void;
};

const PostList: React.FC<PostListProps> = ({ posts, onLike, onComment }) => (
  <div className="flex flex-col gap-4">
    {posts.map(post => (
      <PostCard
        key={post.id}
        post={post}
        onLike={() => onLike(post.id)}
        onComment={() => onComment(post.id)}
      />
    ))}
  </div>
);

export default PostList;
