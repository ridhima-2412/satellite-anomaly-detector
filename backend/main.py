
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core import models, schemas
from core.database import engine, get_db
from datetime import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Satellite Telemetry Backend")
@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/telemetry/")
def receive_telemetry(data: schemas.TelemetrySchema, db: Session = Depends(get_db)):
    # Map simulator fields to DB fields
    telemetry_data = data.dict()
    telemetry_data['temperature'] = telemetry_data.pop('temp_payload', None)
    telemetry_data['rssi'] = telemetry_data.pop('comms_rssi', None)
    telemetry_data['snr'] = telemetry_data.pop('comms_snr', None)
    telemetry_data['packet_loss'] = telemetry_data.pop('comms_packet_loss', None)
    # Remove extra fields not in DB model
    for key in ['temp_battery', 'temp_bus', 'sensor1_value', 'sensor2_value', 'sensor3_value']:
        telemetry_data.pop(key, None)

    telemetry = models.Telemetry(**telemetry_data)
    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)

    issues = []
    score = 0
    severity = "normal"

    if telemetry.temperature and telemetry.temperature > 45:
       issues.append("High Temperature")
       score += 0.6
    if telemetry.packet_loss and telemetry.packet_loss > 0.1:
       issues.append("High Packet Loss")
       score += 0.8

    if len(issues) == 1:
        severity = "warning"
    elif len(issues) >= 2:
        severity = "critical"

    if issues:
        anomaly = models.AnomalyEvent(
            satellite_id=telemetry.satellite_id,
            severity=severity,
            issue=", ".join(issues),
            score=score
        )
        db.add(anomaly)
        db.commit()
        db.refresh(anomaly)

    return {"status": "ok", "anomaly_detected": bool(issues)}

@app.get("/anomalies/latest")
def get_latest_anomalies(db: Session = Depends(get_db)):
    anomalies = db.query(models.AnomalyEvent)
    return anomalies

