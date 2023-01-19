import clr
import os
import pathlib
import sys
import traceback
import json
import time

script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent.parent.parent.parent), "libs")
path_parent2 = os.path.join(str(script_path.parent.parent.parent), "libs")
sys.path.append(path_parent2)
sys.path.append(path_parent)

from System.Collections.Generic import*

#from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView
#from ui_parametros import Ui_MainWindow


from RVTAPI import APIFUNC

try:
    clr.AddReference('RevitAPI')
    from Autodesk.Revit.DB import *

    clr.AddReference('RevitServices')
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager

except:
    pass

import GerProject


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
docs = app.Documents

#LISTA CATEGORIAS
categorias = doc.Settings.Categories
lista_Categorias = []
par_categorias = []

EleCategoria = FilteredElementCollector(doc)\
                                    .WhereElementIsNotElementType().ToElements()
                                    #.OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements()

CatOnDoc = []
CatOnDoc_name = []
for ele in EleCategoria:
    nomeCategoria = ele.Category
    if nomeCategoria != None:
        CatOnDoc_name.append(nomeCategoria.Name)
        CatOnDoc.append(ele.Category)


CatOnDoc = GerProject.uniqueName(CatOnDoc_name, CatOnDoc)
#print(CatOnDoc)

print("-----------------------------")
print("Categorias em uso no projeto:")
print("-----------------------------")

for e in CatOnDoc:
    print(e.Name)   
           
