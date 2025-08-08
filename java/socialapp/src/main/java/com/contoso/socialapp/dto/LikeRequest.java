package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "LikeRequest")
public class LikeRequest {
    @NotBlank
    @Size(min = 1, max = 50)
    @Schema(description = "Username of the user liking the post", example = "mike_wilson")
    private String username;
}
