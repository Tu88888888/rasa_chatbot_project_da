Cách sử dụng Project:.

B1.Download thư mục pythonProject,và file db analogcmos(1) về máy.

B2: Vào mục pythonProject, tại terminal nhập lệnh: cd pythonProject.

B3: Cài đặt tất quả các thư viện cần thiết tại file requirement.txt.

B4: Vào file endpoint tại project, đổi username và passoword mysql, sau đó mở terminal, chạy câu lệnh: Rasa run actions để kết nối database.

B5: Mở 3 terminal khác nhau, nhập 3 lệnh sau:.
1. Tại terminal 1: rasa run -m models --enable-api --cors "*" --debug. 
2. Tại terminal 2: rasa run actions.
3. Tại terminal 3: python run main.py. 

Tại terminal thứ 3, sau khi xuất hiện URL local, kick chuột, sẽ push project lên website local. 
