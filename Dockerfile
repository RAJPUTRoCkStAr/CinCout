FROM python:3.12
ADD main.py .
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxrender-dev \
    libgl1-mesa-glx \
    && apt-get clean
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit","run","main.py"]

