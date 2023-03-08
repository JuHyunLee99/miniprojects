# Qt Designer 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverApi import *
import webbrowser # 웹브라우저 모듈


class qtApp(QWidget):
    count = 0   # 클릭횟수 카운트 변수
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiSearch.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))

        # 검색 버튼 클릭시스널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btenSearchClicked)
        # 검색어 입력후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchClicked)
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)
    
    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row,column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 1).text()
        # print(url)
        webbrowser.open(url)
    
    def txtSearchClicked(self):
        self.btenSearchClicked()
    
    def btenSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self,'경고', '검색어를 입력하세요!')
            return
        else:
            api = NaverApi()    # NaverApi 클래스 객체 생성
            node = 'news'   # movie로 변경하면 영화검색
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            
            # 테이블위젯에 출력 기능
            itmes = result['items'] # json결과 중 items 아래 배열만 추출
            # print(itmes)  
            self.makeTable(itmes)   # 테이블위젯에 데이트들을 할당함수

    # 테이블 위젯에 데이터 표시
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)   # 단일 선택
        self.tblResult.setColumnCount(3)
        self.tblResult.setRowCount(len(items))  # 현재 행 100개 생성
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0, 310)
        self.tblResult.setColumnWidth(1, 260)
        # 컬럼 데이터 수정 금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 뉴스 ...
            title = self.replaceHtmlTag(post['title'])  # HTML 특수문자 변환
            originallink = post['originallink']
            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(originallink))
    
    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt;', '<')  # less than 작다
        result = result.replace('&gt;', '>')   # more than 크다
        result = result.replace('<b>', '')   # bold
        result = result.replace('</b>', '')   # bold
        result = result.replace('&apos;', "'")   # apostopy 홑따음표
        result = result.replace('&quot;', '"')   # quotation mark 쌍 따옴표
        # 변환 안된 특수문자가 나타나면 여기 추가

        return result
        



            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())