from PyQt5.QtWidgets import QApplication , QWidget , QPushButton , QGridLayout , QLineEdit , QMessageBox , QVBoxLayout
from PyQt5.QtGui import QFont , QIcon
from PyQt5.QtCore import Qt
from functools import partial

class Calc_UI (QWidget) :

    font_button = QFont("Acknowledgement",14)
    font_inputbox = QFont("Bahrain",12,weight=87) 

    def __init__(this,*args,**kwargs) :
        
        this.app = QApplication([])

        this.screen_dim = this.app.primaryScreen().size()

        this.icon = QIcon("maths.png")
        
        super().__init__(*args,**kwargs)

        this.setWindowTitle("Calculator")
        this.setWindowIcon(this.icon)
        this.setStyleSheet(open("CSS/QWidget.css").read())
        this.setMaximumSize(this.screen_dim.width()//4 , this.screen_dim.height()//2 )

        down_layout = QVBoxLayout()
        
        this.inputbox = QLineEdit()
        this.inputbox.setFont(this.font_inputbox)
        this.inputbox.setMinimumSize(350,50)
        this.inputbox.setMaximumSize(this.screen_dim.width() ,50)
        this.inputbox.setStyleSheet(open("CSS/QLineEdit.css").read())
        this.inputbox.setAlignment(Qt.AlignCenter)
        this.inputbox.setPlaceholderText("Enter your Expression here ...")
        this.inputbox.returnPressed.connect(this.__evaluate)

        down_layout.addWidget(this.inputbox)
        this.button_layout = QGridLayout()
        this.__buttons_setup()
        down_layout.addLayout(this.button_layout)

        this.setLayout(down_layout)
        this.show()
        exit(this.app.exec())

    def __buttons_setup(this) :
        
        btn_list = [['(' , ')' , '=' , '<--'] , ['1' , '2' , '3' , 'C'] , ['4' , '5' , '6' , '+'] , ['7' , '8' , '9' , '-'] , ['0' , '^' , '÷' , 'x']]
        btn_objects = [[QPushButton() for j in range(btn_list[0].__len__())] for i in range(btn_list.__len__())]

        for i in range(btn_list.__len__()) :
            for j in range(btn_list[i].__len__()) :
                               
                btn_objects[i][j].setText(btn_list[i][j])
                btn_objects[i][j].setFont(this.font_button)
                btn_objects[i][j].setStyleSheet(open("CSS/QPushButton.css").read())
                btn_objects[i][j].setMinimumSize(this.size().width()//8 , this.size().height()//6)
                btn_objects[i][j].setMaximumSize(this.size().width()//4 , this.size().height()//6 )
                
                if btn_list[i][j] == 'C' : btn_objects[i][j].pressed.connect(lambda : this.inputbox.clear() )
                elif btn_list[i][j] == '<--' : btn_objects[i][j].pressed.connect(lambda : this.inputbox.setText( this.inputbox.text()[:-1] ) )
                elif btn_list[i][j] == '=' : btn_objects[i][j].pressed.connect(this.__evaluate)
                else : btn_objects[i][j].clicked.connect(partial(this.__on_btn_clicked , btn_objects[i][j] ))
                
                this.button_layout.addWidget(btn_objects[i][j],i+1,j+1)

    
    def __on_btn_clicked(this,q) : this.inputbox.setText(this.inputbox.text()+q.text())

    def __evaluate(this) :
        try :
            x = eval(this.inputbox.text().replace("^","**").replace("÷","/").replace("x","*") )
            this.inputbox.setText(str(x))
        except ZeroDivisionError :
            this.__message_display("Division by Zero" , "Division by Zero found")
        except SyntaxError :
            this.__message_display("Invalid Syntax" , "Syntax of your expression is not valid")
        except :
            this.__message_display("Something went wrong" , "Please Checkout your expression again.")

    def __message_display(this, title : str , message : str) :

        qm = QMessageBox(text=message)
        qm.setWindowTitle(title)
        qm.setWindowIcon(this.icon)
        qm.setStyleSheet(open("CSS/QMessageBox.css").read())
        qm.exec()

if __name__ == "__main__" :
    Calc_UI()
