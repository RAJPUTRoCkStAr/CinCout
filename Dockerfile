FROM python:3.12
ADD main.py .
COPY . .
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \  # Added package for libGL
    
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit","run","main.py"]

