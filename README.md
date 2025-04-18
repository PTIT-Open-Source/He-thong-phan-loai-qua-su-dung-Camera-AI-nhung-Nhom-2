# 🥭 HỆ THỐNG PHÂN LOẠI QUẢ SỬ DỤNG CAMERA AI NHÚNG

## 🎯 Mục tiêu dự án

Dự án xây dựng **hệ thống nhận dạng và phân loại quả** theo thời gian thực sử dụng **camera AI nhúng**. Hệ thống sẽ nhận diện và đếm số lượng các loại quả, hiển thị kết quả trực tiếp qua **OpenGL**, đồng thời ghi nhận số liệu vào **file Excel** và gửi lên **máy chủ web** qua giao thức **MQTT**.

---

## 🛠️ Công nghệ sử dụng

- **Ngôn ngữ lập trình:** Python  
- **Các thư viện chính:**
  - `OpenCV`, `NumPy`, `Pandas` – xử lý ảnh và dữ liệu
  - `Ultralytics YOLOv8` – nhận diện và tracking đối tượng
  - `OpenGL`, `GLFW`, `GLUT` – hiển thị trực tiếp ảnh và thông tin nhận dạng
  - `paho-mqtt`, `Flask` – giao tiếp MQTT và xây dựng giao diện web

- **Mô hình AI:** YOLOv8 phiên bản **TFLite (quantized)** cho thiết bị nhúng
- **Thiết bị sử dụng:** Raspberry Pi, máy tính cấu hình thấp, camera USB
- **Giao thức mạng:** MQTT (HiveMQ Cloud) với bảo mật **TLS**

---

## 🔧 Chức năng chính

### 🔹 1. **Nhận diện và hiển thị kết quả qua OpenGL**

- **Camera** quay video realtime và truyền vào hệ thống.
- **YOLOv8** xử lý ảnh và nhận diện các đối tượng quả.
- **OpenGL** hiển thị ảnh với các **bounding box** xung quanh các quả nhận diện được, bao gồm tên loại quả và ID của từng quả.
- **Tracking** các đối tượng qua các frame tiếp theo.
- Khi một quả vượt qua **vạch đỏ** giữa khung hình, hệ thống sẽ **đếm thêm 1** vào số lượng quả đó.
- **Kết quả đếm** và loại quả được lưu vào **file Excel** mỗi ngày.
- **Ghi log** chi tiết từng frame vào file `.log` để phục vụ giám sát và kiểm tra.

### 🔹 2. **Giao diện web và server nhận dữ liệu**

- **Server Flask** nhận file `.xlsx` và `.log` từ thiết bị qua MQTT.
- File được lưu trong các thư mục theo ngày như `/excel`, `/detection_log`.
- Giao diện **web đơn giản** hiển thị danh sách các file, cho phép người dùng tải về và xem thống kê.

---

## 🌟 Điểm nổi bật

- **Tối ưu cho thiết bị nhúng:** Sử dụng **TFLite**, giúp mô hình chạy nhanh và tiết kiệm tài nguyên trên Raspberry Pi hoặc các thiết bị cấu hình thấp.
- **Hiển thị trực tiếp qua OpenGL:** Giảm tải cho hệ thống, tăng tốc độ hiển thị mà không cần giao diện GUI phức tạp.
- **Tự động lưu log và Excel:** Dễ dàng theo dõi và kiểm tra dữ liệu trong suốt quá trình hoạt động.
- **Truyền dữ liệu an toàn qua MQTT:** **TLS** đảm bảo tính bảo mật khi truyền tải dữ liệu giữa thiết bị và server.

---

## 📌 Kết luận

Hệ thống giúp **phân loại quả thông minh** với độ chính xác cao, chạy ổn định trên nền tảng nhúng, và cung cấp công cụ để **giám sát từ xa** thông qua dữ liệu gửi về server. Đây là giải pháp hiệu quả cho các ứng dụng trong **nông nghiệp thông minh**, **kiểm tra chất lượng** và **phân loại sản phẩm** tự động.

---

## 📂 Các thư mục và tệp trong dự án

- `/src`: Mã nguồn của hệ thống
- `/models`: Tệp mô hình YOLOv8 đã huấn luyện
- `/logs`: Lưu trữ các file log và kết quả tracking
- `/excel`: Lưu trữ các file Excel chứa số liệu đếm quả
- `/backend: Chứa mã nguồn của server Flask, bao gồm việc tiếp nhận và xử lý các file Excel, log từ thiết bị, và cung cấp API cho giao diện web.
- `/frontend: Chứa mã nguồn của giao diện web được phát triển bằng Flask, hiển thị danh sách các file đã được upload, cho phép người dùng tải về và xem thống kê.
- `/testing: Thư mục dùng để chứa các tệp và mã nguồn dùng cho việc kiểm thử hệ thống, đảm bảo tất cả các tính năng hoạt động đúng.
- `/library: Thư viện bổ sung và các công cụ hỗ trợ khác mà hệ thống cần.
---

## 📝 Cài đặt

Để cài đặt và chạy dự án trên máy của bạn, làm theo các bước sau:

1. **Tải dự án về máy:**

   ```bash
   git clone https://github.com/yourusername/fruit-classification.git
   cd fruit-classification
   
2. **Tạo một môi trường ảo:**

   ```bash
   python -m venv venv
   source venv/bin/activate

3. **Cài thư viện cần thiết:**

   ```bash
   pip install -r requirements.txt

4. **Chạy hệ thống:**
   ```bash
   python /He-thong-phan-loai-qua-su-dung-Camera-AI-nhung-Nhom-2/main/main.py
   python /He-thong-phan-loai-qua-su-dung-Camera-AI-nhung-Nhom-2/backend/web.py

## 📂 Kiểm thử mô hình 

![Fruit Classification System](https://github.com/PTIT-Open-Source/He-thong-phan-loai-qua-su-dung-Camera-AI-nhung-Nhom-2/blob/main/testing/val_batch2_labels.jpg)
![Fruit Classification System](https://github.com/PTIT-Open-Source/He-thong-phan-loai-qua-su-dung-Camera-AI-nhung-Nhom-2/blob/main/testing/confusion_matrix.png)


