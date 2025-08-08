import axios from "axios";
import { Post } from "./types";

const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 5000,
});

export async function getPosts(): Promise<Post[]> {
  const res = await api.get<Post[]>("/posts");
  return res.data;
}
