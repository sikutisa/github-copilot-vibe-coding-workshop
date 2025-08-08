package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "NewCommentRequest")
public class NewCommentRequest {
    @NotBlank
    @Size(min = 1, max = 50)
    @Schema(description = "Username of the comment author", example = "jane_smith")
    private String username;

    @NotBlank
    @Size(min = 1, max = 1000)
    @Schema(description = "Content of the comment", example = "Great photo! Where was this taken?")
    private String content;
}
