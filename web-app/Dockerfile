ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

#set the working directory in the image
WORKDIR /app

#install dependencies into the image
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# add files from local machine into a Docker image
ADD . .

# expose port that the Flask app is running on
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
