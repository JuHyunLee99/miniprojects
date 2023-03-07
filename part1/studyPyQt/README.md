# PyQt5
## QtWidgets
기본적인 UI 구성요소 제공하는 윗젯(클래스)들을 포함하는 모듈

### QApplication
```python
#  어플리케이션 객체 생성
app = QApplication(sys.argv)    
```

### QWidget
self.setWindowTitle('Simple Window')    : 타이틀바에 나타나는 창의 제목 설정
move(1920 // 2 - 200, 1080 // 2 -100)   : 위젯을 스크린의 x=0px, y=0py로 이동 시킴. 정중앙 위치잡기
resize(400, 200)   : 위젯 크기 너비 400px, 높이 200px로 조절
show() : 핵심!! 위젯을 스크린에 보여줌
setWindowIcon(QIcon('./Day09/iot.png')) : 어플레케이션 아이콘 설정

## QtGui
QIcon('./Day09/iot.png')    : QIcon 객체 생성