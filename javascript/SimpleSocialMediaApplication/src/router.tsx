import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import PostDetailPage from "./pages/PostDetailPage";

const Router: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<SearchPage />} />
      <Route path="/posts/:postId" element={<PostDetailPage />} />
    </Routes>
  </BrowserRouter>
);

export default Router;
