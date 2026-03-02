import logging
from config import PORT

async def start_web_server():
    try:
        from fastapi import FastAPI
        import uvicorn
        
        app = FastAPI()

        @app.get("/")
        async def root():
            return {"status": "DixitaChatBot is running successfully."}

        config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
        server = uvicorn.Server(config)
        logging.info(f"Starting optional web service on port {PORT}")
        await server.serve()
    except ImportError:
        logging.error("FastAPI or Uvicorn is not installed. Web service cannot start.")
