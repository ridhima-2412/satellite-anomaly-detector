FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY simulator/ .
CMD ["python", "simulator.py"]