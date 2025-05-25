def classify_crop(crop_img, classifier):
    results = classifier(crop_img)[0]
    if results.probs is None:
        return "error", 0.0
    class_id = int(results.probs.top1)
    class_name = results.names[class_id]
    score = float(results.probs.data[class_id])
    return class_name, score
