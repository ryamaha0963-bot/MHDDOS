FROM python:3.10-slim

WORKDIR /app

# Install MHDDoS dependencies
RUN apt update && apt install -y git curl wget libcurl4 libssl-dev make cmake automake autoconf m4 build-essential

# Clone MHDDoS
RUN git clone https://github.com/MatrixTM/MHDDoS.git /app/mhddos

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install MHDDoS deps
RUN pip install -r /app/mhddos/requirements.txt

# Copy bot
COPY main.py .

# Start bot
CMD ["python", "main.py"]
