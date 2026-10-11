from fastapi import APIRouter, HTTPException

from app.optimization.min_cost_flow_solver import solve_min_cost_flow
from app.schemas.min_cost_flow import (
    MinCostFlowRequest,
    MinCostFlowResponse,
)


router = APIRouter(
    prefix="/api/min-cost-flow",
    tags=["Minimum Cost Flow"],
)


@router.post("/solve", response_model=MinCostFlowResponse)
def solve(request: MinCostFlowRequest):
    try:
        return solve_min_cost_flow(request.nodes, request.arcs)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))
