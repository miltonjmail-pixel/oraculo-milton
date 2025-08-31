from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

@app.get("/oraculo")
def oraculo():
    def evento():
        for i in range(10):
            yield f"data: Hallazgo #{i+1}: token simulado en SAFE_MODE\n\n"
            time.sleep(1)
    return StreamingResponse(evento(), media_type="text/event-stream")
