package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "UpdatePostRequest")
public class UpdatePostRequest {
    @NotBlank
    @Size(min = 1, max = 50)
    @Schema(description = "Username of the post author (for validation)", example = "john_doe")
    private String username;

    @NotBlank
    @Size(min = 1, max = 2000)
    @Schema(description = "Updated content of the post", example = "Just had an amazing hike in the mountains! The view was breathtaking. #outdoorlife #hiking")
    private String content;
}
