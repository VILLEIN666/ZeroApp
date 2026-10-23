from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()
devices = {}

class VerifyRequest(BaseModel):
    code: str
    device_name: str

# অটো কানেক্ট (যেকোনো কোড গ্রহণ করবে)
@app.post("/api/pairing/verify")
async def verify_code(req: VerifyRequest):
    devices[req.device_name] = {"status": "online"}
    return {"success": True, "message": "Device connected"}

@app.get("/api/devices")
async def get_devices():
    return {"devices": [{"device_name": k, "status": v["status"]} for k, v in devices.items()]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
