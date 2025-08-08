export type Post = {
  id: string;
  username: string;
  content: string;
  createdAt: string;
  updatedAt: string;
  likesCount: number;
  commentsCount: number;
};

export type Comment = {
  id: string;
  postId: string;
  username: string;
  content: string;
  createdAt: string;
  updatedAt: string;
};
