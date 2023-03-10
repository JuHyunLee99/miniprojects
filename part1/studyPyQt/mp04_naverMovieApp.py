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
        self.setWindowIcon(QIcon('./studyPyQt/movie.png'))

        # 시스널 / 슬롯함수 지정
        self.btnSearch.clicked.connect(self.btenSearchClicked)  # 검색버튼 클릭 시 검색 실행
        self.txtSearch.returnPressed.connect(self.txtSearchClicked) # txt검색 엔터를 치면 검색 실행
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)   # 결과 주소 더블클릭 시 웹브라우저 오픈 
    
    # 슬롯함수
    def tblResultDoubleClicked(self):   # 더블클릭 웹브라우저 오픈
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row,column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 5).text()   # 열 변경
        # print(url)
        webbrowser.open(url)
    
    def txtSearchClicked(self): # 엔터치면 검색
        self.btenSearchClicked()
    
    def btenSearchClicked(self):    # 검색버튼 누르면 검색
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
        self.tblResult.setColumnCount(7)    # 열 갯수 변경
        self.tblResult.setRowCount(len(items))  # 현재 행 100개 생성
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)   # 단일 선택
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)    # 컬럼수정금지
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '개봉링크', '감독', '배우진', '평점', '링크', '포스터'])  # 열제목
        self.tblResult.setColumnWidth(0, 150)   # 영화제목
        self.tblResult.setColumnWidth(1, 70)    # 개봉연도
        self.tblResult.setColumnWidth(4, 50)    # 평점
        
        for i, post in enumerate(items): # 0, 영화 ...
            title = self.replaceHtmlTag(post['title'])  # HTML 특수문자 변환 / 영화제목 가져오기 추가
            subtitle = post['subtitle']
            title = f'{title} ({subtitle})'
            pubDate = post['pubDate']
            director = self.replaceHtmlTag(post['director'])[:-1]   # [:-1] 파이썬에서만 가능
            actor = self.replaceHtmlTag(post['actor'])[:-1]
            userRating = post['userRating']
            link = post['link']
            img_url = post['image']

            # 포스터 이미지 추가
            if img_url != '':   # 빈값이면 포스터 없음
                data= urlopen(img_url).read()   # 2진데이터 - 네이버영화에 있는 이미지 다운, 텍스트 데이터
                image = QImage()    # 이미지 객체
                image.loadFromData(data)
                # QTableWidget은 이미지를 그냥 넣을 수 없음. QLabel() 집어넣은뒤 QLabel -> QTableWidget
                imgLabel = QLabel()
                imgLabel.setPixmap(QPixmap(image))

                # # data를 이미지로 저장 가능!
                # f = open(f'./studyPyQt/temp/image_{i+1}.png', mode='wb') # 파일쓰기
                # f.write(data)
                # f.close()

            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            if img_url != '':
                self.tblResult.setCellWidget(i, 6, imgLabel)
                self.tblResult.setRowHeight(i,110) # 포스터가 있으면 쉘 높이를 늘림.
            else:
                self.tblResult.setItem(i, 6, QTableWidgetItem('No Poster!'))
            
    # 문자열 특수문자 변환
    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt;', '<')  # less than 작다
        result = result.replace('&gt;', '>')   # more than 크다
        result = result.replace('<b>', '')   # bold
        result = result.replace('</b>', '')   # bold
        result = result.replace('&apos;', "'")   # apostopy 홑따음표
        result = result.replace('&quot;', '"')   # quotation mark 쌍 따옴표
        result = result.replace('|', ',')
        # 변환 안된 특수문자가 나타나면 여기 추가

        return result
        
            
# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())