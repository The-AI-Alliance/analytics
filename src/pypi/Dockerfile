FROM python:3.12

COPY ./requirements.txt . 
RUN pip install -r requirements.txt

COPY ./src/pypi.py .
CMD ["python3", "pypi.py"]