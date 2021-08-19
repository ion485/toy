# toy project (Private)

2021 - 08 - 19
조강희 - Dyphi (CUop)

가장 기본적인 홈페이지 구성 (Board 기반)
Django 기본 패키지를 이용한 로그인, 회원가입, 게시글 기능 공부
이메일 인증, 비밀번호 변경/초기화 등의 기능 공부
로그인 한 사용자만 게시글을 열람할 수 있도록 변경

회사 요구 사항 : Oauth를 이용해 소셜 로그인 구현과 과정 상 어려움
- django 기본 패키지들 상속하여 overide에 어려움
- 각 사이트 제공 API를 이용한 구현 vs django-allauth third-party 라이브러리를 이용한 구현
- API와 제공 로그인 버튼 사용 시 유의점

* http://localhost:8000/para/ : 게시글 접근 url
* 접근시 로그인 되어있지 않은 상태라면 로그인창으로 이동.
* database 관리는 django 제공 admin으로.
