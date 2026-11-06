# Các bước tính để tự viết lên giấy

Tệp này do AI tạo để đối chiếu phép tính. Ảnh `hand_calc.jpg` hiện là ảnh chụp bản AI gõ trong Notepad, không phải ảnh viết tay. Muốn đáp ứng rubric, học viên cần tự viết và chụp ảnh thay thế.

1. **Baseline accuracy:** Sau bỏ trùng có 4.516 ham trên 5.169 tin. Luôn đoán ham thì accuracy = 4.516 / 5.169 = 0,8737 → **0,87**.
2. **Sigmoid tại 0:** σ(0) = 1 / (1 + e⁰) = 1 / 2 = **0,50**.
3. **F1 ví dụ:** TP = 80, FP = 20, FN = 40. Precision = 80 / (80 + 20) = 0,80; recall = 80 / (80 + 40) = 0,6667. F1 = 2TP / (2TP + FP + FN) = 160 / 220 = 0,7273 → **0,73**.
4. **Cosine:** a = [1, 2, 0], b = [2, 1, 2]. Tích vô hướng = 1×2 + 2×1 + 0×2 = 4. ‖a‖ = √(1² + 2²) = √5; ‖b‖ = √(2² + 1² + 2²) = 3. Cosine = 4 / (3√5) = 0,5963 → **0,60**.
5. **Chi phí LLM/ngày theo đề:** 1.000.000 SMS × 100 token input = 100.000.000 token input, phí = 100 × $0,10 = $10,00. Output = 1.000.000 × 1 = 1.000.000 token, phí = 1 × $0,50 = $0,50. Tổng = **$10,50/ngày**.
