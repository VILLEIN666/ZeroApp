from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import random
import string

app = FastAPI()
pairing_codes = {}
devices = {}

class PairRequest(BaseModel):
    guardian_id: str

class VerifyRequest(BaseModel):
    code: str
    device_name: str

@app.post("/api/pairing/generate")
async def generate_code(req: PairRequest):
    code = ''.join(random.choices(string.digits, k=6))
    pairing_codes[code] = req.guardian_id
    return {"code": code}

@app.post("/api/pairing/verify")
async def verify_code(req: VerifyRequest):
    if req.code in pairing_codes:
        devices[req.device_name] = {"status": "online"}
        return {"success": True, "message": "Device paired"}
    raise HTTPException(status_code=400, detail="Invalid code")

@app.get("/api/devices")
async def get_devices():
    return {"devices": [{"device_name": k, "status": v["status"]} for k, v in devices.items()]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
