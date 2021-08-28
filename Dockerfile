# pull the appripriate python image
FROM python:3.8.10

# set workdir
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

# CMD ["python3", "-m", "src.bot_main"]
# CMD ["python3", "manage.py", "runserver", "0:8000"]
ENTRYPOINT ["python3", "manage.py", "runserver"]
CMD ["0:8000"]