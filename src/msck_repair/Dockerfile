FROM python:3.12

COPY ./requirements.txt . 
RUN pip install -r requirements.txt

COPY ./src/msck_repair.py .
CMD ["python3", "msck_repair.py"]