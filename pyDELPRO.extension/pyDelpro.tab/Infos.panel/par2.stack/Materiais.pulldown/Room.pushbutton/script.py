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
from pyrevit import script

from Autodesk.Revit.DB import Transaction

try:
    clr.AddReference('RevitAPI')
    from Autodesk.Revit.DB import *

    clr.AddReference('Revit geo')
    from Autodesk.Revit.DB import Opitions
    from Autodesk.Revit.DB import Point
    from Autodesk.Revit.DB import Opening

    clr.AddReference('RevitServices')
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager

except:
    pass

import GerProject
#=============
#FUNCOES
#SELECIONA INSTANCIAS DA CATEGORIA ESCOLHIDA
def catCategorias(cat, tipo): 
    for i in categorias:
        if i.Name == cat:
            #SELECIONA TODOS OS TIPOS DA CATEGORIA
            if tipo == 1:
                Elementos= FilteredElementCollector(doc)\
                                                .OfCategoryId(i.Id).WhereElementIsElementType().ToElements()
            #SELECIONA TODAS AS INSTANCIAS DA CATEGORIA
            if tipo == 0:
                Elementos = FilteredElementCollector(doc)\
                                                .OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements() 
            if tipo == 2:  
                Elementos = FamilyType(doc)

            print (Elementos)
            return Elementos


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


def DelSubelements(ele):
    subelementos = ele.GetSubelements()
    print(subelementos)
    s = Transaction(doc, "search")
    s.Start()
    FamiliaLoad = doc.EditFamily(ele)
    print(familia)
    print(FamiliaLoad)
    categoriasFamilia = FamiliaLoad.Settings.Categories
    print(categoriasFamilia)
    #ele.DeleteSubelements(subelementos)
    #Finaliza edicao
    s.Commit()
    s.Dispose()
    return ele


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

#SELECIONA CAEGORIA ROOMS
msg = ("Rooms ou Spaces?")
RoomSpace = raw_input(msg)
Rooms = catCategorias(RoomSpace, 0)

#print(RoomSpace + " no modelo:")
#for i in Rooms:
    #print(i)
    #nome = i.LookupParameter("Name")
    #print(nome.AsValueString())

TodasCat = doc.Settings.Categories
TodasCategorias = GerProject.FiltraEle(TodasCat)
opt = Options()

VolumeTotal = 0
ListaVol = []
ListaIds = []

InSide = []
#PEGA ID DOS MATERIAIS
for r in Rooms:
    nomeR = r.LookupParameter("Name")
    if nomeR.AsValueString() == "area":
        GeometriaRoom = r.get_Geometry(opt) 
        geoRoom = GeometriaRoom.GetBoundingBox()
        GeoCentroRoom = (geoRoom.Max) - (geoRoom.Min)
        #print(GeoCentroRoom.X)
        pontoRoom = Point.Create(GeoCentroRoom)
        #print(pontoRoom)
        #print(GeoCentroRoom)
        #enum = Geometria.GetEnumerator()
        #next = enum.MoveNext()
        #solid = enum.Current

        #ELEMENTOS DETRO DO ROOM
        for c in TodasCategorias:
            nomeC = c.Name
            instancias = catCategorias(nomeC, 0)
            if instancias != None:
                for i in instancias:
                    Geometria = i.get_Geometry(opt) 
                    if Geometria != None:
                        geo1 = Geometria.GetBoundingBox()
                        GeoCentro = geo1.Min + ((geo1.Max) - (geo1.Min))
                        pon = Point.Create(GeoCentro)
                        ponto = pon.Coord

                        #P/ VERIFICAR AS COORDENADAS COM BASE NO ID (NO EXEMPLO > ID = 691131 )
                        """
                        if str(i.Id) == "691131":
                            print("----Z")
                            print(i.Id)
                            print(GeoCentro).Z
                            print(ponto.Z)
                            print((geoRoom.Min).Z)
                            print((geoRoom.Max).Z)
                            print("----")
                        """
                        

                        if ponto.X <= ((geoRoom.Max).X) and ponto.X >= ((geoRoom.Min).X):
                            #print("X")
                            if ponto.Y <= ((geoRoom.Max).Y) and ponto.Y >= ((geoRoom.Min).Y):
                                #print("Y")
                                #print("----Y")
                                #print(i.Id)
                                #print(ponto.Y)
                                #print((geoRoom.Min).Y)
                                #print((geoRoom.Max).Y)
                                if ponto.Z <= ((geoRoom.Max).Z) and ponto.Z >= ((geoRoom.Min).Z):
                                    #print("Z")
                                    InSide.append(i)
                                    #i = DelSubelements(i)
                                    volumes = GerProject.calculateVolume(i)
                                    #print("----")
                                    #print(i.Id)
                                    #print(volumes)
                                    VolumeTotal = VolumeTotal + volumes
                                    ListaIds.append(str(i.Id))
                                    ListaVol.append(volumes)
                                    volumes = 0
                                    #print("foi")
            nomeC = None
            instancias = None
                        
print("total")
print(InSide)
print(VolumeTotal)
print("convertido")
vol = VolumeTotal/3531
print(vol)
#print(ListaVol)
#print(ListaIds)