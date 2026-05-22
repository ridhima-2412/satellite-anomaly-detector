FROM python:3.10
WORKDIR /app
COPY simulator/requirements.txt .
RUN pip install -r requirements.txt
COPY simulator/ .
CMD ["python", "simulator.py"]