from fastapi import FastAPI


app = FastAPI()


@app.get("/api/hello")
def hello():
    return {"message": "백엔드 연결 성공!"}
