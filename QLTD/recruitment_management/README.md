# 🚀 Ứng dụng Quản lý Tuyển Dụng (QLTD)

## 🌟 Giới thiệu chung

Dự án **Ứng dụng Quản lý Tuyển Dụng (QLTD)** 
Là một dự án về website quản lý tuyển dụng giúp tạo cơ hội việc làm cho ứng viên và sự tuyển chọn của nhà tuyển dụng.
Mục tiêu chính của QLTD là nâng cao hiệu quả hoạt động tuyển dụng, giảm thiểu gánh nặng hành chính và cung cấp trải nghiệm mượt mà hơn cho cả nhà tuyển dụng và ứng viên.

-link repository:https://github.com/BaThuanPham/HuyenSuVietPhuong

 -Tính năng nổi bật

* **Quản lý Tin tuyển dụng:**
    * Tạo, chỉnh sửa, xem chi tiết và vô hiệu hóa các vị trí tuyển dụng.
    * Hỗ trợ mô tả công việc chi tiết và yêu cầu.
* **Quản lý Ứng viên:**
    * Thu thập và lưu trữ thông tin hồ sơ ứng viên (thông tin cá nhân, kinh nghiệm, học vấn, CV đính kèm).
    * Xem và tìm kiếm hồ sơ ứng viên dễ dàng.
* **Theo dõi Trạng thái Ứng tuyển:**
    * Hệ thống pipeline tuyển dụng rõ ràng với các trạng thái ứng tuyển tùy chỉnh (ví dụ: Đã nộp, Đã xem xét, Phỏng vấn vòng 1, Đã gửi đề nghị, Đã tuyển dụng, Bị từ chối).
    * Cập nhật trạng thái ứng viên theo thời gian thực.
* **Lên lịch Phỏng vấn:**
    * Công cụ lên lịch phỏng vấn trực quan.
    * Gửi thông báo và lời nhắc phỏng vấn tự động đến ứng viên và nhà tuyển dụng.
* **Hệ thống Phân quyền người dùng:**
    * Phân vai trò người dùng (ví dụ: Administrator, Recruiter, Applicant) với các quyền truy cập khác nhau.
    * Đảm bảo bảo mật và tính toàn vẹn dữ liệu.
* **Tìm kiếm & Lọc nâng cao:**
    * Tìm kiếm tin tuyển dụng và hồ sơ ứng viên dựa trên nhiều tiêu chí (vị trí, kỹ năng, kinh nghiệm, trạng thái...).

-Công nghệ sử dụng

Dự án này được xây dựng vững chắc trên các công nghệ và thư viện sau:

* **Backend:**
    * **Python 3.x** (Phiên bản khuyến nghị: 3.8+)
    * **Django Framework** (Phiên bản: `5.2.3`)
* **Database:**
    * **SQLite** (Mặc định cho môi trường phát triển)
* **Frontend:**
    * HTML5, CSS3, JavaScript
* **Công cụ:**
    * **pip** (Trình quản lý gói Python)
    * **virtualenv/venv** (Môi trường ảo để quản lý các gói dự án)

## ⚙ Hướng dẫn cài đặt và chạy ứng dụng cục bộ

Làm theo các bước dưới đây để thiết lập và chạy ứng dụng trên máy tính của bạn.

### 1. Yêu cầu Tiên quyết

* Đảm bảo Python 3.8+ và `pip` đã được cài đặt trên hệ thống của bạn.
* Đảm bảo Git đã được cài đặt.

### 2. Clone Repository

Mở **Terminal** (trên macOS/Linux) hoặc **Git Bash** (trên Windows) và chạy lệnh sau để sao chép dự án về máy tính:

```bash
# Di chuyển đến thư mục bạn muốn lưu trữ dự án (ví dụ: ổ D:).
# Đảm bảo đường dẫn không chứa dấu cách hoặc ký tự đặc biệt nếu không dùng dấu ngoặc kép.
# Ví dụ trên Windows:
cd D:/MyGitHubProjects

# Sao chép repository
git clone [https://github.com/BaThuanPham/HuyenSuVietPhuong.git](https://github.com/BaThuanPham/HuyenSuVietPhuong.git)

# Di chuyển vào thư mục gốc của repository
vd:cd HuyenSuVietPhuong

# Tiếp tục di chuyển vào thư mục chứa mã nguồn chính của ứng dụng Django (nơi có manage.py)

#Tạo và Kích hoạt Môi trường ảo
python -m venv venv
#Kích hoạt môi trường ảo
source venv/Scripts/activate
#Cài đặt các Thư viện phụ thuộc có trong requirements.txt
pip install -r requirements.txt
#Cấu hình Cơ sở dữ liệu và Biến môi trường

#Thực hiện Migrations và chạy ứng dụng (tạo superuser nếu muốn truy cập vào trang quản trị Django - admin)
python manage.py makemigrations # Chạy lệnh này nếu bạn đã tạo hoặc thay đổi các model
python manage.py migrate
python manage.py createsuperuser

#Chạy ứng dụng
python manage.py runserver
