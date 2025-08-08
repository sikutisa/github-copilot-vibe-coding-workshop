package com.contoso.socialapp.config;

import com.contoso.socialapp.model.Post;
import com.contoso.socialapp.repository.PostRepository;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
@RequiredArgsConstructor
public class DatabaseInitializer {
    private final PostRepository postRepository;

    @PostConstruct
    @Transactional
    public void init() {
        // DB는 항상 초기화됨 (spring.jpa.hibernate.ddl-auto=create-drop)
        // 필요시 샘플 데이터 추가 가능
    }
}
