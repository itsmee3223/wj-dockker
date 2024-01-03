FROM python:3.8
WORKDIR /app
COPY scale.py requirements.txt /app/
RUN pip install -r requirements.txt
CMD ["python", "scale.py"]
