#-*-coding:utf-8-*-
# "My Journal version 1.0
# @kk 26-JAN-2023"
# Feature:
# 

# Note:
# Form design file: jishibenUI.py (converted from WindowsUI.ui)


from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QMenu, QDialog
from PyQt6.QtGui import *  # QTextcursor
from PyQt6.QtCore import Qt  # context menu
import sys
import time     # time stamp
import os       # open current dir

from jishibenUI import Ui_MainWindow 
from jishibenFindUI import Ui_Dialog     # uidialog: find windows

fname = 'jishiben.txt'

class NotePadWindow(QMainWindow, Ui_MainWindow):
    def __init__(self): # app init
        super(NotePadWindow,self).__init__()
        self.setupUi(self)
        self.show()
        self.load_file()                    # app init; load jishiben.txt by default
        self.plainTextEdit_2.setFocus()     # set focus
        self.createContextMenu              # right click menu
        #display window

        self.actionOpen.triggered.connect(self.open_file)
        self.actionExit.triggered.connect(self.exit_app)

        self.actionUndo.triggered.connect(self.plainTextEdit_2.undo)
        self.actionRedo.triggered.connect(self.plainTextEdit_2.redo)

        self.actionCut.triggered.connect(self.plainTextEdit_2.cut)
        self.actionCopy.triggered.connect(self.plainTextEdit_2.copy)
        self.actionPaste.triggered.connect(self.plainTextEdit_2.paste)
        self.actionFind.triggered.connect(self.find_window)  # Find next

        self.actionAbout.triggered.connect(self.about)
        # Binding MENU envent

        self.pushButton.clicked.connect(self.append_to_file)    # press ctrl+enter to publish
        self.find_dialog = find_dialog(self)
        # self.pushButton.clicked.connect(self.find_window)    #  findwindow不能有();有()就直接执行了。
        self.find_dialog.pushButton.clicked.connect(self.find_next)

        # highlight format
        self.format = QTextCharFormat()
        self.format.setBackground(QColor('yellow'))
        self.format.setForeground(QColor('red'))
        self.clearformat = QTextCharFormat()
        self.clearformat.setBackground(QColor('white'))
        self.clearformat.setForeground(QColor('black'))


    def open_file(self):
        global fname
        fname=QFileDialog.getOpenFileName(self, "Open File", '/home')

        if fname[0]:
            f = open(fname[0],'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)
                self.textEdit.moveCursor(QTextCursor.MoveOperation.End)

    # Initial display jishiben.txt
    def load_file(self): 
        if fname:
            f = open(fname,'r')

            with f:  
                text = f.read()  
                self.textEdit.setText(text)
                self.textEdit.moveCursor(QTextCursor.MoveOperation.End)

    def exit_app(self):
        self.close()

    def about(self):
        QMessageBox.about(self,"jishiben-QT", "做人，多少尴尬。"+'\n'+'算了，洗洗睡了~'+'\n')

    def createContextMenu(self): # mouse right click menu
        context_menu = QMenu(self)
        #create context menu

        # create cut, copy, paste action
        cut_action = QAction('Cut',self)
        cut_action.triggered.connect(self.plainTextEdit_2.cut)
        copy_action = QAction('Copy',self)
        copy_action.triggered.connect(self.plainTextEdit_2.copy)
        paste_action = QAction('Paste',self)
        paste_action.triggered.connect(self.plainTextEdit_2.paste)

        context_menu.addAction(cut_action)
        context_menu.addAction(copy_action)
        context_menu.addAction(paste_action)

        # bind Qmenu with Textedit
        # 将QMenu关联到QTextEdit上
        self.plainTextEdit_2.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.plainTextEdit_2.customContextMenuRequested.connect(lambda pos: context_menu.exec_(self.plainTextEdit_2.mapToGlobal(pos)))

    def append_to_file(self):
        input_text = self.plainTextEdit_2.toPlainText()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S") 
        if fname:
            f = open(fname,'a')

            with f:
                f.write(timestamp + "\n" + input_text + "\n\n")

        self.load_file()    # update display box

        # input box init        
        self.plainTextEdit_2.clear()
        self.plainTextEdit_2.setFocus()

    def find_window(self): # open find dialog window
        # self.find_dialog = find_dialog(self)    
        # Instance <-- object; declared in init part
        self.find_dialog.show()


    def find_next(self):
        # word to find
        searchStr = self.find_dialog.lineEdit.text()

        # # find next cursor init
        # cursor = self.textEdit.textCursor()
        # pos = cursor.position()
        # cursor.setPosition(0)
# ---------test area ----------------------------------------------
        # get the cursor position
        cursor = self.textEdit.textCursor() # define cursor
        position = cursor.position()

        if self.textEdit.find(searchStr):  # boolean
            cursor = self.textEdit.textCursor()
            cursor.mergeCharFormat(self.format)
            # display cursor position
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            text = cursor.selectedText()
            print('if section:')
            print(f'cursor.selectedText: {text} ')        

            # text = cursor.selectedText()
            # print(text+'find')
            # self.cursor.mergeCharFormat(self.format)
            # print('find')
            # output cursor position
            # cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            # text = cursor.selectedText()
            # print('if section:')
            # print(f'cursor.selectedText: {text} ')

        else:   # just reposition the cursor, no need to do charformat in ELSE section
            cursor.setPosition(0)
            self.textEdit.setTextCursor(cursor) # set cursor posion (the fir char of the document)!!!
            
            #display cursor postion
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            text = cursor.selectedText()
            print('ELSE section:')
            print(f'cursor.selectedText: {text} ')    
            
            self.find_next()
            # if self.textEdit.find(searchStr):
            #     cursor = self.textEdit.textCursor()     # so need update the position again after the first match.
            #     cursor.mergeCharFormat(self.format)
            #     cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            #     text = cursor.selectedText()
            #     print(text+'else')


#---------test -------------------------------
        # get the cursor position
        # cursor = self.textEdit.textCursor() # define cursor
        # position = cursor.position()
        # # cursor.mergeCharFormat(self.clearformat)


        # if self.textEdit.find(searchStr):

        # # Check if the cursor is at the end of the document
        # # if position == self.textEdit.document().characterCount():
        # if cursor.atEnd:
        #     # Reset the cursor to the beginning of the document
        #     cursor.setPosition(0)
        #     self.textEdit.setTextCursor(cursor)
        #     # cursor.insertText('INSERT',self.format)
        #     # output cursor position
        #     cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        #     text = cursor.selectedText()
        #     print('if section:')
        #     print(f'cursor.selectedText: {text} ')
        # else:
        #     cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        #     text = cursor.selectedText()
        #     print('else section:')
        #     print(f'cursor.selectedText: {text} ')
            # if self.textEdit.find(searchStr):  # boolean
                
            #     cursor=self.textEdit.textCursor()
            #     cursor.mergeCharFormat(self.format)
            # else:
            #     pass            

        # if not cursor.position(0):
        #     cursor.setPosition(0)
        #     self.textEdit.setTextCursor
        #     cursor.insertText('INSERT')
        # else:
        #     if self.textEdit.find(self.searchStr):  # boolean
        #         cursor=self.textEdit.textCursor()
        #     else:
        #         self


        # if self.textEdit.find('test'):
        #     cursor = self.textEdit.textCursor()
        #     cursor.mergeCharFormat(self.format) 


# ---------TIPS：code ----------------------------------------------
        # display cursor position
        # self.cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        # text = self.cursor.selectedText()
        # print(text+'find')

        # INSERT TEXT WITH FORMAT:
            # cursor.insertText('INSERT',self.format)  
            # cursor.insertText('INSERT')
        # SET POSITION:
            # cursor.setPosition(0)
        
        # highlight all
        # self.highlight_all(self.searchStr)
            
        # # init cursor position
        # cursor = self.textEdit.textCursor() # define cursor
        # cursor.setPosition(0) # cursor position
        # self.textEdit.setTextCursor(cursor)  # cursor in Textedit
# --------- END ----------------------------------------------
    

        # self.clear_highlight()

        # if self.textEdit.find(self.searchStr):  # boolean
        #     cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        #     cursor.insertText('find')
        #     # text = cursor.selectedText()
        #     # print(text+'find')
        #     # self.cursor.mergeCharFormat(self.format)
        #     # print('find')

        # else:   # just reposition the cursor, no need to do charformat in ELSE section
        #     cursor.setPosition(0)
        #     self.textEdit.setTextCursor(cursor) # set cursor posion (the fir char of the document)!!!
        #     self.find_next()
        #     # if self.textEdit.find(self.searchStr):
        #     #     cursor = self.textEdit.textCursor()     # so need update the position again after the first match.
        #     #     cursor.mergeCharFormat(self.format)
        #     #     cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        #     #     text = cursor.selectedText()
        #     #     print(text+'else')

        #     #     # pass
                


    def highlight(self):
        cursor = self.textEdit.textCursor() # true, then get the cursor position
        # set format
        text =cursor.selectedText()
        print(text)
        # cursor.mergeCharFormat(self.format) 
        # self.textEdit.setTextCursor(cursor)

    # hightlight text (mark all keyword in red color)
    def highlight_all(self, text):
        cursor = self.textEdit.document().find(text)
        while not cursor.isNull():
            cursor.mergeCharFormat(self.format)
            cursor = self.textEdit.document().find(text, cursor, QTextDocument.FindFlag(0))

    def clear_highlight(self):
        cursor_clear = self.textEdit.textCursor()
        cursor_clear.select(QTextCursor.SelectionType.Document)
        cursor_clear.setCharFormat(QTextCharFormat())
        cursor_clear.clearSelection()
        self.textEdit.setTextCursor(cursor_clear)


class find_dialog(QDialog,Ui_Dialog):
    def __init__(self,parent):
        super(find_dialog,self).__init__(parent)
        self.setupUi(self)

        self.pushButton.setText('Press me')
    #     self.pushButton.clicked.connect(self.find_text)
    
    # def find_text(self):
    #     text = self.lineEdit.text()
    #     QMessageBox.information(self, 'SearchStr', 'SearchStr:'+text)

    # def find_text(self):
    #     searchStr = self.lineEdit.text()

    #     self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)
    #     while self.text_edit.document().find(searchStr):
    #         self.text_edit.setTextCursor

    #     cursor = self.text_edit.document().find(searchStr,QTextCursor.MoveOperation.Start)
    #     if cursor.haslection():
    #         cursor.clearSelection()
    #     else:
    #         format = QTextCharFormat()
    #         format.setBackground(QColor('yellow'))
    #         format.setForeground(QColor('red'))
    #         cursor.mergecharFormat(format)
    #         self.text_edit.setTextCursor(cursor)



app=QApplication(sys.argv)
Note=NotePadWindow()    # main window; object --> instance
sys.exit(app.exec())
