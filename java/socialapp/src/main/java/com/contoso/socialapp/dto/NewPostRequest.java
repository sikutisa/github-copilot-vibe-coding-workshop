package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "NewPostRequest")
public class NewPostRequest {
    @NotBlank
    @Size(min = 1, max = 50)
    @Schema(description = "Username of the post author", example = "john_doe")
    private String username;

    @NotBlank
    @Size(min = 1, max = 2000)
    @Schema(description = "Content of the post", example = "Just had an amazing hike in the mountains! #outdoorlife")
    private String content;
}
