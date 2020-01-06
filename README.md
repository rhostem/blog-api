# blog-api

## 개발

### virtualenv 활성화

```bash
. ./venv/bin/activate
```

### 필요한 패키지 설치

```bash
pip install -r requirements
```

#### 설치한 패키지 정보를 파일애 저장

```bash
pip freeze > requirements
```

## 배포

[구글 애널리틱스 API를 사용한 Flask 앱을 uWSGI와 nginx로 배포한 과정 | blog.rhostem.com](https://blog.rhostem.com/posts/2018-11-20-deploy-flask-with-uwsgi)

## references

- [Automatically activate virtualenv - Nathan Cahill](http://nathancahill.github.io/automatically-activate-virtualenv/)
- [Better Python dependency while packaging your project](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1)
