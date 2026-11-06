# Ngày 1 — Bài Tập & Phản Ánh (side lab TUỲ CHỌN)

> Side lab này **không** thuộc điểm chính của Day 01 (xem [RUBRIC.md](../RUBRIC.md) mục Bonus). Model: `gpt-6.1-terra` (lớn) và `gpt-6-luna` (nhỏ). `gpt-4o` / `gpt-4o-mini` bị gỡ khỏi API ngày 14/01/2027 ([nguồn](https://developers.openai.com/api/docs/deprecations)). Tên khoá `gpt4o_*` / `mini_*` trong kết quả là hợp đồng của test, giữ nguyên để tương thích: đọc là "model lớn" / "model nhỏ".
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Copy `src/optional_llm_api/template.py` thành `src/optional_llm_api/solution/solution.py`, triển khai mọi TODO, rồi chạy từ gốc repo: `pytest tests/test_solution.py -v`. Chưa có `solution/solution.py` thì test tự bỏ qua.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python src/optional_llm_api/solution/solution.py
```
Bạn sẽ thấy output so sánh phản hồi của `gpt-6.1-terra` và `gpt-6-luna`.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."** (nhớ gửi `reasoning_effort="none"`: model GPT-6 chỉ nhận `temperature` khi tắt suy luận)

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
Chưa có API key trong phiên chạy, nên chưa có bốn phản hồi để đối chiếu thực nghiệm. Dự đoán: `temperature=0` sẽ ổn định hơn; khi tăng lên 0.5, 1.0 và 1.5, cách diễn đạt và ví dụ có thể đa dạng hơn, nhưng mức thay đổi không nhất thiết tăng đều trong chỉ bốn lần gọi. Cần chạy đủ bốn giá trị và ghi câu trả lời thực tế trước khi kết luận.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
Với chatbot hỗ trợ khách hàng, tôi sẽ bắt đầu ở `temperature=0` để câu trả lời nhất quán với chính sách, rồi đánh giá độ chính xác và mức lặp trước khi điều chỉnh.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem `gpt-6.1-terra` đắt hơn `gpt-6-luna` bao nhiêu lần cho workload này** (giá 11/2026: terra $1.00 / $5.00, luna $0.10 / $0.50 mỗi 1M token input / output):
Có 10.000 × 3 = 30.000 lượt gọi/ngày, tổng khoảng 10,5 triệu token/ngày. Giá input và output của Terra đều gấp **10 lần** Luna, nên với cùng tỷ lệ token, tổng chi phí cũng gấp 10. Ví dụ nếu mỗi lượt có 250 input + 100 output token: Terra khoảng $22,50/ngày, Luna khoảng $2,25/ngày. Đề không cho tỷ lệ input/output nên không thể suy ra một số USD duy nhất.

**Mô tả một trường hợp mà chi phí cao hơn của `gpt-6.1-terra` là xứng đáng, và một trường hợp `gpt-6-luna` là lựa chọn tốt hơn:**
Terra có thể đáng tiền khi cần xử lý yêu cầu phức tạp, nhiều bước và chi phí trả lời sai cao, sau khi đã đo chất lượng trên tập đánh giá riêng. Luna phù hợp hơn cho hỏi đáp ngắn, phân loại đơn giản hoặc các tác vụ số lượng lớn có thể kiểm tra đầu ra tự động.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
Streaming hữu ích khi phản hồi dài hoặc thời gian tạo nội dung cao: người dùng thấy câu đầu sớm và có thể đọc trong khi phần sau đang sinh. Non-streaming phù hợp cho nhãn phân loại hoặc kết quả ngắn cần kiểm tra toàn bộ trước khi hiển thị; nó cũng đơn giản hơn khi cần xử lý JSON như một đơn vị.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/test_solution.py -v` (19/19, mock API)
- [x] `call_openai` đã triển khai và kiểm thử bằng mock
- [x] `call_openai_mini` đã triển khai và kiểm thử bằng mock
- [x] `compare_models` đã triển khai và kiểm thử bằng mock
- [x] `streaming_chatbot` đã triển khai và kiểm thử bằng mock
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [ ] Thí nghiệm temperature bằng API thật và ghi phản hồi thực tế
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định
