import numpy as np
from sklearn.cluster import DBSCAN

def merge_by_proximity(boxes, eps=150):
    if not boxes:
        return []
    centers = [((b[0]+b[2])/2, (b[1]+b[3])/2) for b in boxes]
    cls_list = [b[5] for b in boxes]
    merged_results = []
    for cls_id in set(cls_list):
        class_indices = [i for i, c in enumerate(cls_list) if c == cls_id]
        class_centers = [centers[i] for i in class_indices]
        class_boxes = [boxes[i] for i in class_indices]
        if len(class_boxes) == 1:
            merged_results.append(class_boxes[0])
            continue
        db = DBSCAN(eps=eps, min_samples=1).fit(class_centers)
        labels = db.labels_
        for label in set(labels):
            group = [class_boxes[i] for i in range(len(labels)) if labels[i] == label]
            x1s = [b[0] for b in group]
            y1s = [b[1] for b in group]
            x2s = [b[2] for b in group]
            y2s = [b[3] for b in group]
            confs = [b[4] for b in group]
            merged_box = [
                min(x1s), min(y1s), max(x2s), max(y2s),
                max(confs), cls_id
            ]
            merged_results.append(merged_box)
    return merged_results
