# Qt Designer 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverApi import *
import webbrowser # 웹브라우저 모듈
from urllib.request import urlopen

class qtApp(QWidget):
    count = 0   # 클릭횟수 카운트 변수
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiMovie.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))

        # 검색 버튼 클릭시스널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btenSearchClicked)
        # 검색어 입력후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchClicked)
        # 결과 주소 더블클릭하면 웹브라우저 오픈
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)
    
    # 더블클릭 웹브라우저 오픈
    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row,column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 5).text()   # 열 변경
        # print(url)
        webbrowser.open(url)
    
    # 엔터치면 검색
    def txtSearchClicked(self):
        self.btenSearchClicked()
    
    # 검색버튼 누르면 검색
    def btenSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self,'영화명', '검색어를 입력하세요!')
            return
        else:
            api = NaverApi()    # NaverApi 클래스 객체 생성
            node = 'movie'   # movie로 변경하면 영화검색
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
        self.tblResult.setColumnCount(7)    # 열 갯수 변경
        self.tblResult.setRowCount(len(items))  # 현재 행 100개 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '개봉링크', '감독', '배우진', '평점', '링크', '포스터'])
        self.tblResult.setColumnWidth(0, 150)   # 영화제목
        self.tblResult.setColumnWidth(1, 60)    # 개봉연도
        self.tblResult.setColumnWidth(4, 50)    # 평점
        # 컬럼 데이터 수정 금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 영화 ...
            title = self.replaceHtmlTag(post['title'])  # HTML 특수문자 변환
            pubDate = post['pubDate']
            director = post['director']
            actor = post['actor']
            userRating = post['userRating']
            link = post['link']
            # image = QImage(requests.get(post['image'], stream = True))
            # imageUrl = urlopen(post['image']).read()
            # image = QPixmap()
            # image.loadFromData(imageUrl)
            # imgLabel = QLabel()
            # imgLabel.setPixmap(image)
            # imgLabel.setGeometry(0, 0, 60,100)
            # imgLabel(60,100)

            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            self.tblResult.selCellWidget(i, 6, imgLabel)
            
    
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