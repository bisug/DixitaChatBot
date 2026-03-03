import logging
from config import PORT

async def start_web_server():
    """Initializes and runs a FastAPI web server to provide an HTTP health-check endpoint."""
    try:
        from fastapi import FastAPI
        import uvicorn
        
        # Instantiate FastAPI application for handling HTTP requests
        app = FastAPI()

        @app.get("/")
        async def root():
            """Returns a simple JSON response confirming the bot's operational status."""
            return {"status": "DixitaChatBot is running successfully."}

        # Configure the uvicorn server for the FastAPI app
        config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
        server = uvicorn.Server(config)

        logging.info(f"Starting optional web service on port {PORT}")

        # Asynchronously serve the application
        await server.serve()
    except ImportError:
        logging.error("FastAPI or Uvicorn is not installed. Web service cannot start.")
