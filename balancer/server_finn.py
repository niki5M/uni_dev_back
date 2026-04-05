from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from balancer.decentralized_phase_wave import DecentralizedPhaseWaveBalancer

app = FastAPI(title="Decentralized Phase Wave Balancer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

balancer = DecentralizedPhaseWaveBalancer()


@app.get("/status")
def get_status():
    return JSONResponse(balancer.get_status())


class RequestsPayload(BaseModel):
    count: int = 10


@app.post("/generate_requests")
def generate_requests(body: RequestsPayload):
    current = balancer.add_requests(body.count)
    return JSONResponse(
        {
            "status": "ok",
            "generated": body.count,
            "current": current,
        }
    )


@app.get("/balance")
def balance_one_phase():
    return JSONResponse(balancer.balance_step())


class TopologyPayload(BaseModel):
    topology: Dict[str, List[str]]


@app.post("/topology")
def update_topology(body: TopologyPayload):
    try:
        balancer.set_topology(body.topology)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return JSONResponse({"status": "ok", "topology": body.topology})


class LoadsPayload(BaseModel):
    loads: Dict[str, int]


@app.post("/loads")
def update_loads(body: LoadsPayload):
    try:
        balancer.set_loads(body.loads)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return JSONResponse({"status": "ok", "current": balancer.get_status()})


class RunPayload(BaseModel):
    max_steps: int = 20


@app.post("/balance/run")
def balance_until_stable(body: RunPayload):
    return JSONResponse(balancer.balance_until_stable(max_steps=body.max_steps))


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

