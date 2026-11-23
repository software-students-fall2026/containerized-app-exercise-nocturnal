ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# yolo uses opencv
# opencv needs libxcb
RUN apt-get update && apt-get install -y libxcb1

# opencv needs libgl
RUN apt-get install -y libgl1

# opencv needs glib
RUN apt-get install -y libglib2.0-0

# clip needs git
RUN apt-get install -y git

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY model.py ./
# download yolo and set labels
RUN python3 -c "from model import prepare_yolo_world_for_kitchen_ingredients; prepare_yolo_world_for_kitchen_ingredients()"

ADD . .

CMD ["python3", "-m", "flask", "--app", "server:create_image_detection_app", "run", "--host=0.0.0.0", "--port=5001"]
