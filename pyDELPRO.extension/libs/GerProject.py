import clr
import os
import pathlib
import sys



script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent), "libs")

sys.path.append(path_parent)

from System.Collections.Generic import*

from RVTAPI import APIFUNC

#pylint: disable=E0401,C0103
from pyrevit import*
from pyrevit import forms
from pyrevit.revit import files
from pyrevit.revit import RevitWrapper
from pyrevit import script
from pyrevit import EXEC_PARAMS, HOST_APP, DOCS

from Autodesk.Revit.DB import Transaction


#p/ usa biblioteca colar na funcao
#sys.path.append(path_parent2)
#path_parent2 = os.path.join(str(script_path.parent.parent.parent), "libs")
#import GerProject


try:
    clr.AddReference('RevitAPI')
    from Autodesk.Revit.DB import *

    clr.AddReference('RevitServices')
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager

except:
    pass

#**********************************************************************
#FUNCOES GerProject
#By Simone Behling

#>>> CATEGORIA E PARAMETROS <<<
#SELECIONA CATEGORIA ESCOLHIDA
#sendo > cat = categoria; Tdoc = documento (ativo ou externo); tipo = se tipo(1), se instancia(0)
def catCategorias(cat, tipo, Tdoc):
    categorias = doc.Settings.Categories
    for i in categorias:
        if i.Name == cat:
            print(cat)
            #SELECIONA TODOS OS TIPOS DA CATEGORIA
            if tipo == 1:
                Elementos= FilteredElementCollector(Tdoc)\
                                                .OfCategoryId(i.Id).WhereElementIsElementType().ToElements()
            #SELECIONA TODAS AS INSTANCIAS DA CATEGORIA
            if tipo == 0:
                Elementos = FilteredElementCollector(Tdoc)\
                                                .OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements()   
            print (Elementos)
            return Elementos

#Pega o nome do tipo
def GetTypes(elemento):
    Tipo = elemento.LookupParameter("Type")
    nomeTipo = Tipo.AsValueString()

    return nomeTipo

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

#printa elementos

def printCat(eles):
    for e in eles:
        print(e.Name)



#>>> DOCUMENTACAO <<<

#PRINTA INFORMACOES DE INPUT
def RelatorioInputs(IputVal, par, cat, parRest, valRest):

    filtro = "<"
    if YesNo == "s":
        filtro = ("que possuiam o parametro  >" + parRest + "<  igual a  >" + valRest + "<")

    print("***************RELATORIO DE INPUTS******************")
    print("O valor  >" + IputVal + "<  foi aplicado ao parametro  >" + par + "<  em todos os(as)  >" + cat + filtro)

#ARQUIVOS EXTERNOS (RVT)

#Abre arquivo
def open(doc_path):
    return HOST_APP.app.OpenDocumentFile(doc_path)

def close(doc_path):
        """Close given document.

        Args:
            doc (DB.Document): document
        """
        return doc_path.Close()


#Printa Informacoes sobre o arquivo 
def rvtFile(rvt_file):                              
    if rvt_file:
        mfile = files.get_file_info(rvt_file)
        fileRVT = str(mfile)
        print(fileRVT)
        #Abre o arquivo
        #FileRvt = open(rvt_file)
        print("=============================")
        #print(FileRvt)
        print("Informacoes sobre o arquivo:" )
        print("Created in: {0} ({1}({2}))".format(mfile.RevitProduct.Name,
                                                mfile.RevitProduct.BuildNumber,
                                                mfile.RevitProduct.BuildTarget))
        print("Workshared: {0}".format("Yes" if mfile.IsWorkshared else "No"))
        if mfile.IsWorkshared:
            print("Central Model Path: {0}".format(mfile.CentralModelPath))
        print("Last Saved Path: {0}".format(mfile.LastSavedPath))
        print("Document Id: {0}".format(mfile.UniqueId))
        print("Open Workset Settings: {0}".format(mfile.OpenWorksetConfig))
        print("Document Increment: {0}".format(mfile.DocumentIncrement))

        print("Project Information (Properties):")
        for k, v in sorted(dict(mfile.ProjectInfoProperties).items()):
            print('\t{} = {}'.format(k, v))

        if mfile.IsFamily:
            print("Model is a Revit Family!")
            print("Category Name: {0}".format(mfile.CategoryName))
            print("Host Category Name: {0}".format(mfile.HostCategoryName))
        print("=============================")


#>>> AREA E VOLUME <<<

def calculateVolume (ele):
    volumeEleTnt = 0
    cat = ele.Category.Name
    print(cat)
    if cat == "Structural Columns" or cat == "Structural Connections" or cat == "Structural Framing" or cat == "Structural Framing (Other)":
        parVol = ele.LookupParameter("Volume")
        volumeEleTnt = parVol.AsDouble()
        #print(volumeEleTnt)
        return volumeEleTnt
    if cat == "Structural Foundations":
        parVol = ele.LookupParameter("Volume")
        volumeEleTnt = parVol.AsDouble()
        volumeEleTnt = - volumeEleTnt
        return volumeEleTnt

    return volumeEleTnt


def calculateVolumeSTR (ele):
    volumeEleTnt = 0
    cat = ele.Category.Name
    print(cat)
    if cat == "Structural Columns" or cat == "Structural Connections" or cat == "Structural Framing" or cat == "Structural Framing (Other)" or cat == "Structural Foundations":
        subelementos = GetSubelements(ele)
        parVol = ele.LookupParameter("Volume")
        volumeEle = float(parVol.AsValueString())
        #print(volumeEle)
        volumeEleTnt = parVol.AsDouble()
        #print(volumeEleTnt)
        
        return volumeEle
    return volumeEle


def FiltraEle(categoria):
    elementos = []
    for c in categoria:
        cat = c.Name
        print(cat)
        if cat == "Structural Columns" or cat == "Structural Connections" or cat == "Structural Framing" or cat == "Structural Framing (Other)" or cat == "Structural Foundations":
            elementos.append(c)
    
    return elementos