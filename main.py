import cv2
from ultralytics import YOLO


model = YOLO('best.pt')



class_values = {
    0: 0.5,  # Half Pound
    1: 1.0,  # One Pound
    2: 0.25  # Quarter Pound
}


def detect_and_calculate(image_path):

    results = model(image_path)[0]

    total_sum = 0
    counts = {"One Pound": 0, "Half Pound": 0, "Quarter Pound": 0}


    img = results.orig_img.copy()


    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if conf > 0.5:

            val = class_values.get(cls_id, 0)
            total_sum += val


            class_name = results.names[cls_id]
            counts[class_name] = counts.get(class_name, 0) + 1


            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{class_name}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


    text = f"Total: {total_sum} EGP"
    cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    print(f"Result: {counts}")
    print(f"Total: {total_sum} pounds")


    cv2.imwrite('result_output3.jpg', img)
    return img



detect_and_calculate(r'C:\Users\fajra\PycharmProjects\Coin_Detection\project-1-at-2026-02-02-20-01-a5637ce7\images\264c94b1-photo_2026-02-02_16-35-45.jpg')