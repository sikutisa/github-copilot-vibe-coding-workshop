package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.*;
import java.time.OffsetDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Post")
public class PostDto {
    @Schema(description = "Unique identifier for the post", example = "123e4567-e89b-12d3-a456-426614174000")
    private String id;

    @NotBlank
    @Size(min = 1, max = 50)
    @Schema(description = "Username of the post author", example = "john_doe")
    private String username;

    @NotBlank
    @Size(min = 1, max = 2000)
    @Schema(description = "Content of the post", example = "Just had an amazing hike in the mountains! #outdoorlife")
    private String content;

    @Schema(description = "Timestamp when the post was created", example = "2025-06-01T10:30:00Z")
    private OffsetDateTime createdAt;

    @Schema(description = "Timestamp when the post was last updated", example = "2025-06-01T10:30:00Z")
    private OffsetDateTime updatedAt;

    @Schema(description = "Number of likes on the post", example = "15")
    private int likesCount;

    @Schema(description = "Number of comments on the post", example = "3")
    private int commentsCount;
}
