# Video-Proccessing-and-Storaging-Service

# Project tham khảo: https://github.com/superdesk/video-server

# Thành viên nhóm 23
1. Trần Minh Mẫn - 20110301
2. Nguyễn Minh Sơn - 20110713
3. Hà Vĩ Khang - 20110657

## Project Structure
<pre>
<b>video-server</b>
├── src
│   ├── videoserver
│   │   ├── apps
│   │   │   ├── projects                      (chứa các file routes, task)
│   │   │   ├── swagger
|   │   │   │   └── static                    (chứa các file liên quan đến ui của swagger)
|   │   │   │   └── templates                 (chứa file index.html của swagger)
│   │   ├── lib
│   │   │   ├── storage                       (lưu trữ file system)
│   │   │   ├── video_editor                  (chứa cái file liên quan đến việc thực hiện edit video sử dụng ffmpeg)
│   │   │   │   └── script               
├── tests
│   ├── api                                   (chứa các api để test việc thêm, sửa, xóa video và thumbnail)
│   ├── storage
│   |   └── fixtures                          (chứa hình ảnh và video dùng để test)
|   ├── video                                 (chứa file test các chức năng của thư viện ffmpeg)

</pre>

<br>
<br>
