package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.*;
import com.contoso.socialapp.model.*;
import com.contoso.socialapp.repository.*;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class LikeService {
    private final PostRepository postRepository;
    private final LikeRepository likeRepository;

    @Transactional
    public LikeResponse likePost(String postId, LikeRequest req) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        Optional<Like> existing = likeRepository.findByPostAndUsername(post, req.getUsername());
        if (existing.isPresent()) {
            throw new IllegalArgumentException("Post already liked by this user");
        }
        Like like = Like.builder()
                .post(post)
                .username(req.getUsername())
                .likedAt(OffsetDateTime.now())
                .build();
        likeRepository.save(like);
        return LikeResponse.builder()
                .postId(post.getId())
                .username(like.getUsername())
                .likedAt(like.getLikedAt())
                .build();
    }

    @Transactional
    public void unlikePost(String postId, String username) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        Optional<Like> like = likeRepository.findByPostAndUsername(post, username);
        if (like.isEmpty()) {
            throw new EntityNotFoundException();
        }
        likeRepository.deleteByPostAndUsername(post, username);
    }
}
