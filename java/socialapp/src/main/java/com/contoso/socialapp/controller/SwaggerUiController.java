package com.contoso.socialapp.controller;

import io.swagger.v3.oas.annotations.Hidden;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class SwaggerUiController {
    @Hidden
    @GetMapping("/docs")
    public String redirectToSwaggerUi() {
        return "redirect:/swagger-ui/index.html";
    }
}
