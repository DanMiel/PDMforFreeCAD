# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2022 Dan Miel                                           *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
"""
This can be used to see information about part features or to measure between features.
Select one feature to view information or two features to see distance between them.
The distance also show the x ,y ,z between them.
Version.04
"""

from typing import Collection
import os
import FreeCAD
import FreeCADGui
from PySide import QtGui, QtCore
from PySide.QtGui import *
import math
import numpy
import Part
import Draft
from numpy import f2py
import sqlite3

class globaluseclass:
    def __init__(self, name):
        self.proplist = []
        self.cur = None
        self.con = None
        self.dbname = 'PDMDataBase.db'
        self.dbpath = 'C:/PDMFreeCADtest/'
        self.dbpartspath = 'C:/PDMFreeCADtest/dbparts'


g = globaluseclass("g")


class info:
    def __init__(self):
        self.fname = 'Empty'
        self.type = 'None'

   


    def __str__(self):
        return f'{self.fname, self.type}'



class database():
    def __init__(self):
        pass

    def addattributes(self):
        print('I;m running')
        form1.show()

    def createDatabase(self):       
        
        rows = g.cur.execute('SELECT CreatedBy FROM files').fetchall()

    def readdatabase(self, databasename):
        tablenames = []
        g.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = g.cur.fetchall()
        #tables = tables.replace(',',"")
        print('Tables')
        print(tables)
        for e in tables:
            tablenames.append(str(e).replace(',',''))

        colnamesDB = self.getcolnamesfrmDB(tablenames)
        for tablename in tablenames:
            print()

            g.cur.execute(f"select * from {tablename} limit 1")
            col_names=[i[0] for i in g.cur.description]
            print('all info in ' + tablename)
            print(col_names)
            
            qry = f'SELECT * FROM {tablename}'
            #qry = f'SELECT rowid FROM files'
            rows = g.cur.execute(qry).fetchall()

            for row in rows:
                print(row)



            #print(g.cur.lastrowid)
        

        g.cur.execute("select * from files limit 1")
        col_names=[i[0] for i in g.cur.description]

        #a = g.con.execute("PRAGMA table_info('files')")
        #print(a)
    def getcolnamesfrmDB(self, tablenames):
        for tablename in tablenames:
            print(tablename)
            g.cur.execute(f"select * from {tablename} limit 1")
            colnamesDB =[i[0] for i in g.cur.description]
        return(colnamesDB)

    def opendatebasesheet(self):
        print('In db sheet')
        import Spreadsheet
        page = FreeCAD.ActiveDocument.Page
        texts = page.Template.EditableTexts

        for key, value in texts.items():
            print("{0} = {1}".format(key, value))

        texts["FC-Title"] = "100001"
        page.Template.EditableTexts = texts
        

        #sf = FreeCAD.openDocument(g.dbpath + "Databaseinfo.FCStd")
        #ss = sf.getObject('Spreadsheet')

        #c = ss.A1
        #print(c)
        #for e in sf.Objects:
        ##ssc = sst.A1
        #    print(e.Name)
        
    def connectdb(self):
        dirExist = os.path.exists(g.dbpath)
        if dirExist == False:
            os.makedirs(g.dbpath)
        
        g.con = sqlite3.connect(g.dbpath + g.dbname)
        g.cur = g.con.cursor()
        kk = self.getdbcolumnnames()
        if len(kk) == 0:
            try:
                files = ''
                qry1 = 'Create TABLE files(fileID INTEGER PRIMARY KEY, FileName UNIQUE, Ver, Description CHAR(40), CreatedBy, FileType, Project, FilePath)'
                ##g.cur.execute(qry)
                #g.cur.execute('Create TABLE files(FileName, Ver, Description, CreatedBy, FileType, Project, FilePath)')
                
                
                #qry1 = 'Create TABLE IF NOT EXISTS files(fileID INTEGER PRIMARY KEY, FileName UNIQUE)'
                g.cur.execute(qry1)
            except Exception as e:
                print("qry1 error connecting to database\n" + str(e))

            try:
                qry2 = '''Create TABLE IF NOT EXISTS version(
                VerID INTERGER PRIMARY KEY,
                Ver,
                subfiles
                
                )'''
                                #FOREIGN KEY (VerID) REFERENCES files  (fileID)
                g.cur.execute(qry2)
            except Exception as e:
                print("qry2 error connecting to database\n" + str(e))
            try:
                qry3 = "INSERT INTO files (FileName) Values ('pole1')"
                g.cur.execute(qry3)
                #qry1 = f"INSERT INTO files (FileName) VALUES ('{filename}')"
            except Exception as e:
                print("qry3 error connecting to database\n" + str(e))
                
                
            try:   
                qry4 = "INSERT INTO version (Ver) Values ('00')"
                g.cur.execute(qry4)                
                g.con.commit()

                #qryjoin = 'SELECT files fileID, files.FileName, Version.VerID Version.Ver, subfiles\
                #from files INNER JOIN Versions'
                #g.cur.execute(qryjoin)
            except Exception as e:
                print("Qry4 error connecting to database\n" + str(e))
            try:
                qryjoin = 'SELECT files.*, Version.*\
                from files INNER JOIN Version'
                qryjoin = 'SELECT Ver, subfiles, FileName FROM files INNER JOIN version'


                g.cur.execute(qryjoin)
            except Exception as e:
                print("qryjoin error connecting to database\n" + str(e))

            g.con.commit()


            ViewData = g.cur.fetchall()
            for e in ViewData:
                print(e)
            #sqlite3.DataTableCompAndClient([ViewData])

    def searchprep(self):
        self.connectdb()
        #g.cur.execute("select * from files limit 1")
        #col_names=[i[0] for i in g.cur.description]
        col_names = self.getcolnamesfrmDB(['files'])
        form1.setsearchtable(col_names)

    def commit(self):
        g.con.commit()

    def dbclose(self):
        g.cur.close()
        g.con.close()
        print('database closed')

    

    def searchData(self):
        # Search database for text. Returns full rows.
        celltext = ''
        for num in range(form1.tm.columnCount()):
            header = form1.tm.horizontalHeaderItem(num).text()
            item = form1.tm.item(0, num)
            if item is None:
                continue
            celltext = item.text()
            if celltext != '':
                self.connectdb()
                qry = f"SELECT * FROM files where {header} LIKE '%{celltext}%'"
                rows = g.cur.execute(qry).fetchall()
                self.loadrowsfromsearch(rows)
                #rows = g.cur.execute("SELECT createdby FROM files where filetype = 'prt'").fetchall()
        form1.resizeTable()
        
    def loadrowsfromsearch(self, rows):
        # Writes search results to table.
        cols = form1.tm.columnCount()
        for rownum in range(0,len(rows)):
            info = rows[rownum]
            form1.tm.insertRow(rownum + 1)
            for col in range(0, cols):
                txt = QtGui.QTableWidgetItem(info[col])
                form1.tm.setItem(rownum + 1, col, txt)
        form1.resizeTable()

    def addDataToDataBase(self):
        # Add a new row from table to database
        self.connectdb()
        dbheaders = self.getdbcolumnnames()
        colinfo = []
        cells = []
        celltext = ''
        filename = ''
        for rownum in range(form1.tm.rowCount()):
            for colnum in range(form1.tm.columnCount()):
                item = form1.tm.item(rownum, colnum)
                if item is None:
                    celltext = ''
                else:
                    celltext = item.text()
                title = form1.tm.horizontalHeaderItem(colnum).text()
                if title == 'FileName':
                    filename = celltext
                else:
                    colinfo.append([form1.tm.horizontalHeaderItem(colnum).text(),celltext])
            # Insert check here
            qry = f"SELECT * FROM files where FileName = '{filename}'"
            rows = g.cur.execute(qry).fetchall()
            if len(rows) > 0:
                mApp('File already in database')
                return()
            qry1 = f"INSERT INTO files (FileName) VALUES ('{filename}')"

            g.cur.execute(qry1)
            g.con.commit()

            for item in colinfo:
                if item[0] in dbheaders:
                    if item[0] in 'fileID':
                        pass
                    else:
                        qry2 = f"UPDATE files set {item[0]} = '{item[1]}' WHERE FileName = '{filename}'"
                        g.cur.execute(qry2)
        g.con.commit()



    def addcolumn(self):
        # Add a new column to table        
        columnName = form1.txtboxColumnName.toPlainText()
        if columnName != "":
            self.connectdb()
            qry = f'ALTER TABLE files ADD {columnName}'
            g.cur.execute(qry)
            g.con.commit()

    def getdbcolumnnames(self):
        headers = []
        for num in range(form1.tm.columnCount()):
           headers.append(form1.tm.horizontalHeaderItem(num).text())
        return(headers)

    def getA2subparts(self,doc):
        # get a2+ sub part names
        subfiles = []
        for e in doc.Objects:
            p  = doc.getObject(e.Name)
            if hasattr(p,'sourceFile'):
                sfile = p.sourceFile.replace('.\\','')
                if sfile not in subfiles:
                    subfiles.append(sfile)
        return(subfiles)

    def makepropobj(self, doc):
        ob = doc.addObject("App::FeaturePython", 'Properties')
        ob.addProperty("App::PropertyString","FileName","Prop").FileName = doc.Label        
        ob.addProperty("App::PropertyString","Ver","Prop").Ver = ''
        ob.addProperty("App::PropertyString","FilePath","Prop").Ver = ''

        return(ob)

    def addfile(self):
        # Add file properties to table
        # get opened docs
        subfiles = []
        form1.clearTable()
        doc = FreeCAD.ActiveDocument
        fullpath = FreeCAD.ActiveDocument.FileName.rsplit("/",1)
        filename = fullpath[1]
        filepath = fullpath[0] + '/'

        propobj = doc.getObject('Properties')
        if propobj is None:
            propobj = self.makepropobj(doc)
        self.fillrow(filepath, propobj)

        docdic = FreeCAD.listDocuments()
        opendocs = []
        for v in docdic.values():
            opendocs.append( v.Name)
        if hasattr(propobj, 'FileType'):
            if '2' in propobj.FileType:
                subfiles = self.getA2subparts(doc)
                print(subfiles)
        d = None
        propobj = None
        for sf in subfiles:
            d = FreeCAD.openDocument(filepath + sf, hidden = True)
            propobj = d.getObject('Properties')
            if propobj is None:
                propobj = self.makepropobj(d)
            #rows = form1.tm.rowCount()
            
            self.fillrow(filepath, propobj)
            if not d.Name in opendocs:
                FreeCAD.closeDocument(d.Name)
        form1.resizeTable()
        FreeCAD.setActiveDocument(doc.Name)
        
    def fillrow(self, filepath, propobj = None):        
        
        rownum = form1.tm.rowCount()
        form1.tm.insertRow(rownum)        
        atturbutes = self.getdbcolumnnames()
        attlen = len(atturbutes)
        for col in range(1, attlen):            
            attname = atturbutes[col]
            if hasattr(propobj, attname):
                atttext = propobj.getPropertyByName(attname)
                txt = QtGui.QTableWidgetItem(atttext)
                form1.tm.setItem(rownum, col, txt)

