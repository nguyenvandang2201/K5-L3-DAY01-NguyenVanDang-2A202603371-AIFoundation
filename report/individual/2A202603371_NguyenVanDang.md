# Báo cáo cá nhân — Day 01

- **Họ tên:** Nguyễn Văn Đăng
- **MSSV:** 2A202603371
- **SEED:** 1002
- **Ngày chạy:** 06/11/2026, trên CPU Windows (số đo độ trễ phụ thuộc máy)

## 1. Bằng chứng

| Tệp | Trạng thái |
|---|---|
| [day01_lab.ipynb](day01_lab.ipynb) | Đã chạy và lưu output; 15/15 kiểm tra đạt |
| [lab1_report.json](lab1_report.json) | Đã tạo; đủ 10 dự đoán |
| hand_calc.jpg | Chờ ảnh viết tay do học viên gửi |

Phần LLM chỉ qua API giả lập; chưa có key để chạy đánh giá thật.

## 2. Kết quả chính

| Phương án | F1 test (775 tin) | F1 SUB (40 tin) | p95 ms/tin | USD/1k tin |
|---|---:|---:|---:|---:|
| BoW + LogReg | 0,918 | 0,889 | 0,032 | 0 |
| BoW + MLP | 0,926 | 0,919 | 0,130 | 0 |
| Encoder + kNN | 0,913 | 1,000 | 19,137 | 0 |
| Encoder + LogReg | **0,980** | 0,974 | 11,772 | 0 |
| Encoder + MLP | 0,958 | 0,919 | 11,319 | 0 |

LLM zero-shot/few-shot: chưa đo vì thiếu API key. So sánh với LLM chỉ nên dùng F1 SUB, không lấy F1 test 775 tin của các mô hình cục bộ để so trực tiếp.

## 3. Ba dự đoán lệch thực tế

1. Dự đoán `lr=50` mất ổn định; thực tế loss tăng vọt đầu rồi về khoảng 0,005 sau 300 epoch. Dữ liệu này vẫn cho phép hội tụ ở learning rate rất lớn.
2. Dự đoán bỏ ReLU làm F1 giảm; thực tế F1 không ReLU 0,931 so với MLP có ReLU 0,926. Chênh nhỏ, chưa đủ chứng minh mạng tuyến tính tốt hơn tổng quát.
3. Dự đoán embedding xử lý sáu tin ngụy trang tốt hơn BoW; cả hai đều đúng 5/6 và cùng bỏ sót tin “Last chance! Your account rewards expire tonight...”. Biểu diễn tốt hơn vẫn cần bộ phân loại và dữ liệu phù hợp.

## 4. Phân tích 50 case khó

BoW+LogReg tụt nhiều nhất, từ F1 0,918 trên test thường xuống 0,333 trên bộ khó. Nhóm spam giọng tự nhiên là khó nhất: BoW đúng 10%, Encoder+LogReg đúng 40%. Case #12 mạo giọng người mới đến thành phố, #14 kể việc làm tại nhà; cả năm mô hình đều đoán sai. Điều này cho thấy điểm test thường lạc quan trước cách viết spam lạ. Chưa có kết quả LLM để phân tích prompt injection thực nghiệm.

## 5. Thử thách cá nhân — ngưỡng phân loại

| Ngưỡng | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0,2 | 0,881 | 0,918 | 0,899 |
| 0,5 | 0,977 | 0,866 | 0,918 |
| 0,8 | **1,000** | 0,701 | 0,824 |

Nếu ưu tiên không chặn nhầm OTP, chọn ngưỡng 0,8 trong ba giá trị này; đổi lại recall spam giảm. Kết quả precision 1,000 chỉ đúng trên tập test này, chưa đảm bảo ở sản xuất.

## 6. Phương án cho sản phẩm thật

Encoder+LogReg có F1 test cao nhất 0,980, p95 11,772 ms/tin dưới SLA 50 ms và throughput cả lô khoảng 200 tin/s trên máy thử. Mức trung bình 10 triệu/ngày khoảng 116 tin/s; cần kiểm thử thêm tải cao điểm và mở rộng ngang. Có thể dùng BoW+LogReg (p95 0,032 ms) để xử lý tin chắc chắn, chuyển tin khó sang Encoder+LogReg. Với giả định 100 input + 1 output token/tin, Luna tốn khoảng $3.150/tháng cho 10 triệu SMS/ngày; đây là ước tính theo giá đề bài, chưa phải số đo API.

## 7. AI log và điều đã học

AI đã viết mã và văn bản cho các phần 1–5, kể cả thử thách cá nhân và side lab. Các kiểm chứng đã thực hiện: chạy notebook trên CPU, 15/15 kiểm tra nội bộ đạt; side lab 19/19 test mock đạt. **Học viên chưa tự viết hoặc xác nhận có thể giải thích các hàm**, nên báo cáo không nhận đó là công việc độc lập. Phần LLM thật và ảnh viết tay đang chờ hoàn tất.

Tôi học được rằng learning rate lớn không nhất thiết phân kỳ trên mọi dữ liệu, và F1 trên 40 tin có độ bất định lớn. Stress test cũng cho thấy mô hình có điểm test cao vẫn có thể bỏ sót spam viết như lời trò chuyện.
