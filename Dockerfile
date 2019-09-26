FROM python:3.7
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
WORKDIR /app/app
EXPOSE 5000
CMD ["python", "app.py"]
