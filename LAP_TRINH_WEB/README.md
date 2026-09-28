# BÁO CÁO THỰC HÀNH MÔN LẬP TRÌNH WEB

- **Họ và tên sinh viên:** Nguyễn Duy
- **Mã sinh viên:** K235480106102
- **Lớp:** K59KMT
- **Máy chủ triển khai:** Ubuntu 22.04 LTS (`192.168.199.137`)
- **Tên miền:** `laptrinhwebn4.id.vn` / `sub.laptrinhwebn4.id.vn`

---

##  BÀI 1: CẤU HÌNH MULTI-SITE NGINX VỚI DOCKER & CLOUDFLARE

### 1. Yêu cầu & Nội dung thực hiện
* **Mục tiêu:** Cấu hình Web Server Nginx chạy đa trang web (Multi-site) trên môi trường Docker Container và định tuyến qua tên miền Cloudflare.
* **Các công việc đã làm:**
  1. Dùng **Docker Compose** khởi chạy container Nginx phục vụ 2 thư mục web riêng biệt (`web1` và `web2`).
  2. Cấu hình file `default.conf` của Nginx để phân luồng 2 tên miền/subdomain:
     - Domain chính `laptrinhwebn4.id.vn` trỏ về thư mục `web1`.
     - Subdomain `sub.laptrinhwebn4.id.vn` trỏ về thư mục `web2`.
  3. Cấu hình DNS trên Cloudflare và triển khai **Cloudflared Tunnel** để đưa các trang web ra ngoài Internet an toàn với mã hóa SSL/TLS.

### 2. Kết quả đạt được
* Truy cập `http://laptrinhwebn4.id.vn` (hoặc `http://192.168.199.137`): Hiển thị thành công trang giao diện chính của Web 1.
* Truy cập `http://sub.laptrinhwebn4.id.vn`: Hiển thị thành công trang giao diện phụ của Web 2.
* Hệ thống phản hồi nhanh, tự động chuyển hướng và hoạt động ổn định trên container Nginx.

---

##  BÀI 2: TẠO API TRÊN NODE-RED VỚI ĐỊNH DẠNG JSON & GỌI BẰNG FETCH API

### 1. Yêu cầu & Nội dung thực hiện
* **Mục tiêu:** Xây dựng backend API trả về định dạng JSON bằng Node-RED, cấu hình Nginx Reverse Proxy để chuyển tiếp API và viết mã JavaScript trên giao diện web để gọi API không đồng bộ.
* **Các công việc đã làm:**
  1. **Cấu hình Reverse Proxy trên Nginx:** Thêm quy tắc điều hướng tuyến đường `/api/` tự động chuyển tiếp yêu cầu sang container Node-RED chạy ở cổng `1880` (`proxy_pass http://nodered:1880/api/;`).
  2. **Tạo Endpoint API trong Node-RED:**
     - Thiết lập HTTP In node lắng nghe phương thức `GET` tại URL `/api/engdi`.
     - Viết mã trong Function node trả về cấu trúc JSON chứa mã trạng thái thành công, thông điệp phản hồi và danh sách thông tin cá nhân/nhóm sinh viên:
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
  3. **Tích hợp JavaScript Fetch API vào HTML (`index.html`):** Viết hàm `goiApiNodeRed()` sử dụng Fetch API gọi tới đường dẫn `/api/engdi`, xử lý dữ liệu JSON trả về và tự động hiển thị danh sách sinh viên lên trang web mà không cần tải lại trang.

### 2. Kết quả đạt được
* **Kiểm tra API trực tiếp:** Truy cập `http://192.168.199.137/api/engdi` trên trình duyệt trả về chuỗi JSON chuẩn chứa thông tin của sinh viên Nguyễn Duy.
* **Giao diện Web đồng bộ:** Khi nhấn nút **"GỌI API (/api/engdi)"** trên trang web, dữ liệu được tải thành công từ Node-RED và hiển thị đẹp mắt, rõ ràng lên màn hình người dùng.

---

## 🛠️ HƯỚNG DẪN KHỞI CHẠY DỰ ÁN

```bash
# Khởi chạy toàn bộ hệ thống bằng Docker Compose
docker compose up -d

# Kiểm tra trạng thái các container
docker compose ps