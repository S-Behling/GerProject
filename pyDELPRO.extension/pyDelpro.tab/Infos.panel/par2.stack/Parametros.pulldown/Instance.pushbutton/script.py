import clr
import os
import pathlib
import sys
import traceback
import json
import time

script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent.parent.parent.parent.parent), "libs")
path_parent2 = os.path.join(str(script_path.parent.parent.parent), "libs")
sys.path.append(path_parent2)

sys.path.append(path_parent)

from System.Collections.Generic import*

#from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView
#from ui_parametros import Ui_MainWindow


from RVTAPI import APIFUNC

#pylint: disable=E0401,C0103
from pyrevit import*
from pyrevit import forms
from pyrevit.revit import files
from pyrevit.revit import RevitWrapper

from Autodesk.Revit.DB import Transaction

try:
    clr.AddReference('RevitAPI')
    from Autodesk.Revit.DB import *

    clr.AddReference('RevitServices')
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager

except:
    pass

import GerProject

#=============
#FUNCOES
#SELECIONA CATEGORIA ESCOLHIDA
def catCategorias(cat): 
    for i in categorias:
        if i.Name == cat:
            print(cat)
        #SELECIONA TODAS AS INSTANCIAS DA CATEGORIA
            EleCategoria = FilteredElementCollector(doc)\
                                            .OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements()
            return EleCategoria

#SELECIONA PARAMETRO
#def catParametro(par):
#__revit__.ActiveUIDocument.Document
             
#============   

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
docs = app.Documents

#LISTA TODAS AS CATEGORIAS
categorias = doc.Settings.Categories
lista_Categorias = []
par_categorias = []

for i in categorias:
    #Filtro para eliminar categorias da lista
    #'Model Groups', 'Ramps', 'Cable Tray Fittings', 'Plumbing Fixtures', 'Lighting Devices', 'Curtain Systems', 'Parking', 'Ducts', 'Duct Fittings', 'Schedules', 
    #'Furniture Systems', 'Structural Framing', 'Electrical Fixtures', 'Lighting Fixtures', 'Generic Models', 
    #'Electrical Equipment', 'Curtain Panels', 'Windows', 'Sections', 'Room Tags', 'Curtain Wall Mullions', 'Structural Columns', 'Grids',
    #'Cable Trays', 'Materials', 'Specialty Equipment', 'Levels', 'Security Devices', 'Railings', 'Viewports', 'Structural Beam Systems', 'Views', 'Sheets', 'Casework', 
    #'View Titles', 'Mechanical Equipment', 'Stairs'
    if i.Name == "Cable Trays" or i.Name == "Cable Tray Fittings" or i.Name == "Communication Devices" or i.Name == "Conduits" or i.Name == "Conduit Fittings"\
    or i.Name == "Data Devices" or i.Name == "Electrical Equipment" or i.Name == "Electrical Fixtures" or i.Name == "Pipes" or i.Name == "Pipe Fittings": 
        lista_Categorias.append(i.Name)
        par_categorias.append(i)

#IMPRIME CATEGORIAS USUAIS
GerProject.printCat(categorias)
#USUARIO ESCOLHE A CATEGORIA (Tem que escrever certo o nome)
categoria = raw_input("Qual a categoria do elemento?")
print(categoria)

#SE CATEGORIA DA LISTA = CATEGORIA ESCOLHIDA PELO USUARIO
count = 5
for i in range(0,count):
    EleCategoria = catCategorias(categoria) #funcao
    #print(EleCategoria)
    if EleCategoria == None:
        print("Categoria invalida!")
        print(count-i)
        categoria = raw_input("Qual a categoria do elemento?")
    else:
        break

print("============")
print("Nome categoria")
print(EleCategoria[0].Name)
print("============")
for ele in EleCategoria:
    print(ele.Name)
    if ele.Name == "Surface": #"Topography":
        print("flag")
        for x in ele:
            idEle = x.Id
            print(idEle)
            idMaterial = x.MaterialId
            print(idMaterial)
            volume = GetMaterialVolume(idMaterial)
            print(volume)
            geo = EleCategoria.Geometry


#IMPRIME ELEMENTOS DA CATEGORIA
#for j in EleCategoria:
#    print("ELEMENTOS:")
#    print(j.Name)

print("Parametros disponiveis:")
parametros = EleCategoria[0].Parameters
for x in parametros:
        print(x.Definition.Name)

msg = "verificar um ou todos os parametros? \n 1 -> um \n 2 -> todos"
umTodos = raw_input(msg)
int(umTodos)
if umTodos == 1:
    parametroOrigem = raw_input("qual o parametro voce deseja verificar?")

if umTodos == 1:
    for j in EleCategoria:
        #parametros = j.Parameters
        parametro = j.LookupParameter(parametroOrigem)
        parametro.AsValueString()
        print(parametroOrigem, parametro.AsValueString())
else:
    count = 0
    for j in EleCategoria:
        count = count + 1
        #parametros = j.Parameters
        parametros = j.Parameters
        print("ELEMENTO ")
        print(count)

        for p in parametros:
            parametroX = j.LookupParameter(p.Definition.Name)
            parametroX.AsValueString()
            if p.Definition.Name == "Elevation at Top":
                for x in parametroX:
                    print(x.AsValueString())

            print(p.Definition.Name, parametroX.AsValueString())