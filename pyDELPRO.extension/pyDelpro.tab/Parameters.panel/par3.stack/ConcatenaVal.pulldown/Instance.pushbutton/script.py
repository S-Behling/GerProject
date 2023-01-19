import clr
import os
import pathlib
import sys
import traceback
import json
import time

script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent.parent), "libs")

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

#FILTRA AS CATEGORIAS USADAS COM FREQUENCIA
for i in categorias:
    #Filtro para eliminar categorias da lista
    #'Model Groups', 'Ramps', 'Cable Tray Fittings', 'Plumbing Fixtures', 'Lighting Devices', 'Curtain Systems', 'Parking', 'Ducts', 'Duct Fittings', 'Schedules', 
    #'Furniture Systems', 'Structural Framing', 'Electrical Fixtures', 'Lighting Fixtures', 'Generic Models', 
    #'Electrical Equipment', 'Curtain Panels', 'Windows', 'Sections', 'Room Tags', 'Curtain Wall Mullions', 'Structural Columns', 'Grids',
    #'Cable Trays', 'Materials', 'Specialty Equipment', 'Levels', 'Security Devices', 'Railings', 'Viewports', 'Structural Beam Systems', 'Views', 'Sheets', 'Casework', 
    #'View Titles', 'Mechanical Equipment', 'Stairs'
    if i.Name == "Cable Trays" or i.Name == "Cable Tray Fittings" or i.Name == "Communication Devices" or i.Name == "Conduits" or i.Name == "Conduit Fittings"\
    or i.Name == "Data Devices" or i.Name == "Electrical Equipment" or i.Name == "Electrical Fixtures" or i.Name == "Pipes" or i.Name == "Pipe Fittings" or i.Name == "Structural Framing":
        lista_Categorias.append(i.Name)
        par_categorias.append(i)

#IMPRIME CATEGORIAS USUAIS
print(lista_Categorias)
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

#IMPRIME ELEMENTOS DA CATEGORIA
#for j in EleCategoria:
#    print("ELEMENTOS:")
#    print(j.Name)

print("Parametros disponiveis:")
parametros = EleCategoria[1].Parameters
for x in parametros:
        print(x.Definition.Name)

parametroOrigem = raw_input("qual o primeiro parametro a ser concatenado?")
parametroOrigem2 = raw_input("qual o segundo parametro a ser concatenado?")
parametroDes = raw_input("qual parametro de destino?")

s = Transaction(doc, "search")
s.Start()
Sparametro = []
for j in EleCategoria:
    parametros = j.Parameters
    parametro = j.LookupParameter(parametroOrigem)
    parametro2 = j.LookupParameter(parametroOrigem2)
    parametroDestino = j.LookupParameter(parametroDes)
    #print(parametro)
    if (str(parametro)) == "None":
        #val = "not val"
        #parametroDestino.Set(val)
        Sparametro.append(j)

    if (str(parametro)) != "None":
        if str(parametro.Definition.Name) != str(parametroOrigem):
            Sparametro.append(j)

        if str(parametro2.Definition.Name) != str(parametroOrigem2):
            Sparametro.append(j)

        else:
            #print(parametro.Definition.Name)
            #print(parametro.AsValueString())

            #IDENTIFICA O TIPO DO PARAMETRO DE DESTINO
            #print(parametroDestino.StorageType)

            #Inicia Edicao
            TransactionManager.Instance.ForceCloseTransaction()
            #TransactionManager.Instance.EnsureInTransaction(doc)
            #print(parametroDestino.StorageType)
            #print(parametro.StorageType)
            valor1 = parametro.AsValueString()
            valor2 = parametro2.AsValueString()
            valor = parametro + parametro2
            print(valor)
            #valor= int(valor)
            #valor = float(valor)
            #print("Double")
            #print(valor)
            if parametroDestino.AsValueString() != "not val":
                if str(parametroDestino.StorageType) == "String":
                    valor = parametro.AsValueString()
                    #print(valor)
                    #print("string")
                    parametroDestino.Set(str(valor))
                    #print(parametroDestino.AsValueString())
                    #print(parametroDestino)

                if str(parametroDestino.StorageType) == "Integer":
                    valor = parametro.AsValueString()
                    valor = int(valor)
                    #print("inteiro")
                    parametroDestino.Set(valor)

                if str(parametroDestino.StorageType) == "Double":
                    valor = parametro.AsValueString()
                    #valor= int(valor)
                    valor = float(valor)
                    #print("Double")
                    #print(valor)
                    parametroDestino.Set(valor)

                if str(parametroDestino.StorageType) == "ElementId":
                    valor = parametro.AsValueString()
                    valor = int(valor)
                    print("Id")
                    print(valor)
                    parametroDestino.Set(valor)

            TransactionManager.Instance.ForceCloseTransaction()

print("elementos que nao possuem o parametro")

#for i in Sparametro:
#    sVal = i.LookupParameter("Family Name")
#    print(sVal.AsValueString())

#semParametro = Sparametro[0].Parameters
#for x in parametros:
#        print(x.Definition.Name)
#Finaliza edicao
s.Commit()
s.Dispose()

