FROM ubuntu

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

ENV DEBIAN_FRONTEND noninteractive

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apt-get update -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-tk -y
RUN python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# CMD python server.py
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 'server:create_app()'