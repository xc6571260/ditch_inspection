import cv2

def draw_label_with_background(img, label, x, y, color, font_scale=1.2, font_thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = str(label)
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x, text_y = x, y - 10
    if text_y - text_height - baseline < 0:
        text_y = y + text_height + 10
    cv2.rectangle(
        img,
        (text_x, text_y - text_height - baseline),
        (text_x + text_width, text_y + baseline),
        color,
        thickness=-1
    )
    cv2.putText(
        img,
        text,
        (text_x, text_y),
        font,
        font_scale,
        (0, 0, 0),
        font_thickness
    )
