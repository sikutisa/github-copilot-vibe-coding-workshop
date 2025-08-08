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
public class CommentService {
    private final PostRepository postRepository;
    private final CommentRepository commentRepository;

    public List<CommentDto> getCommentsByPostId(String postId) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        return commentRepository.findByPost(post).stream().map(this::toDto).collect(Collectors.toList());
    }

    public CommentDto getCommentById(String postId, String commentId) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        Comment comment = commentRepository.findById(commentId).orElseThrow(EntityNotFoundException::new);
        if (!comment.getPost().getId().equals(post.getId())) throw new EntityNotFoundException();
        return toDto(comment);
    }

    @Transactional
    public CommentDto createComment(String postId, NewCommentRequest req) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        String id = UUID.randomUUID().toString();
        OffsetDateTime now = OffsetDateTime.now();
        Comment comment = Comment.builder()
                .id(id)
                .post(post)
                .username(req.getUsername())
                .content(req.getContent())
                .createdAt(now)
                .updatedAt(now)
                .build();
        commentRepository.save(comment);
        return toDto(comment);
    }

    @Transactional
    public CommentDto updateComment(String postId, String commentId, UpdateCommentRequest req) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        Comment comment = commentRepository.findById(commentId).orElseThrow(EntityNotFoundException::new);
        if (!comment.getPost().getId().equals(post.getId())) throw new EntityNotFoundException();
        if (!comment.getUsername().equals(req.getUsername())) throw new IllegalArgumentException("Username does not match comment author");
        comment.setContent(req.getContent());
        comment.setUpdatedAt(OffsetDateTime.now());
        commentRepository.save(comment);
        return toDto(comment);
    }

    @Transactional
    public void deleteComment(String postId, String commentId) {
        Post post = postRepository.findById(postId).orElseThrow(EntityNotFoundException::new);
        Comment comment = commentRepository.findById(commentId).orElseThrow(EntityNotFoundException::new);
        if (!comment.getPost().getId().equals(post.getId())) throw new EntityNotFoundException();
        commentRepository.delete(comment);
    }

    private CommentDto toDto(Comment comment) {
        return CommentDto.builder()
                .id(comment.getId())
                .postId(comment.getPost().getId())
                .username(comment.getUsername())
                .content(comment.getContent())
                .createdAt(comment.getCreatedAt())
                .updatedAt(comment.getUpdatedAt())
                .build();
    }
}
