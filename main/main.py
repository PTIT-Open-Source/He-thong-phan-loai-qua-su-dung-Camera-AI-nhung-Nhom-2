import cv2
import numpy as np
import pandas as pd
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from collections import defaultdict, deque, Counter
from ultralytics import YOLO
import datetime
import os
import time

glutInit()

model = YOLO("best_full_integer_quant.tflite")
cap = cv2.VideoCapture(0)

# Lich su theo doi va dem vat the vuot qua duong giua
lich_su_theo_doi = defaultdict(lambda: deque(maxlen=10))
dem_vat_the = defaultdict(int)

# Cac thong so hien thi
chieu_rong_khung_hinh = 640
chieu_cao_khung_hinh = 480
vi_tri_duong_giua = chieu_rong_khung_hinh // 2
id_texture = None

# Thu muc Excel cho dem vat the (khong thay doi)
THU_MUC_EXCEL = "/home/hedieuhanh/excel"
os.makedirs(THU_MUC_EXCEL, exist_ok=True)

def lay_ten_tep_excel():
    ngay_hom_nay = datetime.datetime.now().strftime("%d_%m_%Y")
    return os.path.join(THU_MUC_EXCEL, f"{ngay_hom_nay}.xlsx")

def cap_nhat_va_luu_excel():
    tep_excel = lay_ten_tep_excel()
    df = pd.DataFrame(list(dem_vat_the.items()), columns=["Class", "Count"])
    with pd.ExcelWriter(tep_excel, mode="w", engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    print(f"Luu file Excel: {tep_excel}")
    return tep_excel

# --- Phan ghi log cac khung hinh ---
LOG_DETECTION_DIR = "/home/hedieuhanh/detection_log"
os.makedirs(LOG_DETECTION_DIR, exist_ok=True)
detection_logs = []  # Danh sach chua log cua tung khung hinh
frame_index = 0    # Bien dem khung hinh

def lay_ten_log_file():
    ngay_hom_nay = datetime.datetime.now().strftime("%d_%m_%Y")
    return os.path.join(LOG_DETECTION_DIR, f"detection_log_{ngay_hom_nay}.log")

def cap_nhat_va_luu_detection_log():
    tep_log = lay_ten_log_file()
    with open(tep_log, "w") as f:
        for log in detection_logs:
            f.write(log + "\n")
    print(f"Luu detection log file: {tep_log}")

# --- Khoi tao OpenGL ---
def khoi_tao_opengl():
    global id_texture
    glEnable(GL_TEXTURE_2D)
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, chieu_rong_khung_hinh, 0, chieu_cao_khung_hinh)
    id_texture = glGenTextures(1)

def cap_nhat_texture(khung_hinh):
    global id_texture
    khung_hinh = cv2.cvtColor(khung_hinh, cv2.COLOR_BGR2RGB)
    khung_hinh = cv2.flip(khung_hinh, 0)
    glBindTexture(GL_TEXTURE_2D, id_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, chieu_rong_khung_hinh, chieu_cao_khung_hinh, 0, GL_RGB, GL_UNSIGNED_BYTE, khung_hinh)

def ve_khung_hinh():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, id_texture)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(chieu_rong_khung_hinh, 0)
    glTexCoord2f(1, 1); glVertex2f(chieu_rong_khung_hinh, chieu_cao_khung_hinh)
    glTexCoord2f(0, 1); glVertex2f(0, chieu_cao_khung_hinh)
    glEnd()
    
def ve_duong():
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(vi_tri_duong_giua, 0)
    glVertex2f(vi_tri_duong_giua, chieu_cao_khung_hinh)
    glEnd()

def ve_hop_bao(boxes, track_ids, class_ids, confidences):
    glColor3f(0.0, 1.0, 0.0)
    for (x, y, w, h), track_id, cls, conf in zip(boxes, track_ids, class_ids, confidences):
        x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1, chieu_cao_khung_hinh - y1)
        glVertex2f(x2, chieu_cao_khung_hinh - y1)
        glVertex2f(x2, chieu_cao_khung_hinh - y2)
        glVertex2f(x1, chieu_cao_khung_hinh - y2)
        glEnd()
        ve_chu(f"ID {track_id} ({cls}) {conf:.2f}", x1, chieu_cao_khung_hinh - y1 - 10)

def ve_chu(chu, x, y):
    glDisable(GL_TEXTURE_2D)
    glColor3f(0.0, 1.0, 0.0)
    glRasterPos2f(x, y)
    for ky_tu in chu:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ky_tu))
    glEnable(GL_TEXTURE_2D)

