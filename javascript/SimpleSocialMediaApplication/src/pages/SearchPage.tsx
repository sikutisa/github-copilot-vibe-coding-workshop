import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import FloatingButton from "../components/FloatingButton";
import PostModal from "../components/PostModal";
import NameInputModal from "../components/NameInputModal";
import SearchBar from "../components/SearchBar";
import PostList from "../components/PostList";
import ApiStatusIndicator from "../components/ApiStatusIndicator";
import { getPosts } from "../api/client";
import { Post } from "../api/types";

const SearchPage: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [search, setSearch] = useState("");
  const [apiAvailable, setApiAvailable] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);
  const [modalError, setModalError] = useState("");
  const [username, setUsername] = useState<string | null>(null);
  const [nameModalOpen, setNameModalOpen] = useState(true);
  const [nameModalError, setNameModalError] = useState("");

  useEffect(() => {
    if (!username) return;
    getPosts()
      .then(data => {
        setPosts(data);
        setApiAvailable(true);
      })
      .catch(() => setApiAvailable(false));
  }, [username]);
  const handleNameSubmit = (name: string) => {
    if (!name.trim()) {
      setNameModalError("Username is required");
      return;
    }
    setUsername(name.trim());
    setNameModalOpen(false);
    setNameModalError("");
  };
  const handleNameClose = () => {
    setNameModalOpen(false);
  };

  const handleOpenModal = () => {
    setModalOpen(true);
    setModalError("");
  };
  const handleCloseModal = () => {
    setModalOpen(false);
    setModalError("");
  };
  const handleSubmitModal = async (content: string) => {
    setModalLoading(true);
    setModalError("");
    try {
      // 실제 API 연동 필요: post 생성
      // await createPost({ content });
      setModalOpen(false);
      setModalLoading(false);
      setModalError("");
      // 새로고침
      getPosts().then(setPosts);
    } catch (e) {
      setModalError("API 요청에 실패했습니다.");
      setModalLoading(false);
    }
  };

  const filtered = posts.filter(
    p =>
      p.username.toLowerCase().includes(search.toLowerCase()) ||
      p.content.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <NameInputModal
        open={nameModalOpen}
        onSubmit={handleNameSubmit}
        onClose={handleNameClose}
        error={nameModalError}
      />
      {username && (
        <div className="flex h-screen bg-white">
          <Sidebar />
          <main className="flex-1 flex flex-col items-center justify-start p-8 overflow-y-auto">
            <ApiStatusIndicator isAvailable={apiAvailable} />
            <SearchBar value={search} onChange={setSearch} />
            <div className="mt-8 w-full max-w-3xl">
              <PostList posts={filtered} onLike={() => {}} onComment={() => {}} />
            </div>
          </main>
          <FloatingButton onClick={handleOpenModal} />
          <PostModal
            open={modalOpen}
            onClose={handleCloseModal}
            onSubmit={handleSubmitModal}
            loading={modalLoading}
          />
          {modalError && (
            <div className="fixed bottom-28 right-8 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50">
              {modalError}
            </div>
          )}
        </div>
      )}
    </>
  );
};

export default SearchPage;
