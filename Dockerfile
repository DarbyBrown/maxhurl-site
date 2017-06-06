FROM ubuntu:16.04

RUN apt-get update && apt-get install -y git nginx libreadline-dev python3-pip python3-venv build-essential python-setuptools nodejs npm
RUN ln -s /usr/bin/nodejs /usr/bin/node

# Set the working directory to /app
RUN mkdir /opt/app
WORKDIR /opt/app

# Copy the current directory contents into the container at /app
ADD . /opt/app

# install and build
RUN python3 -m venv env && env/bin/pip install -U setuptools && env/bin/pip install -r requirements.txt
RUN npm install && npm run build-dev

# Make port 80 available to the world outside this container
EXPOSE 8080

CMD ["env/bin/waitress-serve", "--port", "8080", "maxhurl:app"]