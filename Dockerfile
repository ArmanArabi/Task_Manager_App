FROM python:3.11-slim

#container working directory
WORKDIR /usr/src/app

#copy the requirements for using docker cache
COPY ./requirements.txt .

#install the lib & ...
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#copy all code to the destination dir
COPY . . 

#run code
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
