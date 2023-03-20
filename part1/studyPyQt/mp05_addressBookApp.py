# 주소록 GUI 프로그램 - MySQL 연동
# Qt Designer 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql  # MySQL DB 모듈

class qtApp(QMainWindow):
    conn = None
    curIdx = 0  # 현재 데이터 PK

    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/addressBook.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/address-book.png'))

        self.initDB()   # DB 불러오기

        # 버튼 시그널/슬롯함수 지정
        self.btnNew.clicked.connect(self.btnNewClicked) # 신규
        self.btnSave.clicked.connect(self.btnSaveClicked)   # 저장
        self.tblAddress.doubleClicked.connect(self.tblAddressDoubleClicked) # 테이블 더블 클릭
        self.btnDel.clicked.connect(self.btnDelClicked) # 삭제
  

    # 신규, 저장 버튼 슬롯함수
    def btnNewClicked(self):    # 신규

        # 라인에디트 내용 삭제 후 이름에 포커스
        self.txtName.setText('')
        self.txtPhone.setText('')
        self.txtEmail.setText('')
        self.txtAddress.setText('')
        self.txtName.setFocus()
        self.curIdx = 0 # 0은 진짜 신규!
        # print(self.curIdx)

    def btnSaveClicked(self):   # 저장
        fullName = self.txtName.text()
        phoneNum = self.txtPhone.text()
        email = self.txtEmail.text()
        address = self.txtAddress.text()

        # print(fullName, phoneNum, email, address)

        # 이름과 전화번호를 입력하지 않으면 알람 메세지박스
        if fullName == '' or phoneNum == '':
            QMessageBox.warning(self, '주의', '이름과 전화번호를 입력하세요!')
            return # 진행 불가

        elif fullName == '':
            QMessageBox.warning(self, '주의', '이름을 입력하세요!')
            return # 진행 불가

        elif phoneNum == '':
            QMessageBox.warning(self, '주의', '핸드폰 번호를 입력하세요!')
            return # 진행 불가
        
        else:    # INSERT 쿼리문 UPDATE 쿼리문 -> DB에 새 데이터 저장
            # MySQL 서버 Connect
            self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db = 'miniproject', charset='utf8')
            cur = self.conn.cursor()    # Connection으로부터 Cursor 생성

            if self.curIdx == 0: # 신규
                # INSERT 쿼리문
                query = '''INSERT INTO addressbook (FullName, PhoneNum, Email, Address)
                            VALUES (%s, %s, %s, %s)'''
                cur.execute(query, (fullName, phoneNum, email, address))
                # 저장성공 메세지박스
                QMessageBox.about(self, '성공', '저장 성공했습니다.')
            else:   # 수정 
                # UPDATE 쿼리문
                query = '''UPDATE addressbook
                              SET FullName = %s
                                , PhoneNum = %s
                                , Email = %s
                                , Address = %s
                            WHERE Idx = %s'''  
                cur.execute(query, (fullName, phoneNum, email, address, self.curIdx))
                # 수정 성공 메세지박스
                QMessageBox.about(self, '성공', '변경했습니다.')

            self.conn.commit()
            self.conn.close()


            # QTableWidget 새 데이터 출력 : 새로 DB 불러오기
            self.initDB()
            # 입력창 내용 초기화
            self.btnNewClicked()

    def tblAddressDoubleClicked(self):  # 더블클릭
        rowIndex = self.tblAddress.currentRow() 
        self.txtName.setText(self.tblAddress.item(rowIndex, 1).text())
        self.txtPhone.setText(self.tblAddress.item(rowIndex, 2).text())
        self.txtEmail.setText(self.tblAddress.item(rowIndex, 3).text())
        self.txtAddress.setText(self.tblAddress.item(rowIndex, 4).text())
        self.curIdx = int(self.tblAddress.item(rowIndex, 0).text()) # 해당 Key값 저장
        # print(self.curIdx)
    
    def btnDelClicked(self):    # 삭제
        if self.curIdx == 0:
            QMessageBox.warning(self, '경고', '삭제할 데이터를 선택하세요.')
            return # 함수를 빠져나감
        else:
            reply = QMessageBox.question(self, '확인', '정말로 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return # 함수 빠져나감
            
            self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db = 'miniproject', charset='utf8')
            query = 'Delete From addressbook WHERE Idx = %s'
            cur = self.conn.cursor()
            cur.execute(query, (self.curIdx))

            self.conn.commit()
            self.conn.close()

            QMessageBox.about(self, '성공', '데이터를 삭제했습니다.')

            self.initDB()   # DB 다시 불러오기
            self.btnNewClicked()    # txt 내용 삭제

    # DB 불러오기
    def initDB(self):  # SELECT 쿼리문
        # MySQL 서버 Connect
        self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db = 'miniproject', charset='utf8') 
        
        # Connection으로부터 Cursor 생성
        cur = self.conn.cursor()

        # SQL SELECT 쿼리문 실행
        query = '''SELECT Idx
	                    , FullName
                        , PhoneNum
                        , Email
                        , Address
                     FROM addressbook'''    # ''' ''' 멀티라인 문자열 편함!
        cur.execute(query)

        # 데이터 Fetch
        rows = cur.fetchall()   
        # print(rows)   # 전체 rows (Tuple 형태로 출력)
        # print(rows[0]) # 첫번째 row: (1, '이주현', 010-9466-2399, juhyun.lee0829@daum.net, 경남 양산시)
        # print(rows[1]) # 두번째 row: (2, '성명건', 010-6683-777, personar95@naver.com, 부산광역시 동래구)

        # 테이블 위젯에 데이터 삽입
        self.makeTable(rows)

        # Connection 닫기
        self.conn.close()
       
    def makeTable(self, rows):  # 테이블 위젯에 DB 데이터 삽입
        self.tblAddress.setColumnCount(5)   # 0. 컬럼갯수
        self.tblAddress.setRowCount(len(rows))  # 0. 행갯수
        self.tblAddress.setSelectionMode(QAbstractItemView.SingleSelection)   # 1. 단일 선택
        self.tblAddress.setEditTriggers(QAbstractItemView.NoEditTriggers)    # 1. 컬럼수정금지
        self.tblAddress.setHorizontalHeaderLabels(['번호','이름','핸드폰','이메일','주소']) # 1. 열 제목
        self.tblAddress.setColumnWidth(0, 0)    # 1. 번호는 숨김
        self.tblAddress.setColumnWidth(1, 70)    # 이름 열 7 
        self.tblAddress.setColumnWidth(2, 105)    # 핸드폰 열 105
        self.tblAddress.setColumnWidth(3, 175)    # 이메일 열
        self.tblAddress.setColumnWidth(4, 200)    # 주소열


        for i, row in enumerate(rows):
            # row[0] ~ row[4]
            # # rows의 첫번째 row에서 row[0]: 1 row[1] 이주현 row[2] 010-9466-2399 ... 
            idx = row[0]
            fullName = row[1]
            phoneNum = row[2]
            email = row[3]
            address = row[4]

            self.tblAddress.setItem(i, 0, QTableWidgetItem(str(idx)))
            self.tblAddress.setItem(i, 1, QTableWidgetItem(fullName))
            self.tblAddress.setItem(i, 2, QTableWidgetItem(phoneNum))
            self.tblAddress.setItem(i, 3, QTableWidgetItem(email))
            self.tblAddress.setItem(i, 4, QTableWidgetItem(address))

        # 상태바
        self.stbCurrent.showMessage(f'전체 주소록 : {len(rows)}개')
    

# mian
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())   # app.exec_(): 계속 반복 실행함.