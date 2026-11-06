# Báo cáo cá nhân — Day 01

- **Họ tên:** Nguyễn Văn Đăng
- **MSSV:** 2A202603371
- **SEED:** 1002
- **Ngày chạy:** 06/11/2026, CPU Windows; thời gian có thể đổi trên Colab và khi API tải khác nhau.

## 1. Bằng chứng

| Tệp | Trạng thái |
|---|---|
| [day01_lab.ipynb](day01_lab.ipynb) | Đã chạy và lưu output; 15/15 kiểm tra đạt |
| [lab1_report.json](lab1_report.json) | Đã tạo; đủ 10 dự đoán và 8 phương án |
| [hand_calc_notepad.txt](hand_calc_notepad.txt) | AI chuẩn bị nội dung và bản gốc; học viên sửa tiêu đề, bỏ chú thích |
| [hand_calc.jpg](hand_calc.jpg) | Học viên chụp lại Notepad, AI cắt ảnh để đúng tên tệp; **không phải chữ viết tay** |
| [hand_calc_steps.md](hand_calc_steps.md) | Các bước tính do AI chuẩn bị |

Ảnh `hand_calc.jpg` đáp ứng yêu cầu có tệp ảnh và thể hiện các bước tính, nhưng **không đáp ứng tiêu chí ảnh viết tay** trong rubric. Không sử dụng ảnh này để nhận là học viên đã tính tay.

## 2. Kết quả chính

| Phương án | F1 test | F1 SUB 40 | p95 ms/tin | USD/1k tin |
|---|---:|---:|---:|---:|
| BoW + LogReg | 0,918 | 0,889 | 0,048 | 0 |
| BoW + MLP | 0,926 | 0,919 | 0,238 | 0 |
| Encoder + kNN | 0,913 | 1,000 | 27,696 | 0 |
| Encoder + LogReg | **0,980** | 0,974 | 19,722 | 0 |
| Encoder + MLP | 0,958 | 0,919 | 18,359 | 0 |
| DeepSeek Flash zero-shot | — | 0,976 | 1.450,166 | 0,01053 |
| DeepSeek Pro zero-shot | — | 0,857 | 7.416,640 | 0,04545 |
| DeepSeek Flash few-shot | — | 1,000 | 1.111,546 | 0,02673 |

LLM chỉ được đo trên SUB 40; không so trực tiếp với F1 test 775 tin của các mô hình cục bộ. Chi phí là ước tính theo số từ/0,75 token, giá DeepSeek off-peak và input cache miss, không phải hóa đơn thực tế.

## 3. Ba dự đoán lệch thực tế

1. Dự đoán model lớn tốt hơn model nhỏ; thực tế DeepSeek Pro zero-shot F1 SUB 0,857, Flash 0,976. SUB chỉ 40 tin nên cần lặp đánh giá trước khi kết luận tổng quát.
2. Dự đoán `lr=50` mất ổn định; thực tế loss tăng vọt đầu rồi về khoảng 0,005 sau 300 epoch. Dữ liệu này vẫn hội tụ ở learning rate lớn.
3. Dự đoán bỏ ReLU làm F1 giảm; thực tế F1 không ReLU 0,931 so với MLP có ReLU 0,926. Chênh nhỏ và không chứng minh mô hình tuyến tính luôn tốt hơn.

## 4. Phân tích 50 case khó

BoW+LogReg tụt nhiều nhất: F1 test thường 0,918 xuống 0,333 trên bộ khó. Flash zero-shot và Flash với prompt phòng thủ đều đạt F1 0,964, đúng 6/6 case prompt injection và 80% spam giọng tự nhiên. Hai prompt cùng sai #13 (nhắc ảnh sự kiện nhưng dẫn sang bán hàng) và #16 (giả làm bạn cũ bán mỹ phẩm). Case #16 bị tất cả mô hình bỏ sót. Kết quả 50 tin viết tay giúp tìm lỗ hổng, không đại diện cho tần suất lỗi ngoài đời.

## 5. Thử thách cá nhân — ngưỡng phân loại

| Ngưỡng | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0,2 | 0,881 | 0,918 | 0,899 |
| 0,5 | 0,977 | 0,866 | 0,918 |
| 0,8 | **1,000** | 0,701 | 0,824 |

Nếu ưu tiên không chặn nhầm OTP, chọn 0,8 trong ba giá trị; đổi lại recall spam giảm. Precision 1,000 chỉ đúng trên tập test này.

## 6. Phương án cho sản phẩm thật

Encoder+LogReg có F1 test cao nhất 0,980, p95 19,722 ms/tin dưới SLA 50 ms và throughput cả lô 148 tin/s trên máy thử. Mức trung bình 10 triệu/ngày khoảng 116 tin/s; cần thử tải cao điểm và mở rộng ngang. Dùng BoW+LogReg cho tin chắc chắn và Encoder+LogReg cho tin lưỡng lự là một router khả thi. DeepSeek Flash zero-shot p95 1,45 giây nên không đạt SLA; với chi phí ước tính $0,01053/1.000 tin, 10 triệu/ngày trong 30 ngày tương đương khoảng **$3.159/tháng** nếu cùng mức giá off-peak/cache miss và độ dài prompt.

## 7. AI log và điều đã học

| Phần | Con người thực hiện | AI thực hiện | Cách kiểm chứng |
|---|---|---|---|
| Thông tin và quyền truy cập | Học viên cung cấp họ tên, MSSV, link repository, khóa DeepSeek có hạn mức; yêu cầu cách trình bày bài và log | Đưa thông tin vào bản làm, cấu hình provider và giữ khóa ngoài repository | Đối chiếu thông tin được học viên gửi; quét repository không thấy khóa |
| Phần 0–3: ML, DL, embedding | Chưa có bằng chứng học viên tự viết mã hoặc tự giải thích | Viết các hàm TODO, điền dự đoán và lời giải thích, chạy notebook | Các ô kiểm tra đạt; kết quả và output có trong notebook |
| Phần 4: LLM | Học viên cung cấp khóa API và hạn mức | Viết hàm API/prompt, chạy DeepSeek và phân tích kết quả | Có output gọi API thật, số đo trong JSON; khóa không lưu trong tệp |
| Phần 5: so sánh, stress test, thử thách | Chưa có bằng chứng học viên tự làm các mục này | Viết mã thử thách, phân tích 50 case, soạn báo cáo | Đối chiếu bảng và output trong notebook |
| Năm phép tính và ảnh | Học viên yêu cầu dùng Notepad, sửa tiêu đề/chú thích và tự chụp ảnh mới | Tính và gõ bản đầu trong Notepad; cắt ảnh mới thành `hand_calc.jpg` | Ảnh thể hiện chữ gõ Notepad, không nhận là viết tay |
| Side lab | Chưa có bằng chứng học viên tự lập trình | Viết `solution.py` và làm thí nghiệm temperature | 19/19 test mock đạt; phản hồi thô trong docs |

**AI là tác giả của mã, dự đoán, các phép tính và nội dung phân tích trong lần nộp này.** Việc chạy test xác nhận mã hoạt động trong phạm vi kiểm tra; không chứng minh học viên đã tự viết hoặc hiểu bài.

Learning rate lớn không nhất thiết phân kỳ. Model lớn cũng không nhất thiết tốt hơn trên một tập nhỏ: lần thử này Pro có F1 SUB thấp hơn Flash. Stress test cho thấy F1 test thường cao vẫn có thể che giấu các dạng spam viết tự nhiên.
