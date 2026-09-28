# BÁO CÁO THỰC HÀNH MÔN LẬP TRÌNH WEB

## 1. MÔN LẬP TRÌNH WEB

### Cấu hình Môi trường
- **Hệ điều hành:** Ubuntu Server 22.04 LTS (Chạy trên môi trường ảo hóa VMware)
- **Công nghệ & Công cụ sử dụng:**
  - **Docker & Docker Compose:** Đóng gói, quản lý và vận hành toàn bộ hạ tầng dịch vụ dưới dạng Container độc lập.
  - **Nginx (Reverse Proxy & Web Server):** Điều hướng truy cập Multi-site, định tuyến API và xử lý tĩnh.
  - **Node-RED:** Xây dựng backend API trả về định dạng JSON xử lý không đồng bộ.
  - **MariaDB:** Cơ sở dữ liệu quan hệ (Relational Database) lưu trữ dữ liệu người dùng và hệ thống.
  - **phpMyAdmin:** Giao diện trực quan trên web quản lý Cơ sở dữ liệu MariaDB.
  - **Cloudflare & Cloudflared Tunnel:** Quản lý tên miền, cấu hình DNS và thiết lập đường truyền mã hóa SSL/TLS ra Internet.

**Thông tin sinh viên thực hiện:**
- **Họ và tên:** Nguyễn Duy
- **Mã sinh viên:** K235480106102
- **Lớp:** K59KMT
- **Địa chỉ IP Server:** `192.168.199.137`
- **Tên miền:** `laptrinhwebn4.id.vn` / `sub.laptrinhwebn4.id.vn`

---

##  BÀI 1: CẤU HÌNH MULTI-SITE NGINX VỚI DOCKER & CLOUDFLARE

### 1. Yêu cầu & Nội dung thực hiện
* **Mục tiêu:** Cấu hình Web Server Nginx chạy đa trang web (Multi-site) trên môi trường Docker Container và định tuyến an toàn qua tên miền Cloudflare.
* **Chi tiết các bước thực hiện:**
  1. **Khởi tạo Hạ tầng dịch vụ:** Sử dụng `docker-compose.yml` định nghĩa và khởi chạy tập trung các dịch vụ: Nginx, Node-RED, MariaDB (port `3306`) và phpMyAdmin (port `8080`).
  2. **Cấu hình Đa tên miền (Multi-site Virtual Hosts):**
     - Tạo 2 thư mục mã nguồn riêng biệt (`web1` và `web2`) chứa giao diện HTML/CSS.
     - Cấu hình file `default.conf` của Nginx để lắng nghe cổng `80` và điều hướng dựa theo `server_name`:
       - Domain chính `laptrinhwebn4.id.vn` trỏ nội dung về thư mục `/usr/share/nginx/html/web1`.
       - Subdomain `sub.laptrinhwebn4.id.vn` trỏ nội dung về thư mục `/usr/share/nginx/html/web2`.
  3. **Định tuyến tên miền qua Cloudflare Tunnel:**
     - Thiết lập bản ghi DNS trên Cloudflare trỏ tên miền về IP Server (`192.168.199.137`).
     - Kích hoạt Cloudflared Tunnel bảo mật kết nối mã hóa HTTPS/SSL mà không cần mở port thủ công trên Router.

### 2. Kết quả đạt được
* Truy cập `http://laptrinhwebn4.id.vn`: Phản hồi chính xác trang giao diện chính của **Web 1**.
* Truy cập `http://sub.laptrinhwebn4.id.vn`: Phản hồi chính xác trang giao diện phụ của **Web 2**.
* Quản lý Cơ sở dữ liệu qua giao diện web bằng cách truy cập `http://192.168.199.137:8080` (phpMyAdmin).
* Hệ thống hoạt động mượt mà, cách ly tài nguyên tốt giữa các dịch vụ container.

---

##  BÀI 2: TẠO API TRÊN NODE-RED VỚI ĐỊNH DẠNG JSON & GỌI BẰNG FETCH API

### 1. Yêu cầu & Nội dung thực hiện
* **Mục tiêu:** Xây dựng Backend API trả về dữ liệu định dạng JSON bằng Node-RED, cấu hình Nginx làm Reverse Proxy để chuyển tiếp Yêu cầu (Request) và viết mã JavaScript trên Frontend để gọi API không đồng bộ.
* **Chi tiết các bước thực hiện:**
  1. **Cấu hình Nginx Reverse Proxy cho API:**
     - Bổ sung khối `location /api/` trong cấu hình Nginx để điều hướng toàn bộ request bắt đầu bằng `/api/` tới container Node-RED chạy tại `http://nodered:1880/api/`.
  2. **Tạo Backend Endpoint trong Node-RED:**
     - Kéo thả khối **HTTP In node** thiết lập phương thức `GET` tại đướng dẫn `/api/engdi`.
     - Dùng **Function node** để thiết lập Header `Content-Type: application/json` và khởi tạo nội dung JSON phản hồi chứa thông tin thành viên:
       ```javascript
       msg.headers = { 'Content-Type': 'application/json' };
       msg.payload = {
           "ok": 1,
           "msg": "Kết nối API Node-RED thành công!",
           "dssv": [
               {
                   "name": "Nguyễn Duy",
                   "msv": "K235480106102",
                   "role": "Nhóm trưởng"
               }
           ]
       };
       return msg;
       ```
     - Nối với **HTTP Response node** để xuất dữ liệu trả về cho client.
  3. **Tích hợp JavaScript Fetch API vào HTML Frontend (`index.html`):**
     - Lập trình hàm `goiApiNodeRed()` bằng Fetch API gọi tới tuyến đường `/api/engdi`.
     - Nhận chuỗi JSON, bóc tách mảng `dssv` và render dữ liệu động lên giao diện HTML mà không làm tải lại (reload) trang web.

### 2. Kết quả đạt được
* **Kiểm tra API Backend:** Truy cập trực tiếp `http://192.168.199.137/api/engdi` trả về kết quả JSON chuẩn hóa.
* **Tương tác Frontend:** Khi người dùng bấm nút **"GỌI API (/api/engdi)"**, trang web tự động gửi request, xử lý và hiển thị thông tin của Nguyễn Duy lên màn hình ngay lập tức.

---

