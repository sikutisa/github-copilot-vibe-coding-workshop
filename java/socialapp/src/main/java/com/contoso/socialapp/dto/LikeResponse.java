package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;
import java.time.OffsetDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "LikeResponse")
public class LikeResponse {
    @Schema(description = "ID of the liked post", example = "123e4567-e89b-12d3-a456-426614174000")
    private String postId;

    @Schema(description = "Username who liked the post", example = "mike_wilson")
    private String username;

    @Schema(description = "Timestamp when the post was liked", example = "2025-06-01T12:00:00Z")
    private OffsetDateTime likedAt;
}