database = database()


class formMain(QtGui.QMainWindow):

    def __init__(self, name):
        self.name = name
        super(formMain, self).__init__()
        self.setWindowTitle('PDM for FreeCAD')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(280, 250, 650, 550)
        self.setStyleSheet("font:10pt arial MS")                
        


        self.btnClose = QtGui.QPushButton(self)
        self.btnClose.move(130, 30)
        self.btnClose.setFixedWidth(70)
        self.btnClose.setFixedHeight(24)
        self.btnClose.setToolTip("Close dialog")
        self.btnClose.setText("Close")
        self.btnClose.clicked.connect(lambda:self.closeme())

        self.btnSearch = QtGui.QPushButton(self)
        self.btnSearch.move(210, 4)
        self.btnSearch.setFixedWidth(60)
        self.btnSearch.setFixedHeight(24)
        self.btnSearch.setToolTip("Search database.")
        self.btnSearch.setText("Search")
        self.btnSearch.clicked.connect(lambda:database.searchData())

        self.btnAddtoDB = QtGui.QPushButton(self)
        self.btnAddtoDB.move(90, 4)
        self.btnAddtoDB.setFixedWidth(70)
        self.btnAddtoDB.setFixedHeight(24)
        self.btnAddtoDB.setToolTip("Add first row to database.")
        self.btnAddtoDB.setText("Add to DB")
        self.btnAddtoDB.clicked.connect(lambda:database.addDataToDataBase())
        
        self.btnClear = QtGui.QPushButton(self)
        self.btnClear.move(160, 4)
        self.btnClear.setFixedWidth(60)
        self.btnClear.setFixedHeight(24)
        self.btnClear.setToolTip("Clear table.")
        self.btnClear.setText("Clear")
        self.btnClear.clicked.connect(lambda:database.searchprep())

        self.btnAddFileInfo = QtGui.QPushButton(self)
        self.btnAddFileInfo.move(4, 4)
        self.btnAddFileInfo.setFixedWidth(80)
        self.btnAddFileInfo.setFixedHeight(24)
        self.btnAddFileInfo.setToolTip('Add Active file data to table')
        self.btnAddFileInfo.setText('Add File info')
        self.btnAddFileInfo.clicked.connect(lambda:database.addfile())
        
        
        
        self.btnreadfiles = QtGui.QPushButton(self)
        self.btnreadfiles.move(500, 4)
        self.btnreadfiles.setFixedWidth(80)
        self.btnreadfiles.setFixedHeight(24)
        self.btnreadfiles.setToolTip('Read the information in the database')
        self.btnreadfiles.setText('Read files')
        self.btnreadfiles.clicked.connect(lambda:database.readdatabase('Files'))
        #self.btnreadfiles.clicked.connect(lambda:database.getTableList())
        

        self.btnAddColumn = QtGui.QPushButton(self)
        self.btnAddColumn.move(500, 30)
        self.btnAddColumn.setFixedWidth(80)
        self.btnAddColumn.setFixedHeight(24)
        self.btnAddColumn.setToolTip("Add column to file DataBase")
        self.btnAddColumn.setText("Add Column")
        self.btnAddColumn.clicked.connect(lambda:database.addcolumn())
        
        self.txtboxColumnName = QtGui.QTextEdit(self)
        self.txtboxColumnName.setGeometry(500, 54, 100, 30) # xy, wh
        self.txtboxColumnName.setToolTip("Enter name for new BD column.")
        
        
        """ Main Table """
        self.tm = QtGui.QTableWidget(self)

    
    def setsearchtable(self, colnames):
        self.tm.setRowCount(0)
        self.tm.setGeometry(10, 90, 600, 350)  # xy,wh
        self.tm.setWindowTitle("Broken Constraints")
        #self.tm.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.tm.setRowCount(1)
        self.tm.setColumnCount(len(colnames))
        self.tm.setMouseTracking(True)
        #self.tm.cellClicked.connect(self.cell_was_clicked)
        self.tm.setHorizontalHeaderLabels(colnames)
         
        self.tm.horizontalHeader().sectionClicked.connect(self.fun)


    def resizeTable(self):
        header = self.tm.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        for row in range(self.tm.rowCount()):
            self.tm.setRowHeight(row, 15)


    def fun(self, i):
        # click in column header to sort column
        self.tm.sortByColumn(i)


    def SaveClose(self):
        self.saveProperties()

    def addrow(self):
        rows = self.tm.rowCount()
        self.tm.insertRow(0)


    def clearTable(self):
        self.tm.setRowCount(0)


    def resizeEvent(self, event):
        # resize table
        formx = self.width()
        formy = self.height()
        self.tm.resize(formx - 20, formy - 150)
        self.btnClose.move(300, formy - 30)
        self.btnSearch.move(195, formy - 30)
        #self.btnOpenSearch.move(10, formy - 30)
        
    def showme(self, msg):
        self.show()

    def closeme(self):
        self.close()

    def closeEvent(self, event):
        database.dbclose()
        print('Shut down in closeEvent')

