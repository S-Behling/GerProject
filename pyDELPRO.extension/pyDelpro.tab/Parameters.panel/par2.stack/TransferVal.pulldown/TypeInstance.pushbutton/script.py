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
#ELEMENTO E SEU TIPO
class Element:
    def __init__(self, STRnome, nome, type, familia):
        self.STRnome = STRnome
        self.nome = nome
        self.type = type
        self.familia = familia
        #self.STRtype = STRtype
    
    #Cria classe Element e insere as propriedades da instancia atual selecionada do revit
    #em seguida agrupa em uma lista todas essas instancias
    def getTypeInstance(instances):
        group = [] 
        for i in instances:
            strIns = i.Name
            ins = str(strIns)
            Tipo = i.LookupParameter("Type")
            nomeTipo = Tipo.AsValueString()
            ins = Element(strIns, i, nomeTipo, "nomeFamilia")
            print(ins.nome)
            group.append(ins) 
        return group

#FUNCOES
#SELECIONA CATEGORIA ESCOLHIDA
def catCategorias(cat, tipo): 
    for i in categorias:
        if i.Name == cat:
            print(cat)
            #SELECIONA TODOS OS TIPOS DA CATEGORIA
            if tipo == 1:
                Elementos= FilteredElementCollector(doc)\
                                                .OfCategoryId(i.Id).WhereElementIsElementType().ToElements()
            #SELECIONA TODAS AS INSTANCIAS DA CATEGORIA
            if tipo == 0:
                Elementos = FilteredElementCollector(doc)\
                                                .OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements()   
            print (Elementos)
            return Elementos    

#Pega o nome do tipo
def GetTypes(elemento):
    Tipo = elemento.LookupParameter("Type")
    nomeTipo = Tipo.AsValueString()

    return nomeTipo

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
    or i.Name == "Data Devices" or i.Name == "Electrical Equipment" or i.Name == "Electrical Fixtures" or i.Name == "Pipes" or i.Name == "Pipe Fittings": 
        lista_Categorias.append(i.Name)
        par_categorias.append(i)

tipo = 0 
#[INSTANCIA -> TIPO] OU [TIPO -> INTANCIA] ?
while (tipo == 0):
    print("A ordem do fluxo de dados e: ")
    print("1 - Parametro de Tipo -> Parametro de Instancia \n 2 - Parametro de Instancia -> Parametro de Tipo")
    tipo = input(int)
    print(tipo)

#IMPRIME CATEGORIAS USUAIS
print(lista_Categorias)
#USUARIO ESCOLHE A CATEGORIA (Tem que escrever certo o nome)
categoria = raw_input("Qual a categoria do elemento?")
print(categoria)

#SE CATEGORIA DA LISTA = CATEGORIA ESCOLHIDA PELO USUARIO
count = 5
for i in range(0,count):
    EleCategoria = catCategorias(categoria, 1) #funcao
    EleInsCategoria = catCategorias(categoria, 0)
    #print(EleCategoria)
    if EleCategoria == None:
        print("Categoria invalida!")
        print(count-i)
        categoria = raw_input("Qual a categoria do elemento?")
    else:
        break

print("Parametros de tipo disponiveis:")
parametros = EleCategoria[1].Parameters
for x in parametros:
        print(x.Definition.Name)

print("===============================")

print("Parametros de instancia disponiveis:")
parametros = EleInsCategoria[1].Parameters
for x in parametros:
        print(x.Definition.Name)

print("===============================")
 

parametroOrigem = raw_input("qual o parametro original?")
parametroDes = raw_input("qual parametro de destino?")

#Agrupa instancias por tipo
#GroupTypes = getTypeInstance(EleInsCategoria)

if tipo == 1:
    Categoria = EleCategoria
else:
    #ISSO AQUI N FAZ SENTIDO 
    Categoria = EleInsCategoria 

#PENSAR!!!!!!!!!!!!
#SEMPRE VAI SER DE TIPO PARA INSTANCIA?
#SE DE INSTANCIA PRA TIPO IRIA SOBREPOR VALORES
#UMA INSTANCIA -> UM TIPO
#UM TIPO -> VARIAS INSTANCIAS

s = Transaction(doc, "search")
s.Start()
Sparametro = []
for j in Categoria:
    parametros = j.Parameters
    parametro = j.LookupParameter(parametroOrigem)
    Tipo = j.LookupParameter("Type Name")
    nomeTipo = Tipo.AsValueString()

    for x in EleInsCategoria:
        parametroDestino = x.LookupParameter(parametroDes)
        Tipo = GetTypes(x)

        if nomeTipo == Tipo:
            if (str(parametro)) == "None":
                val = "not val"
                parametroDestino.Set(val)
                Sparametro.append(j)

            if (str(parametro)) != "None":
                if str(parametro.Definition.Name) != str(parametroOrigem):
                    Sparametro.append(j)

                else:
                    #print(parametro.Definition.Name)
                    #print(parametro.AsValueString())

                    #IDENTIFICA O TIPO DO PARAMETRO DE DESTINO
                    #print(parametroDestino.StorageType)

                    #Inicia Edicao
                    TransactionManager.Instance.ForceCloseTransaction()
                    #TransactionManager.Instance.EnsureInTransaction(doc)
                    
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
                        print("inteiro")
                        parametroDestino.Set(valor)

                    if str(parametroDestino.StorageType) == "Double":
                        valor = parametro.AsValueString()
                        valor = float(valor)
                        print("Double")
                        print(valor)
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

