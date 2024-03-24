import os
import numpy as np
import cv2
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
count_objects = {}

# Define the directory where annotated images will be saved
ANNOTATED_IMAGES_DIR = "annotated_images"
if not os.path.exists(ANNOTATED_IMAGES_DIR):
    os.makedirs(ANNOTATED_IMAGES_DIR)

def detect_objects(image_path):
    global count_objects  # Use the global count_objects dictionary
    # Load pre-trained YOLO model and labels
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")  # Update paths
    if net.empty():
        return "Failed to load YOLO model"
    
    classes = []
    with open("coco.names", "r") as f:  # Update path
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    if not output_layers:
        return "Failed to get output layers"
    
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        return "Failed to read image"
    height, width, _ = img.shape
    
    # Perform object detection
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    # Process the detected objects
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    # Draw bounding boxes and labels on the image
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if label in count_objects:
                count_objects[label] += 1
            else:
                count_objects[label] = 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
    
    # Save the annotated image
    annotated_image_path = os.path.join(ANNOTATED_IMAGES_DIR, image_path)
    cv2.imwrite(annotated_image_path, img)
    
    return annotated_image_path

def delete_annotated_images():
    for filename in os.listdir(ANNOTATED_IMAGES_DIR):
        file_path = os.path.join(ANNOTATED_IMAGES_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def upload_file():
    global count_objects  # Use the global count_objects dictionary
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        file_path = os.path.join(current_directory, filename)
        if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            os.remove(file_path)

    if 'files[]' not in request.files:
        resp = jsonify({
            "message": 'No file part in the request',
            "status": 'failed'
        })
        resp.status_code = 400
        return resp
  
    file = request.files.getlist('files[]')[0]
    image_path = file.filename
    file.save(image_path)

    # Delete existing annotated images
    delete_annotated_images()

    # Perform object detection
    annotated_image_path = detect_objects(image_path)

    # Return the URL of the annotated image and reset count_objects
    annotated_image_url = request.host_url + "annotated/" + os.path.basename(annotated_image_path)
    response_data = {
        "message": "Object detection completed",
        "status": "success",
        "annotated_image_url": annotated_image_url,
        "count": count_objects
    }
    count_objects = {}  # Clear count_objects
    resp = jsonify(response_data)
    return resp

@app.route('/annotated/<path:filename>')
def annotated_image(filename):
    return send_from_directory(ANNOTATED_IMAGES_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