def hien_thi():
    global frame_index, cap
    start_pre = time.time()
    ret, khung_hinh = cap.read()
    if not ret:
        glfw.set_window_should_close(cua_so, True)
        return
    cap_nhat_texture(khung_hinh)
    end_pre = time.time()
    
    start_inf = time.time()
    results = model.track(khung_hinh, imgsz=320, persist=True, iou=0.3)
    end_inf = time.time()
    
    # Tien hanh xu ly ket qua (postprocess)
    start_post = time.time()
    boxes, track_ids, class_ids, confidences = [], [], [], []
    conf_threshold = 0.5
    if results and results[0].boxes is not None and results[0].boxes.xywh is not None:
        boxes = results[0].boxes.xywh.cpu().tolist()
        confidences = results[0].boxes.conf.cpu().tolist() if results[0].boxes.conf is not None else []
        track_ids = results[0].boxes.id.cpu().int().tolist() if results[0].boxes.id is not None else []
        class_ids = results[0].boxes.cls.cpu().int().tolist()
        
        filtered_data = [(b, tid, cid, conf) for b, tid, cid, conf in zip(boxes, track_ids, class_ids, confidences) if conf >= conf_threshold]
        if filtered_data:
            boxes, track_ids, class_ids, confidences = zip(*filtered_data)
        else:
            boxes, track_ids, class_ids, confidences = [], [], [], []
        
        # Cap nhat lich su va dem khi doi tuong vuot qua duong giua
        for (x, _, _, _), track_id in zip(boxes, track_ids):
            lich_su_theo_doi[track_id].append(x)
            if len(lich_su_theo_doi[track_id]) > 1 and lich_su_theo_doi[track_id][-2] < vi_tri_duong_giua <= lich_su_theo_doi[track_id][-1]:
                index = track_ids.index(track_id)
                dem_vat_the[class_ids[index]] += 1
    end_post = time.time()
    
    # Tinh thoi gian cac buoc (ms)
    preprocess_time = (end_pre - start_pre) * 1000
    inference_time  = (end_inf - start_inf) * 1000
    postprocess_time = (end_post - start_post) * 1000

    # Cap nhat file Excel dem vat the
    tep_excel = cap_nhat_va_luu_excel()
    
    # Log thong tin detection cua khung hinh hien tai
    resolution = "320x320"
    if hasattr(model, "names"):
        class_names_list = [model.names[c] for c in class_ids] if class_ids else []
    else:
        class_names_list = [str(c) for c in class_ids]
    
    if class_names_list:
        counter = Counter(class_names_list)
        class_summary = ", ".join(f"{count} {cls}" for cls, count in counter.items())
    else:
        class_summary = "0 objects"
    
    detection_info = f"{frame_index}: {resolution} {class_summary}, {inference_time:.1f}ms"
    speed_info = f"Speed: {preprocess_time:.1f}ms preprocess, {inference_time:.1f}ms inference, {postprocess_time:.1f}ms postprocess per image at shape (1, 3, 320, 320)"
    excel_info = f"Luu file Excel: {tep_excel}"
    
    detection_logs.append(detection_info)
    detection_logs.append(speed_info)
    detection_logs.append(excel_info)
    
    # Luu detection log vao file .log
    cap_nhat_va_luu_detection_log()
    
    glClear(GL_COLOR_BUFFER_BIT)
    ve_khung_hinh()
    ve_duong()
    ve_hop_bao(boxes, track_ids, class_ids, confidences)

    y_offset = 20
    for cls, count in dem_vat_the.items():
        ve_chu(f"Class {cls}: {count}", 10, chieu_cao_khung_hinh - y_offset)
        y_offset += 20

    glfw.swap_buffers(cua_so)
    glfw.poll_events()
    
    frame_index += 1

def chuong_trinh_chinh():
    global cua_so
    if not glfw.init():
        return
    cua_so = glfw.create_window(chieu_rong_khung_hinh, chieu_cao_khung_hinh, "YOLO OpenGL", None, None)
    if not cua_so:
        glfw.terminate()
        return
    glfw.make_context_current(cua_so)
    khoi_tao_opengl()
    while not glfw.window_should_close(cua_so):
        hien_thi()
    cap.release()
    glfw.terminate()

if __name__ == "__main__":
    chuong_trinh_chinh()
