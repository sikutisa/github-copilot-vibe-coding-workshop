package com.contoso.socialapp.repository;

import com.contoso.socialapp.model.Like;
import com.contoso.socialapp.model.Post;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface LikeRepository extends JpaRepository<Like, String> {
    Optional<Like> findByPostAndUsername(Post post, String username);
    int countByPost(Post post);
    void deleteByPostAndUsername(Post post, String username);
}
