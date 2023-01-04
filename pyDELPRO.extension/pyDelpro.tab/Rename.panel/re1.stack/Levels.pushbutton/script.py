import clr
import os
import pathlib
import sys
import traceback
import json
import time

script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent), "libs")

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
print("Esta rotina renomeia os pavimentos.")
print("***************************************************************************************")
ok = raw_input("digite ok p/ contnuar, ou feche a janela p/ cancelar")

#SELECIONA PAVIMENTOS
Pavimentos = catCategorias("Levels") #funcao

print("PAVIMENTOS:")
#IMPRIME ELEMENTOS DA CATEGORIA
for j in Pavimentos:
    print(j.Name)

print("Parametros disponiveis: \n [")
parametros = Pavimentos[1].Parameters
NomesParametros = []
for x in parametros:
    NomesParametros.append(x.Definition.Name)
    print(x.Definition.Name)

print("] \n \n")

#APLICACAO DE FILTRO, SE NECESSARIO
msg = "Algum filtro aplicado aos elementos? \n sim -> s \n nao -> n"
YesNo = raw_input(msg)
YesNo = confereInput(YesNo, 0, msg)


print(YesNo)

if YesNo == "s":
    print("ex1 > elementos c/ parametro: \n Level = PAV 1 \n ex2> elementos com parametro: \n Type = Tubos pvc Tigre")
    print("Level, Type (parametro de restricao)")
    print("PAV 1, Tubos pvc Tigre (valor do parametro)")
    msg = "\nQual o parametro que voce deseja usar como restricao?"
    ParRestricao = raw_input(msg)
    ParRestricao = confereInput(ParRestricao, 3, msg)
    ValRestricao = raw_input("Qual o valor x que esse parametro devera POSSUIR ou NAO POSSUIR")
    tipoRestricao = raw_input("Todos os elementos que possuam o parametro com um valor igual a x (valor informado) -> 1 \
        \n Todos os elementos que NAO possuam o parametro com um valor diferente de x (valor informado) -> 0")
    tipoRestricao = confereInput(tipoRestricao, 1, msg)

    PavimentoF = []
    for j in Pavimentos:
        GetRestricao = j.LookupParameter(ParRestricao)
        GetValor = GetRestricao.AsValueString()
        valor = ajustaTipo(GetRestricao, GetValor)
        if tipoRestricao == "1":
            if GetValor == ValRestricao:
                PavimentoF.append(j)
        if tipoRestricao == "0":
            if GetValor != ValRestricao:
                PavimentoF.append(j)
        
else:
    PavimentoF = Pavimentos

s = Transaction(doc, "search")
s.Start()
Sparametro = []
for j in PavimentoF:

    parametros = j.Parameters
    parametro = j.LookupParameter("Name")

    #Inicia Edicao
    TransactionManager.Instance.ForceCloseTransaction()

    print("Nome atual:")
    print(parametro.AsValueString())
    valor = raw_input("Novo valor:")
    if valor != "":
        parametro.Set(valor)
    else:
        print("sem alteracao")

    TransactionManager.Instance.ForceCloseTransaction()

print("elementos que nao possuem o parametro")

#Finaliza edicao
s.Commit()
s.Dispose()

output = script.get_output()
output.close()

