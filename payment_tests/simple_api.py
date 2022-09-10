import uvicorn

from fastapi import FastAPI



app = FastAPI()


@app.post("/get_payment")
async def get_payment_body(body):
    print(body)
    return {"message": f"body"}

@app.get("/")
async def root():
    msg = "redirected from yookassa"
    print("mes")
    return {"message": f"msg"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7777)
