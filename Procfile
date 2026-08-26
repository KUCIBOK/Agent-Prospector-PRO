web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
release: python -c "from app.db import engine; from sqlmodel import SQLModel; SQLModel.metadata.create_all(engine)"
worker: python -c "from app.scheduler import start_scheduler; start_scheduler()"
