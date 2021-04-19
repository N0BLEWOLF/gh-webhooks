import uvicorn
from decouple import config

from main import app

port = int(config("PORT", default=6969))
uvicorn.run(app, host="0.0.0.0", port=port)
