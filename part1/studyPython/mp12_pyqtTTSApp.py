import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *  # Qt.wite...
import time
from gtts import gTTS
from playsound import playsound

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/ttsApp.ui', self)
        self.setWindowTitle('텍스트 투 스피치 v0.3')

        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked)

    def btnQrGenClicked(self):
        text = self.txtQrGen.text()

        if text == '':
            QMessageBox.warning(self,'경고', '텍스트를 입력하세요')
            return
        
        tts = gTTS(text=text, lang='ko', slow=False)
        tts.save('./studyPython/output/hi.mp3')
        # time.sleep(1.0)
        # playsound('./studyPython/output/hi.mp3')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())