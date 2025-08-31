from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from datetime import datetime
import time

app = FastAPI()

@app.get("/oraculo")
def oraculo():
    def generar_eventos():
        for i in range(10):
            timestamp = datetime.utcnow().isoformat()
            yield f"data: {{\"hallazgo\": \"Token #{i+1}\", \"modo\": \"SAFE_MODE\", \"timestamp\": \"{timestamp}\"}}\n\n"
            time.sleep(1)
    return StreamingResponse(generar_eventos(), media_type="text/event-stream")
