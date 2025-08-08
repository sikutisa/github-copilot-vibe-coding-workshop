package com.contoso.socialapp.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Error")
public class ErrorResponse {
    @Schema(description = "Error code or type", example = "VALIDATION_ERROR")
    private String error;

    @Schema(description = "Human-readable error message", example = "The request body is invalid")
    private String message;

    @Schema(description = "Additional error details (optional)")
    private List<String> details;
}
