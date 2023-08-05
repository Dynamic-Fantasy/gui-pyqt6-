from PyQt6.QtWidgets import QApplication , QWidget , QPushButton ,QHBoxLayout ,QLineEdit
from PyQt6.QtGui import QFont , QIcon 
import pyautogui as p
from pytube import YouTube

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        
        self.setGeometry(400,100,400,400)
        self.setFixedHeight(400)
        self.setFixedWidth(520)
        self.setStyleSheet("background-color:#101010")
        self.setWindowIcon(QIcon("qt_test/pngwing.com.png"))              

        

        self.hbx()




    def hbx(self):
        hbox = QHBoxLayout(self)

        self.entry = QLineEdit()
        self.entry.setPlaceholderText(" "+'Enter your link')
    

        self.entry.setFont(QFont("Calibri",19))
        #& Entry
        self.entry.setStyleSheet("""     

        QLineEdit{
                background-color :#171717 ;
                color :#f3f3f3;
                height : 50px;
                width : 100px;
                border-radius : 25px;
                border : none ;                
        }
        QLineEdit:hover{
                border: 1px solid #d128a6;
                                 
        }




        """)

        btn = QPushButton("Download")    #^button 
        btn.clicked.connect(self.click)
        btn.setFont(QFont("Calibri",16))
        btn.setStyleSheet("""
        
            QPushButton {
                background-color: #9603a3; 
                color: white;
                height : 50px;
                width : 100px;
                border: none;
                border-radius: 20px;  
            }
            QPushButton:hover {
                background-color: #871bec;
            }
            QPushButton:focus {
                background-color: #871bec;
            }
            """)
        
        hbox.addWidget(self.entry)

        hbox.addWidget(btn)

        self.setLayout(hbox)


    

    def download_video(self,url, output_path):
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            
            print(f"Downloading: {yt.title}")
            video.download(output_path)
            print("Download completed!")
        except Exception as e:
            print("Error:", e)

    def click(self):
        link =self.entry.text()
        path=r"<folder directory>"    #add your directory here        
        self.download_video(link,path)



app = QApplication([])
win =window()
win.show()

app.exec()
