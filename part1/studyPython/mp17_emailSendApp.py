import smtplib  # 메일전송프로토콜
from email.mime.text import MIMEText
# MIME은 ASCII가 아닌 문자 인코딩을 이용해 영어가 아닌 다른 언어로된 전자 우편을 보낼 수 있는 방식

send_email = 'dlwngus0829@naver.com'
send_pass = '' # 임시 비밀번호

recv_email = 'juhyun.lee0829@kakao.com'

smtp_name = 'smtp.naver.com'
smtp_port = 587 # 포트번호

text = ''' 메일 내용입니다. 긴급입니다.
조심하게요~ 빨리 연락주세요!!
'''

msg = MIMEText(text)
msg['Subject'] = '메일 제목입니다'
msg['From'] = send_email # 보내는 메일
msg['To'] = recv_email # 받는 메일
# print(msg.as_string())

mail = smtplib.SMTP(smtp_name, smtp_port)   # SMTP 객체생성
mail.starttls() # 전송계층보안 시작
mail.login(send_email, send_pass)
mail.sendmail(send_email, recv_email, msg=msg.as_string())
mail.quit()
print('전송완료!')
