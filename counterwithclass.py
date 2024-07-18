import cv2

from ultralytics import YOLO, solutions

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("data\\nhanvien.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
'''
#line_points = [(540, 50), (540, 350)] # chai
#line_points = [(300, 70), (300, 350)] # vacxin
#line_points = [(200, 80), (200, 300)] # vacxin1
#line_points = [(200, 80), (200, 300)] # vacxin2
line_points = [(200, 20), (200, 400)] # vacxin3
#classes_to_count = [39]  # chai
khai báo line khi vật đi qua và đối tượng muốn đọc
'''
classes_to_count = [0]  # vali
line_points = [(210, 340), (300, 320)]
# Lưu video
video_writer = cv2.VideoWriter("outputs/sc1.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Đếm đối tượng 
counter = solutions.ObjectCounter(
    view_img=True,
    view_out_counts=True,
    reg_pts=line_points,
    classes_names=model.names,
    draw_tracks=False,
    line_thickness=2,
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Hết frame")
        break
    tracks = model.track(im0, persist=True, show=False,  classes=classes_to_count)

    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()