# Video-Proccessing-and-Storaging-Service

# Project tham khảo: https://github.com/superdesk/video-server

# Link Report:
1. Báo cáo cuối kỳ: https://docs.google.com/document/d/1Z5GAFFelnkUP0pqBmEVgdWkDBrQwJW0yPogDbaatizc/edit?usp=sharing
2. Báo cáo SRS: https://docs.google.com/document/d/1OOjgWxlsUVJEMIwTfeKHEU3K7AaujnD9/edit?usp=share_link&ouid=109879817859511417201&rtpof=true&sd=true
3. OKRs: https://docs.google.com/spreadsheets/d/16YGwkaIgDvp5gyVPwIHJyktZSaj9x7U-/edit?usp=share_link&ouid=109879817859511417201&rtpof=true&sd=true
4. Quản lý rủi ro: https://docs.google.com/document/d/1xeHImiNBFAl98cjVxKHSzowT7xfWULS3/edit?usp=sharing&ouid=109879817859511417201&rtpof=true&sd=true
5. Báo cáo plan test: https://docs.google.com/spreadsheets/d/1YdNVWXL9qwR6NsLMSltpClcjhdWm7yqK/edit?usp=sharing&ouid=109879817859511417201&rtpof=true&sd=true
6. Hướng dẫn chạy project: https://docs.google.com/document/d/1BIRsB4beaSb_My790LbNdJNzbOZpOTVH/edit?usp=sharing&ouid=109879817859511417201&rtpof=true&sd=true

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
