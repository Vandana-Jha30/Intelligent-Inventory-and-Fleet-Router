from pydantic import BaseModel, Field


class FlowNodeRequest(BaseModel):
    node_id: int = Field(gt=0)
    name: str = Field(min_length=1)
    supply: float = Field(default=0, ge=0)
    demand: float = Field(default=0, ge=0)


class FlowArcRequest(BaseModel):
    from_node: int = Field(gt=0)
    to_node: int = Field(gt=0)
    capacity: float = Field(gt=0)
    cost: float = Field(ge=0)


class MinCostFlowRequest(BaseModel):
    nodes: list[FlowNodeRequest] = Field(min_length=1)
    arcs: list[FlowArcRequest] = Field(min_length=1)


class FlowPlanResponse(BaseModel):
    from_node: int
    to_node: int
    flow: float
    capacity: float
    unit_cost: float
    total_cost: float


class MinCostFlowResponse(BaseModel):
    total_supply: float
    total_demand: float
    total_flow: float
    total_cost: float
    flow_plan: list[FlowPlanResponse]
