package com.contoso.socialapp.repository;

import com.contoso.socialapp.model.Comment;
import com.contoso.socialapp.model.Post;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CommentRepository extends JpaRepository<Comment, String> {
    List<Comment> findByPost(Post post);
}
