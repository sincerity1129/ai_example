#  face fusion 1.0
face swap

## docker 환경 설정

## docker container 생성
    cd Docker
    docker build -t facefusion . --no-cache
    docker-compose up -d


## 구동 환경 설정
docker 내부에서 api 사용을 위한 설정

    # api 실행
    python app.py
    # demo 실행
    streamlit run demo.py --server.address 0.0.0.0 --server.port 11000

데모 id와 token

    id: test
    token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdCJ9.QlmOBM7imQkVauXII7Hd9rYAFgW6NKMuvZ4GmVSTgpM



#### API 예제
    # swagger 경로
    localhost:12000

# facefasion
