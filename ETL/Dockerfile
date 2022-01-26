FROM python:3.9
WORKDIR /DOC_ETL
ADD . /DOC_ETL
RUN pip install --upgrade pip
RUN pip install --trusted-host pipy.python.org -r requirements.txt
CMD ["python", "/DOC_ETL/ETL_Job.py"]