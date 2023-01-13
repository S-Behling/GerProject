# Parameter Link rvt
import clr
import os
import pathlib
import sys
import traceback
import json
import time


script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent), "libs")
#n usado
path_parent2 = os.path.join(str(script_path.parent.parent.parent), "libs")

sys.path.append(path_parent)

#import ifcopenshell

from System.Collections.Generic import*

from RVTAPI import APIFUNC

#pylint: disable=E0401,C0103
#biblioteca pyrevit
from pyrevit import*
from pyrevit import forms
from pyrevit.revit import files
from pyrevit.revit import*
from pyrevit import EXEC_PARAMS, HOST_APP, DOCS

try:
    clr.AddReference('RevitAPI')
    from Autodesk.Revit.DB import *

    clr.AddReference('RevitServices')
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager

except:
    pass

#FUNCOES >>>

#Abre arquivo
def open(doc_path):
    return HOST_APP.app.OpenDocumentFile(doc_path)

def close(doc_path):
        """Close given document.

        Args:
            doc (DB.Document): document
        """
        return doc_path.Close()

#Seleciona categoria escolhida
def catCategorias(cat): 
    for i in categorias:
        if i.Name == cat:
            print(cat)
        #SELECIONA TODAS AS INSTANCIAS DA CATEGORIA
            EleCategoria = FilteredElementCollector(FileRvt)\
                                            .OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements()
            return EleCategoria

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

#<<<<<

#Documento selecionado
rvt_file = forms.pick_file(files_filter='Revit Files |*.rvt;*.rte;*.rfa|'
                                        'Revit Model |*.rvt|'
                                        'Revit Template |*.rte|'
                                        'Revit Family |*.rfa')

print(rvt_file)
FileRvt = open(rvt_file)

#Documento ativo
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
docs = app.Documents

#Infos arquivo aberto
rvtFile(rvt_file)

#Script
#LISTA CATEGORIAS
categorias = FileRvt.Settings.Categories
lista_Categorias = []
par_categorias = []

print("*****TODAS AS CATEGORIAS*****:")
for j in categorias:
    print(j.Name)


for i in categorias:
    #Filtro para eliminar categorias da lista
    #'Model Groups', 'Ramps', 'Cable Tray Fittings', 'Plumbing Fixtures', 'Lighting Devices', 'Curtain Systems', 'Parking', 'Ducts', 'Duct Fittings', 'Schedules', 
    #'Furniture Systems', 'Structural Framing', 'Electrical Fixtures', 'Lighting Fixtures', 'Generic Models', 
    #'Electrical Equipment', 'Curtain Panels', 'Windows', 'Sections', 'Room Tags', 'Curtain Wall Mullions', 'Structural Columns', 'Grids',
    #'Cable Trays', 'Materials', 'Specialty Equipment', 'Levels', 'Security Devices', 'Railings', 'Viewports', 'Structural Beam Systems', 'Views', 'Sheets', 'Casework', 
    #'View Titles', 'Mechanical Equipment', 'Stairs'
    if i.Name == "Cable Trays" or i.Name == "Cable Tray Fittings" or i.Name == "Communication Devices" or i.Name == "Conduits" or i.Name == "Conduit Fittings"\
    or i.Name == "Data Devices" or i.Name == "Electrical Equipment" or i.Name == "Electrical Fixtures" or i.Name == "Structural Columns"\
    or i.Name == "Structural Framing": # modelo generico
        lista_Categorias.append(i.Name)
        par_categorias.append(i)

print("*****CATEGORIAS SUGERIDAS*****:")
print(lista_Categorias)

#for i in categorias:
#    EleCategoria = FilteredElementCollector(FileRvt)\
#                                    .OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements()

categoriaEdiferente = 2
while (categoriaEdiferente != 0) and (categoriaEdiferente != 1):
    categoriaEdiferente = raw_input("A categoria do elemento de origem e diferente do elemento de destino? \n sim = 1 \n nao = 0")
    categoriaEdiferente = int(categoriaEdiferente)

if (categoriaEdiferente == 1):
    print("DEFINIR A EQUIVALENCIA DE ELEMENTOS, POSICAO, NOME, TAMANHO?")
    categoria = raw_input("Qual a categoria do elemento de origem?")
    categoria2 = raw_input("Qual a categoria do elemento de destino?")
    print(categoria)
    print(categoria2)
else:
    categoria = raw_input("Qual a categoria do elemento?")
    categoria2= categoria
    print(categoria)

#SE CATEGORIA DA LISTA = CATEGORIA ESCOLHIDA PELO USUARIO
count = 5
for i in range(0,count):
    EleCategoria = catCategorias(categoria) #funcao
    EleCategoria2 = catCategorias(categoria2) #funcao
    #print(EleCategoria)
    if EleCategoria == None:
        print("Categoria invalida!")
        print(count-i)
        categoria = raw_input("Qual a categoria do elemento?")
    elif EleCategoria2 == None:
        print("Categoria invalida!")
        print(count-i)
        categoria2 = raw_input("Qual a categoria do elemento?")
    else:
        break

print("PARAMETROS DISPONIVEIS ORIGEM:")  
p = EleCategoria[0].Parameters
for x in p:
        print(x.Definition.Name)

if (categoriaEdiferente == 1):
    print("PARAMETROS DISPONIVEIS DESTINO:")  
    p = EleCategoria2[0].Parameters
    for x in p:
            print(x.Definition.Name)
            
parametroOrigem = raw_input("qual o parametro original?")
parametroDes = raw_input("qual parametro de destino?")


if (categoriaEdiferente != 1):
    s = Transaction(FileRvt, "search")
    s.Start()
    Sparametro = []
    for j in EleCategoria:
        parametros = j.Parameters
        parametro = j.LookupParameter(parametroOrigem)
        parametroDestino = j.LookupParameter(parametroDes)
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
                #TransactionManager.Instance.ForceCloseTransaction()
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

                #TransactionManager.Instance.ForceCloseTransaction()

if (categoriaEdiferente == 1):
    print("desenvolver")


print("elementos que nao possuem o parametro")

s.Commit()
s.Dispose()

FileRvt2 = close(FileRvt)

            
