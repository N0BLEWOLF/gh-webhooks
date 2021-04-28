from fastapi import FastAPI, Request
import uvicorn
from client import config, tgbot

app = FastAPI(debug=True)

@app.get("/omk")
async def test(request: Request):
    return ({"hello": "world"})


@app.get("/")
async def fuck(request: Request):
    om = await tgbot.send_message(-1001237141420, "TEST")
    print(om)
    return ({"msg": "MC"})


PORT = config("PORT")
if __name__ == "__main__":
    uvicorn.run(
        "test:app", host="0.0.0.0", port=int(PORT), log_level="info", reload=False
    )
