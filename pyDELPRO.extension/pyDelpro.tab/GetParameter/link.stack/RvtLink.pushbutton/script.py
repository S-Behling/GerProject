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
def open(doc_path):
    return HOST_APP.app.OpenDocumentFile(doc_path)

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

#Caminho do arquivo


#Informacoes sobre o arquivo                                
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


#Script
#LISTA CATEGORIAS
categorias = FileRvt.Settings.Categories
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
    or i.Name == "Data Devices" or i.Name == "Electrical Equipment" or i.Name == "Electrical Fixtures": # modelo generico
        lista_Categorias.append(i.Name)
        par_categorias.append(i)

for i in categorias:
    print("CATEGORIAS:")
    print(i.Name)

    EleCategoria = FilteredElementCollector(FileRvt)\
                                    .OfCategoryId(i.Id).WhereElementIsNotElementType().ToElements()
    
    print("IDs:")
    print(i.Id)
    print(EleCategoria)
    for j in EleCategoria:
        print("ELEMENTO")
        print(j.Name)
        parametros = j.Parameters
        print(parametros)
        for x in parametros:
            print(x.Definition.Name)
            
