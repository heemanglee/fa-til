## 프로젝트 구조

```
fa-til/
├── main.py                   # FastAPI 애플리케이션 진입점
├── database.py               # 데이터베이스 연결 설정
├── database_models.py        # SQLAlchemy 모델
├── docker-compose.yml        # Docker 설정
├── requirements.txt          # Python 의존성
├── alembic.ini               # 데이터베이스 마이그레이션 설정
├── migration/                # 데이터베이스 마이그레이션
├── utils/                    # 공통 유틸리티
└── user/                     # 사용자 도메인
    ├── infra/                # 인프라 계층
    │   ├── model/            # 데이터베이스 모델
    │   └── repository/       # 데이터 접근 구현체
    ├── interface/            # 인터페이스 계층
    │   └── controller/
    ├── application/          # 애플리케이션 계층
    ├── domain/               # 도메인 계층
    └── repository/           # 리포지토리 인터페이스
```

### 아키텍처 계층

계층이 안쪽(도메인)으로 들어갈수록 더 고수준이 되어 추상적이게 됩니다:

- **도메인 (Domain)**: 핵심 비즈니스 로직과 엔티티 (가장 추상적, 고수준)
- **애플리케이션 (Application)**: 비즈니스 유스케이스 조정
- **인터페이스 (Interface)**: 외부와의 상호작용 (Controller, API)
- **인프라 (Infrastructure)**: 데이터베이스, 외부 서비스 연동 (가장 구체적, 저수준)