#  face fusion 1.0
[원본코드](https://github.com/facefusion/facefusion)
    
# 프로세스 작동 원리
<img width="80%" src="https://private-user-images.githubusercontent.com/80209763/304988057-79d025a5-407d-4847-9c8a-8c1eecc66e8f.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDc5ODMxMDYsIm5iZiI6MTcwNzk4MjgwNiwicGF0aCI6Ii84MDIwOTc2My8zMDQ5ODgwNTctNzlkMDI1YTUtNDA3ZC00ODQ3LTljOGEtOGMxZWVjYzY2ZThmLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAyMTUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMjE1VDA3NDAwNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTM3ZTdhMWM1YWY2OWU3ZmEzMDRlNjk4OWNjZWNlNjc5ZGViMDVlNWE3Mjg0ZjBjNGM2NjFkN2RhYzE1YWE2OGYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.nTKffmM9f785HC4wKB7g-YbiljJr6wYNrKdtvl4mS84"/>
## docker 환경 설정

## docker container 생성
    cd Docker
    docker build -t facefusion . --no-cache
    docker-compose up -d

## default folder 만들기
 app 기준

    mkdir .assets/models
    mkdir video_img
    mkdir data/output
    mkdir data/streamlit_input
    mkdir data/video_img
    mkdir logs

## 구동 환경 설정
docker 내부에서 api 사용을 위한 설정

    # api 실행
    python app.py
    # demo 실행
    streamlit run demo.py --server.address 0.0.0.0 --server.port 11000

### auth register
Auth 추가

    curl -XPOST localhost:11000/auth/register --header 'Content-Type: application/json' --data '{"name": "test", "password": "1234"}'

### image
    curl -XPOST localhost:11000/api/face-generation --header 'Content-Type: application/json' --data '{"source": "/workspace/video_img/0.jpg", "target": "/workspace/video_img/13.jpeg"}' --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdCJ9.D5Mw2XPATN0phpUUNh8v253tbvR2MCP1k-LZLYH7Jw4'
