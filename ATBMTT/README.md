# BÁO CÁO BÀI TẬP MÔN AN TOÀN VÀ BẢO MẬT THÔNG TIN

## Câu 1: Thuật toán mã hóa đối xứng DES và AES

### 1. Thuật toán DES (Data Encryption Standard)
* **Mô tả**: Là thuật toán mã hóa khối (block cipher) đối xứng mã hóa dữ liệu theo từng khối 64-bit sử dụng khóa có độ dài 56-bit (cùng 8-bit kiểm tra parities).
* **Quy trình mã hóa/giải mã**:
  * **Mã hóa**: Khối 64-bit trải qua phép hoán vị ban đầu (IP), qua 16 vòng mạng Feistel (kết hợp các phép thế S-Box, P-Box và tính XOR với khóa con), cuối cùng là phép hoán vị nghịch đảo ($IP^{-1}$).
  * **Giải mã**: Thực hiện quy trình ngược lại hoàn toàn với việc áp dụng các khóa con theo thứ tự ngược từ 16 về 1.

### 2. Thuật toán AES (Advanced Encryption Standard)
* **Mô tả**: Là tiêu chuẩn mã hóa đối xứng thay thế DES, hỗ trợ kích thước khối cố định 128-bit và khóa có độ dài 128, 192 hoặc 256-bit.
* **Quy trình mã hóa/giải mã**:
  * Dựa trên mạng thay thế - hoán vị (Substitution-Permutation Network).
  * Quy trình gồm 4 bước chính lặp lại qua các vòng ($N_r = 10, 12, 14$ tùy độ dài khóa):
    1. **SubBytes**: Thế phi tuyến từng byte qua bảng S-Box.
    2. **ShiftRows**: Dịch chuyển các hàng trong ma trận trạng thái.
    3. **MixColumns**: Trộn các cột bằng phép nhân ma trận trên trường Galois $GF(2^8)$.
    4. **AddRoundKey**: XOR ma trận trạng thái với khóa con của vòng đó.
  * **Giải mã**: Áp dụng các phép biến đổi ngược tương ứng (InvSubBytes, InvShiftRows, InvMixColumns, AddRoundKey).

---

## Câu 2: Thuật toán mã hóa bất đối xứng RSA

### 1. Nguyên lý sinh cặp khóa (Public Key & Private Key)
1. Chọn 2 số nguyên tố lớn ngẫu nhiên $p$ và $q$.
2. Tính $n = p \times q$.
3. Tính hàm Euler: $\phi(n) = (p - 1)(q - 1)$.
4. Chọn một số nguyên $e$ sao cho $1 < e < \phi(n)$ và $gcd(e, \phi(n)) = 1$ (Thường chọn $e = 65537$).
5. Tính $d$ sao cho $d \cdot e \equiv 1 \pmod{\phi(n)}$.
6. **Kết quả**:
   * **Khóa công khai (Public Key)**: $(e, n)$
   * **Khóa bí mật (Private Key)**: $(d, n)$

### 2. Quy trình Mã hóa và Giải mã
* **Mã hóa**: $C = M^e \pmod n$
* **Giải mã**: $M = C^d \pmod n$

---

## Câu 3: Mô hình áp dụng RSA & So sánh với AES

### 1. Các mô hình áp dụng thuật toán RSA
* **Xác thực người nhận (Mã hóa bảo mật - Confidentiality)**:
  * Người gửi dùng **Public Key của người nhận** để mã hóa. Chỉ có người nhận có **Private Key** mới giải mã được.
* **Xác thực người gửi (Chữ ký số - Digital Signature)**:
  * Người gửi dùng **Private Key của chính mình** để ký/mã hóa hash của thông điệp. Người nhận dùng **Public Key của người gửi** để kiểm tra tính toàn vẹn và xác thực nguồn gốc.
* **Kết hợp cả hai (Confidentiality + Authentication)**:
  * Người gửi ký bằng **Private Key của mình**, sau đó mã hóa toàn bộ bằng **Public Key của người nhận**.

### 2. So sánh thời gian mã hóa/giải mã: RSA vs AES
| Tiêu chí | AES (Symmetric) | RSA (Asymmetric) |
| :--- | :--- | :--- |
| **Tốc độ mã hóa/giải mã** | **Cực nhanh** (Thao tác trên bit/byte, hỗ trợ phần cứng). | **Rất chậm** (Do tính toán lũy thừa trên số nguyên cực lớn). |
| **Kích thước khóa** | Nhỏ (128 - 256 bit). | Lớn (2048 - 4096 bit). |
| **Mục đích chính** | Mã hóa dữ liệu khối lượng lớn. | Trao đổi khóa, Chữ ký số, Xác thực. |

### 3. Mô hình kết hợp sức mạnh (Mã hóa lai - Hybrid Cryptosystem)
Để tối ưu cả tốc độ và độ bảo mật:
1. **Bước 1**: Tạo một khóa phiên đối xứng ngẫu nhiên (Session Key) dùng **AES**.
2. **Bước 2**: Dùng **AES** mã hóa toàn bộ dữ liệu thực tế bằng Session Key (Tối ưu tốc độ mã hóa).
3. **Bước 3**: Dùng **Public Key RSA của người nhận** để mã hóa Session Key (Bảo mật quá trình truyền khóa).
4. **Bước 4**: Gửi cả gói `[Dữ liệu đã mã hóa AES] + [Session Key đã mã hóa RSA]` sang bên nhận.
5. **Bước 5**: Người nhận dùng **Private Key RSA** để giải mã lấy Session Key, sau đó dùng Session Key giải mã dữ liệu chính.
