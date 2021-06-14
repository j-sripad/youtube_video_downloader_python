import sys
from PyQt5.QtWidgets import QProgressBar,QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,QRadioButton
from PyQt5.QtGui import *

from PyQt5.QtCore import *


from pytube import YouTube 

class SecondWindow(QWidget):
    def __init__(self,filesize = None):
        super().__init__()
        self.filesize = 0
        
    def init_ui(self,rbuttons=None,ids=None,yt_obj=None):
        self.setStyleSheet("background-color: #1e3d59;")
        print(rbuttons)
        self.yt_obj = yt_obj
        self.ids = ids
        self.main_wd =  MainWindow()
        self.setWindowTitle('second window')
        self.label = QLabel('Please select the quality of download ')
        self.label.setStyleSheet("color:white;font-weight:strong")
        self.label2 = QLabel("")
        self.button_2 = QPushButton('download', self)
        self.button_2.clicked.connect(self.onClick)
        self.button_2.setStyleSheet("background-color : green")

        self.cls_btn =  QPushButton('back', self)
        self.cls_btn.clicked.connect(self.mainLayout)
        self.cls_btn.setStyleSheet("background-color : #ecc19c")
        self.progressBar = QProgressBar(self)


        self.layout1 = QVBoxLayout()
    
        self.layout1.addWidget(self.label)
        
        self.rdbtn = []
        for rb in rbuttons:
            print(rb)
            self.rdbtn.append(QRadioButton(rb))
        for rbs in  self.rdbtn:  
            rbs.setStyleSheet("color : white")
            self.layout1.addWidget(rbs)
    
        self.layout1.addWidget(self.label2)
        self.layout1.addWidget(self.progressBar)
        self.layout1.addWidget(self.button_2)
        self.layout1.addWidget(self.cls_btn)
       
        self.setGeometry(200, 200, 800, 400)
        self.setLayout(self.layout1)
        self.setWindowTitle('Download window')
        self.show()
    def onClick(self):
        tag_id = None
        for i,rdbtn in enumerate(self.rdbtn):
            if rdbtn.isChecked():
                print(rdbtn.text())
                tag_id = self.ids[i]
                break

                    
        stream = self.yt_obj.streams.get_by_itag(int(tag_id))
        self.filesize = stream.filesize
        stream.download()
        print("download succesfull")
    def mainLayout(self):
        
        self.main_wd.show()

        self.close()
    def progress_Check(self, chunk = None, file_handler = None, bytes_remaining = None):
        #Gets the percentage of the file that has been downloaded.
        percent = (100*(self.filesize-bytes_remaining))/self.filesize
        self.progressBar.setValue(percent)
        QApplication.processEvents()


       
        
   


            

        

  
        

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui(['audio','video'])
    def init_ui(self,rbuttons):
        self.setStyleSheet("background-color: #1e3d59;")
        self.secondWindow = SecondWindow()
        self.label = QLabel('Please paste the youtube video URL ')
        self.label.setStyleSheet("color:white;font-weight:strong")
        self.label2 = QLabel("")
        self.url_link = QLineEdit(self)
        self.url_link.setStyleSheet("background-color : white")
        self.button_1 = QPushButton('Proceed to download', self)
        self.button_1.setStyleSheet("background-color : #ecc19c")
        self.button_1.setFixedHeight(40)

        self.label.setAlignment(Qt.AlignCenter)

        self.button_1.clicked.connect(self.onClick)
       
        self.warning = QLabel(' ')
        self.warning.setStyleSheet("color:red")

        self.layout = QVBoxLayout()
        
        self.layout.addStretch()
        self.layout.addWidget(self.label)
        self.layout.addWidget( self.url_link)
        
        self.rdbtn = []
        for rb in rbuttons:
            print(rb)
            self.rdbtn.append(QRadioButton(rb))
            
        for rbs in  self.rdbtn:  
            rbs.setStyleSheet("color : white")
            self.layout.addWidget(rbs)
    
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.button_1)
        self.layout.addWidget( self.warning)
        self.layout.addStretch()
        self.layout.setAlignment(Qt.AlignTop)
        self.setGeometry(200, 200, 800, 400)

        self.setLayout(self.layout)
        self.setWindowTitle('Youtube downloader')

    def onClick(self):
        check_flag = 0
        link=self.url_link.text()
        self.warning.setText('....')
        QApplication.processEvents()
       
        try: 
            # object creation using YouTube
            # which was imported in the beginning 
            yt = YouTube(link, on_progress_callback=self.secondWindow.progress_Check) 
            self.warning.setText('Please wait....')
            QApplication.processEvents()
            
        except: 
            print("Connection Error")
            if len(link) == 0:
                self.warning.setText('Please enter valid link')
                print(len(link))
            return #to handle exception 
        
        media_type = 'mp4'
        self.warning.setText('Please wait....')
        for rdbtn in self.rdbtn:
            if rdbtn.isChecked():
                check_flag = 1
                print(rdbtn.text())
                if 'audio' in rdbtn.text():
                    tags = [x.itag for x in yt.streams.filter(only_audio=True,)]
                    ids = [str(x.abr )for x in yt.streams.filter(only_audio=True)]
                else:
                    tags = [x.itag for x in yt.streams.filter(file_extension=media_type,progressive=True)]
                    ids = [str(x.resolution )for x in yt.streams.filter(file_extension=media_type,progressive=True)]
            
        if check_flag == 0:
            self.warning.setText('Please select audio or video....')
            return     
        else:
            self.warning.setText('Please wait....')
            QApplication.processEvents()



        
        if len(tags)<1:
            return
        else:

            self.secondWindow.init_ui(ids,tags,yt)
            self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())


