package com.contoso.socialapp.controller;

import com.contoso.socialapp.dto.*;
import com.contoso.socialapp.service.LikeService;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/posts/{postId}/likes")
@RequiredArgsConstructor
@Tag(name = "Likes")
public class LikeController {
    private final LikeService likeService;

    @PostMapping
    public ResponseEntity<LikeResponse> likePost(@PathVariable String postId, @Valid @RequestBody LikeRequest req) {
        LikeResponse res = likeService.likePost(postId, req);
        return ResponseEntity.status(HttpStatus.CREATED).body(res);
    }

    @DeleteMapping
    public ResponseEntity<Void> unlikePost(@PathVariable String postId, @RequestParam String username) {
        likeService.unlikePost(postId, username);
        return ResponseEntity.noContent().build();
    }
}
