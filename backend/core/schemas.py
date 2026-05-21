from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TelemetrySchema(BaseModel):
    satellite_id: str
    timestamp: datetime
    position_x: float | None = None
    position_y: float | None = None
    position_z: float | None = None
    velocity_x: float | None = None
    velocity_y: float | None = None
    velocity_z: float | None = None
    temp_payload: float | None = None
    temp_battery: float | None = None
    temp_bus: float | None = None
    sensor1_value: float | None = None
    sensor2_value: float | None = None
    sensor3_value: float | None = None
    comms_rssi: float | None = None
    comms_snr: float | None = None
    comms_packet_loss: float | None = None

class AnomalyCreate(BaseModel):
    satellite_id: str
    metric: str
    value: float
    severity: Optional[str] = "low"

class Anomaly(BaseModel):
    id: int
    satellite_id: str
    metric: str
    value: float
    severity: str
    timestamp: datetime

class Config:
    orm_mode = True