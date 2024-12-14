Cách sử dụng Project:
B1: Vào mục pythonProject
B2: Cài đặt tất quả các thư viện cần thiết tại file requirement.txt
B3: Mở 3 terminal khác nhau, nhập 3 lệnh sau:
1. rasa run -m models --enable-api --cors "*" --debug
2. rasa run actions
3. python run main.py

Tại terminal thứ 3, sau khi xuất hiện URL local, kick chuột, sẽ push project lên website local. 
