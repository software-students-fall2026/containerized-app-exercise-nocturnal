machine learning client

this cheeky client uses a pre-trained yolo-world model to detect the ingredients in an image. the prediction is then saved to mongodb.

here are some somewhat important steps:
1. build the image:
    docker build -t machine-learning-client .
2. start the client with a mongodb connection string:
    docker run --rm -p 5001:5001 -e MONGO_URI="yourMongoDBConnectionString" machine-learning-client
3. send a post request to /detect with an image in the image field.
    please note the image upload must be multi-part and no longer than 10mb.
4. _optional_: run the tests:
    docker run --rm machine-learning-client python -m pytest
