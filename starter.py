import uvicorn
from main import app
from decouple import config

port = int(config('PORT', default=6969))
uvicorn.run(app, host="0.0.0.0", port=port)
