from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes import router

app = FastAPI()
app.include_router(router)


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def root():
    return """
    <html>
      <head><title>Server B</title></head>
      <body>
        <h1>Server B is running 🟢</h1>
        <p>This service stores IP coordinates in Redis.</p>
        <p>See <a href="/docs">/docs</a> for API details.</p>
      </body>
    </html>
    """