from predict import Ui_GAN
from PyQt5.QtWidgets import QApplication,QWidget
import  sys
from PyQt5 import QtCore
import sys

class GAN_show(QWidget,Ui_GAN):  #继承类
    def __init__(self):
        super().__init__()
        self.setupUi(self)   #执行类中的setupUi函数
        self.setWindowOpacity(0.95)
        self.setStyleSheet("background-color:rgb(43,43,43)")
        self.create.setStyleSheet('''
                     QPushButton
                     {text-align : center;
                     background-color : rgb(60,63,65);
                     font: bold;
                     border: solid;
                     border-color: rgb(255,255,255);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 25px;
                     color:white;
                     }
                     QPushButton:hover
                     {text-align : center;
                     background-color : rgb(255,255,255);
                     font: bold;
                     border: solid;
                     border-color: rgb(60,63,65);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 30px;
                     color:rgb(50,50,50);}
                     ''')
        self.picture_address.setStyleSheet('''
                     QPushButton
                     {text-align : center;
                     background-color : rgb(60,63,65);
                     font: bold;
                     border: solid;
                     border-color: rgb(255,255,255);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 25px;
                     color:white;
                     }
                     QPushButton:hover
                     {text-align : center;
                     background-color : rgb(255,255,255);
                     font: bold;
                     border: solid;
                     border-color: rgb(60,63,65);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 30px;
                     color:rgb(50,50,50);}
                     ''')
        self.mask_address.setStyleSheet('''
                     QPushButton
                     {text-align : center;
                     background-color : rgb(60,63,65);
                     font: bold;
                     border: solid;
                     border-color: rgb(255,255,255);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 25px;
                     color:white;
                     }
                     QPushButton:hover
                     {text-align : center;
                     background-color : rgb(255,255,255);
                     font: bold;
                     border: solid;
                     border-color: rgb(60,63,65);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 30px;
                     color:rgb(50,50,50);}
                     ''')
        self.save_address.setStyleSheet('''
                     QPushButton
                     {text-align : center;
                     background-color : rgb(60,63,65);
                     font: bold;
                     border: solid;
                     border-color: rgb(255,255,255);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 25px;
                     color:white;
                     }
                     QPushButton:hover
                     {text-align : center;
                     background-color : rgb(255,255,255);
                     font: bold;
                     border: solid;
                     border-color: rgb(60,63,65);
                     border-width: 5px;
                     border-radius: 10px;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 30px;
                     color:rgb(50,50,50);}
                     ''')
        self.output.setStyleSheet('''
        QLabel{
                backgound-color:rgb(200,200,200);
                border: solid;
                border-color: rgb(255,255,255);
                border-width: 2px;
                border-radius: 5px;
                }
        ''')
        self.picture_text.setStyleSheet('''
                     QPushButton
                     {text-align : center;
                     background-color : rgb(60,63,65);
                     font: bold;
                     border: None;
                     padding: 6px;
                     height : 14px;
                     border-style: outset;
                     font : 15px;
                     color:white;
                     }
                     ''')
        self.mask_text.setStyleSheet('''
                             QPushButton
                             {text-align : center;
                             background-color : rgb(60,63,65);
                             font: bold;
                             border: None;
                             padding: 6px;
                             height : 14px;
                             border-style: outset;
                             font : 15px;
                             color:white;
                             }
                             ''')
        self.save_text.setStyleSheet('''
                             QPushButton
                             {text-align : center;
                             background-color : rgb(60,63,65);
                             font: bold;
                             border: None;
                             padding: 6px;
                             height : 14px;
                             border-style: outset;
                             font : 15px;
                             color:white;
                             }
                             ''')


        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.picture_address.clicked.connect(self.get_picture)
        self.mask_address.clicked.connect(self.get_mask)
        self.save_address.clicked.connect(self.get_save)

        self.create.clicked.connect(self.get_output)

    def get_detail_picture(self):
        return self.picture_address

    def get_detail_mask(self):
        return self.mask_address

    def get_detail_save(self):
        return self.save_address



if __name__=='__main__':
    app=QApplication(sys.argv)
    w=GAN_show()
    w.show()
    sys.exit(app.exec_())
