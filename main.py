import os
import cv2
from ultralytics import YOLO

from utils.sliding_window_utils import sliding_window_tiles
from utils.merge_utils import merge_by_proximity
from utils.classification_utils import classify_crop
from utils.draw_utils import draw_label_with_background

# ==== 輸入參數 ====
detection_model_path = "model/yolo_box/best.pt"
classifier_model_path = "model/yolo_classify/best.pt"

input_folder = "input"     
output_folder = "output"   

tile_size = 1024
overlap = 200
eps_distance = 150  # DBSCAN合併距離閾值（像素）

# ==== 模型載入 ====
detector = YOLO(detection_model_path)
classifier = YOLO(classifier_model_path)

def process_image(image_path, output_path):
    img = cv2.imread(image_path)
    img_name = os.path.splitext(os.path.basename(image_path))[0]
    all_boxes = []

    # 切圖 + 偵測
    tiles = sliding_window_tiles(img, tile_size, overlap)
    for tile, x_offset, y_offset in tiles:
        results = detector(tile)[0]
        for box in results.boxes:
            xyxy = box.xyxy.cpu().numpy()[0]
            cls = int(box.cls)
            conf = float(box.conf)
            x1, y1, x2, y2 = xyxy
            x1 += x_offset
            x2 += x_offset
            y1 += y_offset
            y2 += y_offset
            all_boxes.append([x1, y1, x2, y2, conf, cls])

    # 合併框
    merged_boxes = merge_by_proximity(all_boxes, eps=eps_distance)

    # 分類每個框的內容
    for box in merged_boxes:
        x1, y1, x2, y2, conf, cls = box
        x1i, y1i, x2i, y2i = map(int, [x1, y1, x2, y2])
        crop = img[y1i:y2i, x1i:x2i]
        if crop.shape[0] == 0 or crop.shape[1] == 0:
            continue
        label, score = classify_crop(crop, classifier)
        if label == "health":
            color = (0, 255, 0)
            cv2.rectangle(img, (x1i, y1i), (x2i, y2i), color, 2)
            draw_label_with_background(img, label, x1i, y1i, color)
        elif label == "stocking":
            color = (0, 0, 255)
            cv2.rectangle(img, (x1i, y1i), (x2i, y2i), color, 2)
            draw_label_with_background(img, label, x1i, y1i, color)
        elif label == "error":
            color = (255, 0, 0)
            cv2.rectangle(img, (x1i, y1i), (x2i, y2i), color, 2)
            draw_label_with_background(img, 'TBC', x1i, y1i, color)

    # 儲存圖片
    os.makedirs(output_path, exist_ok=True)
    save_path = os.path.join(output_path, f"{img_name}.jpg")
    cv2.imwrite(save_path, img)
    print(f"✅ 已完成: {img_name}")

def process_folder():
    for fname in os.listdir(input_folder):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif')):
            image_path = os.path.join(input_folder, fname)
            process_image(image_path, output_folder)

if __name__ == "__main__":
    process_folder()
