"""detect kitchen ingredients with yolo world"""

from PIL import Image
from ultralytics import YOLOWorld

INGREDIENTS = [
    "apple",
    "banana",
    "tomato",
    "carrot",
    "chicken",
    "potato",
    "milk carton",
    "bread",
    "onion",
    "cheese",
    "corn",
    "shrimp",
    "butter",
    "chocolate",
    "beef",
    "sugar",
    "lime",
    "blueberries",
    "eggs",
    "flour",
    "green beans",
    "ham",
    "cream",
    "mushrooms",
    "spinach",
    "strawberries",
    "sweet potato",
    "orange",
    "broccoli",
    "beer can",
    "soda can",
    "hot sauce bottle",
]


def prepare_yolo_world_for_kitchen_ingredients(output_path="kitchen-world.pt"):
    """download yolo and configure ingredient labels"""
    model = YOLOWorld("yolov8s-worldv2.pt")
    model.set_classes(INGREDIENTS)
    model.save(output_path)


def load_pretrained_yolo_world_model():
    """load the configured model"""
    return YOLOWorld("kitchen-world.pt")


def detect_objects_in_image(model, image_file):
    """return detected labels and confidence scores"""
    with Image.open(image_file) as image:
        results = model.predict(image.convert("RGB"), verbose=False)

    detections = []
    for result in results:
        for box in result.boxes:
            detections.append(
                {
                    "name": result.names[int(box.cls.item())],
                    "confidence": float(box.conf.item()),
                }
            )
    return detections
