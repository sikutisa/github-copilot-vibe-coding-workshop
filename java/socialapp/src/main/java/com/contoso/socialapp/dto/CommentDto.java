package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.*;
import java.time.OffsetDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Comment")
public class CommentDto {
    @Schema(description = "Unique identifier for the comment", example = "987fcdeb-51a2-43d1-9f6b-123456789abc")
    private String id;

    @Schema(description = "ID of the post this comment belongs to", example = "123e4567-e89b-12d3-a456-426614174000")
    private String postId;

    @NotBlank
    @Size(min = 1, max = 50)
    @Schema(description = "Username of the comment author", example = "jane_smith")
    private String username;

    @NotBlank
    @Size(min = 1, max = 1000)
    @Schema(description = "Content of the comment", example = "Great photo! Where was this taken?")
    private String content;

    @Schema(description = "Timestamp when the comment was created", example = "2025-06-01T11:15:00Z")
    private OffsetDateTime createdAt;

    @Schema(description = "Timestamp when the comment was last updated", example = "2025-06-01T11:15:00Z")
    private OffsetDateTime updatedAt;
}