form1 = formMain('form1')

#class SelObserver:
#    def __init__(self):
#        pass
#    def SelObserverON(self):
#        if g.sONOFF != 'on':
#            FreeCADGui.Selection.addObserver(selObv)
#            g.sONOFF = 'on'
#            # print('SelObserverON')
#    def SelObserverOFF(self):
#        try:
#            FreeCADGui.Selection.removeObserver(selObv)
#            g.sONOFF = 'off'
#            # print('SelObserverOFF')
#        except Exception as e:
#            print('Error2 = ' + str(e))
#    def addSelection(self, doc, obj, sub, pnt): # Selection object
#        print(obj)
#        test = FreeCAD.ActiveDocument.getObject(obj)
#        if test is None:
#            pass
#        elif 'AssmInfo' in test.Content:
#            form1.txtboxConName.setText(obj)
#        else:
#            onebutton.readselect(onebutton, doc, obj, sub)
#            modmeasure.measureSelected()
#    def removeSelection(self, doc, obj, sub): # Delete the selected object
#        print('In remove')
#        #modmeasure.measureSelected()
#selObv = SelObserver()


toolTipText = \
"""
Select pointsMoves Parts
Selecting two will show the distance and information of both features.

"""

class PDMforFreeCAD:
    def GetResources(self):
        mypath = os.path.dirname(__file__)
        return {
             'Pixmap': mypath + "/Icons/PDMforFreeCAD.svg",
             'MenuText': 'PDM for FreeCAD',
             'ToolTip': 'PDMforFreeCAD'
             }

    def Activated(self, placeholder = None):        
        if FreeCAD.activeDocument() is None:
            mApp('No file is opened.You must open a file first.')
            return
        database.searchprep()
        form1.showme('delete me')
    #def Deactivated(self):
    #    """This function is executed when the workbench is deactivated."""
    #    #selObv.SelObserverOFF()
    #    print('Deactivated')

    #def IsEnabled(self):
    #    return()

    #def IsActive(self):
    #    return(True)
FreeCADGui.addCommand('PDMforFreeCADTool', PDMforFreeCAD())
#==============================================================================

class mApp(QtGui.QWidget):
    """This message box was added to make this file a standalone file"""
    # for error messages
    def __init__(self, msg, msgtype ='ok'):
        super().__init__()
        self.title = 'Properties'
        self.initUI(msg)

    def initUI(self, msg, msgtype = 'ok'):
        self.setGeometry(100, 200, 320, 200)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        if msgtype == 'ok':
            buttonReply = QtGui.QMessageBox.question(self, "Information", msg, QtGui.QMessageBox.Ok|QtGui.QMessageBox.Ok)
        if msgtype == 'yn':
            buttonReply = QtGui.QMessageBox.question(self, "Information", msg, QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if buttonReply == QtGui.QMessageBox.Yes:
           #properties.createPropertyobject()
           print('Yes clicked.')
        else:
            
           print('No clicked.')
        return(buttonReply)
        #self.show()
        
