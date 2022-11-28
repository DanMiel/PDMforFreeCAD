# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2022 Dan Miel                                           *
#*                                                                         *
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

''' 
Quick Measure program
written by Dan Miel
'''
import os
import FreeCADGui

import PDMforFreeCAD
class FreeCADDataBase (Workbench):

    def __init__(self):
        import PDM_dict
        mypath = PDM_dict.getdir(None)
        print('in dir ' + mypath)
        self.__class__.Icon = mypath + "/Icons/PDMforFreeCAD.svg"
        self.__class__.MenuText = 'DataBase FreeCAD'

    def Initialize(self):
        FreeCADGui.updateLocale()

        DataBaseMenu = [
            'PDMforFreeCADTool'
            ]
       
        self.appendToolbar(
           'PDM Menu',
           DataBaseMenu
           )
           
    def Activated(self):
        pass

    def Deactivated(self):
        pass
Gui.addWorkbench(FreeCADDataBase())