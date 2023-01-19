import clr
import os
import pathlib
import sys
import traceback
import json
import time


script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent.parent.parent.parent.parent), "libs")



sys.path.append(path_parent)

from System.Collections.Generic import*

import GerProject

#from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView
#from ui_parametros import Ui_MainWindow


from RVTAPI import APIFUNC

#pylint: disable=E0401,C0103
from pyrevit import*
from pyrevit import forms
from pyrevit.revit import files
from pyrevit.revit import RevitWrapper
from pyrevit import script

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

#TRANSFORMA VALOR NO TIPO DE VALOR CERTO
def ajustaTipo(par, val):
    #print(par)
    #print(str(par.StorageType))
    if str(par.StorageType) == "String":
        valor = str(val)

    if str(par.StorageType) == "Integer":
        valor = int(val)

    if str(par.StorageType) == "Double":
        valor = float(val)
    
    if str(par.StorageType) == "ElementId":
                print("Nao rola, Ids nao podem ser definidos pelo usuario")
    
    #else:
    #    print("Tipo de parametro invalido")
    #    return val
    
    return valor

#CONFERE INPUT DO USUARIO
#Tipos de input:
# 0 = sim e nao
# 1 = 0 e 1
# 2 = categoria
# 3 = parametro

def confereInput(inputUser, input, msg):
    count = 10
    for i in range(0,count):
        if input == 0:
            if ((inputUser == "s") or (inputUser == "n")):
                return inputUser
            else: 
                print("Valor invalido!")
                print(count-i)
                inputUser = raw_input(msg)
        if input == 1:
            if ((inputUser == "0") or (inputUser == "1")):
                return inputUser
            else:
                print("Valor invalido!")
                print(count-i)
                inputUser = raw_input(msg)
        if input == 2:
            for j in lista_Categorias:
                if (j == inputUser):
                    flag = 1
                    break
                else:
                    flag = 0

            if flag == 1:
                return inputUser
            if flag == 0:
                print("Valor invalido!")
                print(count-i)
                inputUser = raw_input(msg)

        if input == 3:
            for j in NomesParametros:
                if (j == inputUser):
                    flag = 1
                    break
                else:
                    flag = 0

            if flag == 1:
                return inputUser
            if flag == 0:
                print("Valor invalido!")
                print(count-i)
                inputUser = raw_input(msg)
        
    return inputUser

#PRINTA INFORMACOES DE INPUT
def RelatorioInputs(IputVal, par, cat, parRest, valRest):

    filtro = "<"
    if YesNo == "s":
        filtro = ("que possuiam o parametro  >" + parRest + "<  igual a  >" + valRest + "<")

    print("***************RELATORIO DE INPUTS******************")
    print("O valor  >" + IputVal + "<  foi aplicado ao parametro  >" + par + "<  em todos os(as)  >" + cat + filtro)

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

#FUNCAO ROTINA
print("***************************************************************************************")
print("Esta rotina le o parametro escolhido pelo usuario de todas as instancias de x categoria, \n e insere y valor definido pelo usuarios, sendo y uma string (parametro de texto ou numero)")
print("***************************************************************************************")
ok = raw_input("digite ok p/ contnuar, ou feche a janela p/ cancelar")

#FILTRA AS CATEGORIAS USADAS COM FREQUENCIA
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
print(lista_Categorias)
#USUARIO ESCOLHE A CATEGORIA (Tem que escrever certo o nome)
categoria = raw_input("Qual a categoria do elemento?")

#SE CATEGORIA DA LISTA = CATEGORIA ESCOLHIDA PELO USUARIO
count = 5
for i in range(0,count):
    EleCategoria = GerProject.catCategorias(categoria, 1) #funcao
    #print(EleCategoria)
    if EleCategoria == None:
        print("Categoria invalida!")
        print(count-i)
        categoria = raw_input("Qual a categoria do elemento?")
    else:
        break


print("> "+ categoria)
#IMPRIME ELEMENTOS DA CATEGORIA
#for j in EleCategoria:
#    print("ELEMENTOS:")
#    print(j.Name)

print("Parametros disponiveis: \n [")
parametros = EleCategoria[1].Parameters
NomesParametros = []
for x in parametros:
    NomesParametros.append(x.Definition.Name)
    print(x.Definition.Name)

print("] \n \n")

#APLICACAO DE FILTRO, SE NECESSARIO
msg = "Algum filtro aplicado aos elementos? \n sim -> s \n nao -> n"
YesNo = raw_input(msg)
YesNo = confereInput(YesNo, 0, msg)
print("> "+ YesNo)


if YesNo == "s":
    print("ex1 > elementos c/ parametro: \n Level = PAV 1 \n ex2> elementos com parametro: \n Type = Tubos pvc Tigre")
    print("Level, Type (parametro de restricao)")
    print("PAV 1, Tubos pvc Tigre (valor do parametro)")
    msg = "\nQual o parametro que voce deseja usar como restricao?"
    ParRestricao = raw_input(msg)
    ParRestricao = confereInput(ParRestricao, 3, msg)
    print("> "+ ParRestricao)
    ValRestricao = raw_input("Qual o valor x que esse parametro devera POSSUIR ou NAO POSSUIR")
    print("> "+ ValRestricao)
    tipoRestricao = raw_input("Todos os elementos que possuam o parametro com um valor igual a x (valor informado) -> 1 \
        \n Todos os elementos que NAO possuam o parametro com um valor diferente de x (valor informado) -> 0")
    tipoRestricao = confereInput(tipoRestricao, 1, msg)
    print("> "+ tipoRestricao)

    ElesCategoria = []
    for j in EleCategoria:
        GetRestricao = j.LookupParameter(ParRestricao)
        GetValor = GetRestricao.AsValueString()
        #valor = ajustaTipo(GetRestricao, GetValor)
        if tipoRestricao == "1":
            if GetValor == ValRestricao:
                ElesCategoria.append(j)
        if tipoRestricao == "0":
            if GetValor != ValRestricao:
                ElesCategoria.append(j)
        
else:
    ElesCategoria = EleCategoria

msg = "qual o parametro que voce deseja inserir um valor?"
parametroEdit = raw_input(msg)
parametroEdit = confereInput(parametroEdit, 3, msg)
print("> "+parametroEdit)
valor = raw_input("digite o valor a ser inserido")
print("> " + valor)

s = Transaction(doc, "search")
s.Start()
Sparametro = []
for j in ElesCategoria:

    parametros = j.Parameters
    parametro = j.LookupParameter(parametroEdit)
    if (str(parametro)) == "None":
        val = "not val"
        parametro.Set(val)
        Sparametro.append(j)

    if (str(parametro)) != "None":
        if str(parametro.Definition.Name) != str(parametroEdit):
            Sparametro.append(j)

        else:

            #Inicia Edicao
            TransactionManager.Instance.ForceCloseTransaction()

            valor = ajustaTipo(parametro, valor)
            parametro.Set(valor)

            TransactionManager.Instance.ForceCloseTransaction()

print("elementos que nao possuem o parametro")

#Finaliza edicao
s.Commit()
s.Dispose()

RelatorioInputs(valor, parametroEdit, categoria, ParRestricao, ValRestricao)

output = script.get_output()
output.close()

