import cv2

from ultralytics import YOLO, solutions

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("data/nhanvien.mp4")
assert cap.isOpened(), "Lỗi đọc video"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Khai báo vùng
region_points = [(230, 370), (300, 350), (300, 10), (230, 10)]

classes_to_count = [0]
# lưu video
video_writer = cv2.VideoWriter("outputs/nhanvien.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Đếm đối tượng
counter = solutions.ObjectCounter(
    view_img=True,
    reg_pts=region_points,
    classes_names=model.names,
    draw_tracks=True,
    line_thickness=2,
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("không có frame.")
        break
    tracks = model.track(im0, persist=True, show=False,classes= classes_to_count)

    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()