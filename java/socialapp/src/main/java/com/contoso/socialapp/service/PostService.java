package com.contoso.socialapp.service;

import com.contoso.socialapp.dto.*;
import com.contoso.socialapp.model.*;
import com.contoso.socialapp.repository.*;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;
import java.util.*;
import java.util.stream.Collectors;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class PostService {
    private final PostRepository postRepository;
    private final CommentRepository commentRepository;
    private final LikeRepository likeRepository;

    public List<PostDto> getAllPosts() {
        return postRepository.findAll().stream().map(this::toDto).collect(Collectors.toList());
    }

    public PostDto getPostById(String postId) {
        return postRepository.findById(postId).map(this::toDto).orElseThrow(EntityNotFoundException::new);
    }

    @Transactional
    public PostDto createPost(NewPostRequest req) {
        String id = UUID.randomUUID().toString();
        OffsetDateTime now = OffsetDateTime.now();
        Post post = Post.builder()
                .id(id)
                .username(req.getUsername())
                .content(req.getContent())
                .createdAt(now)
                .updatedAt(now)
                .build();
        postRepository.save(post);
        return toDto(post);
    }

    @Transactional
    public PostDto updatePost(String postId, UpdatePostRequest req) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        if (!post.getUsername().equals(req.getUsername())) {
            throw new IllegalArgumentException("Username does not match post author");
        }
        post.setContent(req.getContent());
        post.setUpdatedAt(OffsetDateTime.now());
        postRepository.save(post);
        return toDto(post);
    }

    @Transactional
    public void deletePost(String postId) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        postRepository.delete(post);
    }

    private PostDto toDto(Post post) {
        return PostDto.builder()
                .id(post.getId())
                .username(post.getUsername())
                .content(post.getContent())
                .createdAt(post.getCreatedAt())
                .updatedAt(post.getUpdatedAt())
                .likesCount(post.getLikesCount())
                .commentsCount(post.getCommentsCount())
                .build();
    }
}
