import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *  # Qt.wite...
import pymysql
import qrcode


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/qrcodeApp.ui', self)
        self.setWindowTitle('Qrcode 생성앱 v0.1')
        self.setWindowIcon(QIcon('./studyPython/qr-code.png'))

        # 시그널/슬롯
        self.btnQrGen.clicked.connect(self.btnQrGenClicked) # Generate 버튼
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked)  # 입력 후 엔터
    
    def btnQrGenClicked(self):  # Generate 버튼
        data = self.txtQrData.text()

        if data == '':
            QMessageBox.warning(self,'경고','데이터를 입력하세요.')
            return
        else:
            qr_img = qrcode.make(data)
            qr_img.save('./studyPython/site.png')

            img = QPixmap('./studyPython/site.png')
            self.lblQrCode.setPixmap(img.scaledToWidth(300))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())