#! python3
# ifc
import clr
import os
import pathlib
import sys
import traceback

script_path = pathlib.Path(__file__).parent.absolute()
path_parent = os.path.join(str(script_path.parent), "libs")

sys.path.append(path_parent)

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView
from ifc_compare_ui import Ui_MainWindow

import ifcopenshell
from ifcopenshell import geom

#import FreeCAD
#import Part

from RVTAPI import APIFUNC

try:
    clr.AddReference('RevitAPI')
    from Autodesk.Revit.DB import *

    clr.AddReference('RevitServices')
    from RevitServices.Persistence import DocumentManager
    from RevitServices.Transactions import TransactionManager

except:
    pass



uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = doc.Application
docs = app.Documents


#<<<END

#>>>>>SELECT ELEMENTS AND PARAMETERS > RVT
#Select Columns in project 
RVTColumns = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_StructuralColumns)\
            .WhereElementIsNotElementType()\
            .ToElements()

#Select Floors in project
RVTFloors = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_Floors)\
            .WhereElementIsNotElementType()\
            .ToElements()

RVTFraming = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_StructuralFraming)\
            .WhereElementIsNotElementType()\
            .ToElements()

# SELECT CATEGORIES > RVT
#list Rvt categories
RVTcategories = doc.Settings.Categories
RVTelements = []
par_RVTelements = []
for i in RVTcategories:
    if i.Name == "Floors" or i.Name == "Columns" or i.Name == "Structural Framing" or i.Name == "Structural Columns":
        RVTelements.append(i.Name)
        par_RVTelements.append(i)


settings = geom.settings()
settings.set(settings.USER_BREP_DATA, True)


ifc_file = ""

    
class MyEnvironment:
    def __init__(self):
        self.Desktop = os.path.join(self.GetUserPath(), "Desktop")
        
    def GetUserPath(self):
        if 'HOME' in os.environ:
            return os.environ['HOME']
        elif os.name == 'posix':
            return os.path.expanduser("~/")
        elif os.name == 'nt':
            if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
                return os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
        else:
            return os.environ['HOMEPATH']


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #self.types(self)

        def SelectPath():
            print("--------")
            self.path = QFileDialog.getOpenFileName()

            
            self.lineEdit_folder.setText(str(self.path))
            
            self.ifc_file = ifcopenshell.open(self.path[0])
            self.types = self.ifc_file.types()

            #print(obj_info).keys()
            # elements = ifc_file.by_type('IfcProduct')
            
            PopulateSelectElementIFC()
            PopulateSelectElementRevit(RVTelements)
            

        def PopulateSelectElementIFC():
          
            #seleciona elementos IFC
            for type in self.types:
                self.comboBox_IFCelement_2.addItem(type, type) 


        def PopulateSelectElementRevit(RVTelements):
            #seleciona elementos Revit
            
            for type in RVTelements:
                self.comboBox_RVTelement.addItem(type, type)

        def PopulateSelectParametersIFC():

            #Select elements by current index
            selectEleIfc = self.comboBox_IFCelement_2.currentIndex()
            #selectEleIfc = self.comboBox_IFCparameter.currentIndex()
            list_types = self.types

            elements = self.ifc_file.by_type(list_types[selectEleIfc-1]) #'IfcColumn')
            obj_info = elements[0].get_info()

            #list parameters by current type
            self.select_types = self.ifc_file.by_type(list_types[selectEleIfc-1])
            #self.select_types = self.ifc_file.by_type(list_types[selectEleIfc])
            print(self.select_types)
            #select any element to get the parameters 

            shape = shape.create_shape(settings, self.select_types[0])

            par_info = self.select_types[0].get_info()
            #List parameters
            for type in par_info:
                self.comboBox_IFCparameter.addItem(type, type)
            
            #get id from selected parameter 
            if self.comboBox_IFCparameter.currentIndexChanged:
                self.selectPar = self.comboBox_IFCparameter.currentIndex()
                #self.selectPar = self.comboBox_IFCelement_2.currentIndex()

            PopulateElementsTable(elements)
            #wall = self.ifc_file.by_type(list_types[selectEleIfc-1])
            #print(wall[0].GlobalId)
            #test = par_info[self.selectPar]
            #print(wall[0].test)
 
        
        def PopulateSelectParametersRVT():

            #Get current Id in combo box
            selectIdRvt = self.comboBox_RVTelement.currentIndex()
            #Get category contained in this Id
            self.selectCat = par_RVTelements[selectIdRvt-1]
            #Get Id of category
            IdCat = self.selectCat.Id
            
            #list all elements in this category
            self.RVTElementsbyCat = FilteredElementCollector(doc)\
                                 .OfCategoryId(IdCat).WhereElementIsNotElementType().ToElements()
            
            #NAO ESTA FUNCIONANDO PARA COLUNA
            allParam1 = []
            for RvtPar in self.RVTElementsbyCat[1].Parameters:
	            allParam1.append(RvtPar.Definition.Name)
            #print(allParam1)

            for type in allParam1:
                self.comboBox_RVTparameter.addItem(type, type)

        def ClearRows():
            while self.tableWidget_all.rowCount() > 0:
                self.tableWidget_all.removeRow(0)

        def PopulateElementsTable(elements):
            #seleciona elementos IFC
            ClearRows()

            #print(elements[0].GlobalId)
            for e in elements:
                rowPosition = self.tableWidget_all.rowCount()
                #print(rowPosition)
                self.tableWidget_all.insertRow(rowPosition) 
                self.tableWidget_all.setItem(rowPosition , 0, QTableWidgetItem(e.GlobalId))
                self.tableWidget_all.setItem(rowPosition , 1, QTableWidgetItem(e.Name))
                print(e.ObjectPlacement)
                #self.tableWidget_all.setItem(rowPosition , 2, QTableWidgetItem(e.ObjectPlacement))
                #self.tableWidget_all.setItem(rowPosition , 3, QTableWidgetItem(e.Name))

        #def Refresh():
    
        def Done():
            
            #tipo selecionado IFC
            self.IFCselect_element = self.comboBox_IFCelement_2.currentText()
            #tipo selecionado Rvt
            self.RVTselect_element = self.comboBox_RVTelement.currentText() 
            #parametro selecionado Rvt
            self.RVTselect_parameter = self.comboBox_RVTparameter.currentText()
            self.RVTselect_parameter2 = self.comboBox_RVTparameter.currentData()
            #parametro selecionado IFC
            self.IFCselect_parameter = self.comboBox_IFCparameter.currentText()
            self.IFCselect_parameter2 = self.comboBox_IFCparameter.currentData()
            #IFCindex = self.comboBox_IFCparameter.currentIndex()  

            #IFCget_par = self.select_types[IFCindex].get_info()
            #todos os elementos da categoria selecionada
            IFClista_tipos = self.select_types
            RVTlista_tipos = self.RVTElementsbyCat

            IFC_selectPar = self.selectPar #index
            IFC_selectPar2 = str(self.IFCselect_parameter) #text
            IFC_selectParData = self.IFCselect_parameter2 #data


            #REMOVE CARACTERES ESPECIAIS DOS PARAMETROS IFC
            lista_limpa = []
            nova_lista = []
            lista_completa = []
            element_info = []
            for i in IFClista_tipos:
                # i = 1 elemento
                aux = i.get_info() 
                aux2 = str(aux)
                # aux = i.Name
                #element_info.append(aux2)
                infos_split = [aux2.split(",")]
                for x in infos_split:
                    #print("x={[id:123,... ")
                    # x = 1 elemento como string
                    for k in x:
                        #print("K={[id:123")
                        #k = 1 palavra
                        for j in k:
                            
                            # j = 1 letra
                            if j == " ": 
                                k = k.replace(j," ")
                            elif j == "{": 
                                k = k.replace(j," ")
                            elif j == "'":
                                k = k.replace(j,"")
                            elif j =="}" :
                                k = k.replace(j,"")
                            elif j == "(":
                                k = k.replace(j,"")
                            elif j == ")":
                                k = k.replace(j,"")
                    
                        nova_lista.append(k) 
                    #lista com todos os elementos e seus parametros correspondentes      
                    lista_limpa.append(nova_lista)
                    nova_lista = [] 

            #PROCURA ELEMENTOS "PARAMETRO DE PROCURA" PARA VERIFICAR A DIFERENCA DE COORDENADAS ENTRE MODELOS
            coordenada_ifc = []
            coordenada_rvt = []
            aux = 0
            
            a = 1
            for i in IFClista_tipos:
                if a < len(IFClista_tipos):
                    prox = IFClista_tipos[a]
                else:
                    pass
                for j in RVTlista_tipos:
                    aux_ifc = i.Name #alterar parametro de procura OU pegar id e depois pegar valor correspondente
                    aux_rvt = j.LookupParameter('Mark') #alterar parametro de procura
                    if aux_rvt.HasValue:
                        aux_rvt = aux_rvt.AsString()
                        #print(aux_rvt)
                        #print(aux_ifc)
                        inicializa = i.ObjectPlacement.RelativePlacement.Location[0][2]
                        if aux_ifc == aux_rvt:
                            print("achou")
                            print(aux_rvt)
                            print(aux_ifc)
                            #coordenada_rvt 
                            point = j.Location.Point
                            pointX = point.X
                            pointY = point.Y
                            pointZ = point.Z
                            coordenada_rvt.append([point.X, point.Y, point.Z])
                            #coordenada ifc
                            IFCpointX = prox.ObjectPlacement.RelativePlacement.Location[0][0]
                            IFCpointY = prox.ObjectPlacement.RelativePlacement.Location[0][1]
                            IFCpointZ = prox.ObjectPlacement.RelativePlacement.Location[0][2]
                            coordenada_ifc.append([i.ObjectPlacement.RelativePlacement.Location[0][0], i.ObjectPlacement.RelativePlacement.Location[0][1], i.ObjectPlacement.RelativePlacement.Location[0][2]])
                            if inicializa < prox.ObjectPlacement.RelativePlacement.Location[0][2] and prox.Name == aux_rvt:
                                point = j.Location.Point
                                pointX = point.X
                                pointY = point.Y
                                pointZ = point.Z
                                coordenada_rvt.append([point.X, point.Y, point.Z])
                                #coordenada ifc
                                IFCpointX = prox.ObjectPlacement.RelativePlacement.Location[0][0]
                                IFCpointY = prox.ObjectPlacement.RelativePlacement.Location[0][1]
                                IFCpointZ = prox.ObjectPlacement.RelativePlacement.Location[0][2]
                                coordenada_ifc.append([prox.ObjectPlacement.RelativePlacement.Location[0][0], prox.ObjectPlacement.RelativePlacement.Location[0][1], prox.ObjectPlacement.RelativePlacement.Location[0][2]])
                                aux = aux + 1
                            break

                
                        else:
                            pass
                    else:
                        pass
                a = a + 1
                if aux > 10:
                    break
                else:
                    pass

            #CALCULA A DIFERENCA ENTRE AS COORDENADAS DE UM ELEMENTO DE CADA MODELOx
            Xdif = pointX - IFCpointX
            Ydif = pointY - IFCpointY
            Zdif = pointZ - IFCpointZ

            # Xdif = coordenada_rvt[0][0] - (coordenada_ifc[0][0])
            # Ydif =  coordenada_rvt[0][1] - (coordenada_ifc[0][1])
            # Zdif =  coordenada_rvt[0][2] - (coordenada_ifc[0][2])
            print(Xdif)

            lista_parametros = lista_limpa[0]
            print(lista_parametros[0])
            print("--------------")
            info_index = 0
            nmr = 0
            
            positionIFC = []
            positionIFC_prox = []
            positionRVT = []
            i=0

            TransactionManager.Instance.EnsureInTransaction(doc)

            #percorre elementos RVT
            for ele in RVTlista_tipos:
                
                i = 0
                #percorre elementos IFC str
                for str_ele in lista_limpa:
                    #percorre elementos TFC
                    IFCele = IFClista_tipos[i]
                   
                    #coordenada rvt elemento atual 
                    point = ele.Location.Point
                    pointX = point.X - Xdif
                    pointY = point.Y - Ydif
                    pointZ = point.Z - Zdif
                    positionRVT.append([pointX, pointY, pointZ])

                    #coordenada ifc
                    positionIFC.append([IFCele.ObjectPlacement.RelativePlacement.Location[0][0], IFCele.ObjectPlacement.RelativePlacement.Location[0][1], IFCele.ObjectPlacement.RelativePlacement.Location[0][2]])
                    IFCpointX = IFCele.ObjectPlacement.RelativePlacement.Location[0][0]
                    IFCpointY = IFCele.ObjectPlacement.RelativePlacement.Location[0][1]
                    IFCpointZ = IFCele.ObjectPlacement.RelativePlacement.Location[0][2]

                    if i+1 < len(IFClista_tipos):
                        #coordenada proximo elemento IFC
                        prox_IFCpointX = IFClista_tipos[i+1].ObjectPlacement.RelativePlacement.Location[0][0]
                        prox_IFCpointY = IFClista_tipos[i+1].ObjectPlacement.RelativePlacement.Location[0][1]
                        prox_IFCpointZ = IFClista_tipos[i+1].ObjectPlacement.RelativePlacement.Location[0][2]
                        positionIFC_prox.append([IFClista_tipos[i+1].ObjectPlacement.RelativePlacement.Location[0][0], IFClista_tipos[i+1].ObjectPlacement.RelativePlacement.Location[0][1], IFClista_tipos[i+1].ObjectPlacement.RelativePlacement.Location[0][2]])
                        # print("---------")
                        # print(pointX)
                        # print(IFCpointX)
                        # print("---------")
                    else:
                        break

                    if (pointZ - IFCpointZ) < 3 and (pointZ - IFCpointZ) > -3 :
                        if (pointX - IFCpointX) < 3 and (pointX - IFCpointX) > -3 and (pointY - IFCpointY) < 3 and (pointY- IFCpointY) > -3:
                            pull = ele
                            push = IFCele
                            print("sub")
                            print(pointX)
                            print(pointZ)
                            print(pointY)
                            print(pointX - IFCpointX)
                            print(pointZ - IFCpointZ)
                            print(pointY - IFCpointY)
                            # print("IFC")
                            # print(IFCpointX)
                            # print ("RVT")
                            # print(pointX)
                            if (IFCpointX - pointX) > (prox_IFCpointX - pointX) and (IFCpointY - pointY) > (prox_IFCpointY - pointY) and (IFCpointZ - pointZ) > (prox_IFCpointZ - pointZ):
                                pull = ele
                                push = IFClista_tipos[i+1]
                                print("IFC_PROX")
                                print(prox_IFCpointX)
                                print ("RVT_PROX")
                                print(pointX)
                                positionIFC = []
                                positionRVT = []
                                print("coordenada")

                                #percorre parametros de x IFC str
                            for par in str_ele:
                                au = IFCele.get_info()
                                # teste = au.keys(value_par)
                                # print(teste)
                                # au2 = str(au)
                                # infos_split = au2.split(",")
                                # print(infos_split[0])
                                # print(self.comboBox_IFCparameter.currentIndex())
                                # print(self.selectPar)
                                # index = infos_split[self.comboBox_IFCparameter.currentIndex()]
                                # if "'" in index:
                                #     index = index.replace("'","")
                                    
                                # else:
                                #     print("index")
                                #     print(index)

                                # split_index =  index.split(":")
                                # value_index = split_index[1]
                               
                                if ":" in par:
                                    split_par =  par.split(":")
                                    nome_par = split_par[0]
                                    value_par = split_par[1]

                                    teste = au.keys()
                                    teste1 = str(teste)
                                    split_index =  teste1.split(",")
                                    print(split_index)
                                    nome_index = split_index[self.comboBox_IFCparameter.currentIndex()-1]
                                    print(nome_index)
                                    print(nome_par)
                                    if "'" in nome_index:
                                        nome_index = nome_index.replace("'","")
                                    else:
                                        pass
                                    if nome_index == nome_par:
                                        print("1")
                                        #seleciona parametro Mark do Rvt
                                        aux_rvt = ele.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
                                        #seta valor do parametro mark do elemento atual do revit com value_par
                                        aux_rvt.Set(value_par)
                                            
                                        #aux_rvt = ele.LookupParameter('Mark')
                                        # if value_par == value_index:
                                        #     print("2")
                                        #     ele.SetparameterByName('Mark', value_par)
                                        #     
                                        # else:
                                        #     pass
                                    else:
                                        pass    
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass

                    i= i+1
            
            TransactionManager.Instance.TransactionTaskDone()

            #-----------------------------

            #Separa string do nome do parametro
            infos_extract = lista_parametros[11] #[info_index] #name
            print(infos_extract)
            pa =  infos_extract.split(":")
            #pega valor atribuido ao parametro
            nome_parametro = pa[0]
            valor_parametro = pa[1]
            print(nome_parametro)
            print(valor_parametro)

            
            #melhoria codigo abaixo
                #CorrespondenciaElementos = [('IfcColumns', 'Structural Columns'),('Structural Frame, Bean')]
                #print(CorrespondenciaElementos[0][1])

            RVTselect = str(self.RVTselect_element)
            IFCselect = self.IFCselect_element
            IFCajuste_aux = 0
            IFCajuste_cat = 0
            RVTajuste_cat =[]
            RVTpoints = []
            RVTListEle = []
            RVTListCat =[]
            saju = 0
            #par_RVTelements = Categoria RVT
            for cat in par_RVTelements:
                for i in self.RVTElementsbyCat:
                    # Se o elemento selecionado do ifc... 
                    # for IfcColumns, remove str Ifc
                    if IFCselect == 'IfcColumn':
                        IFCajuste_aux = IFCselect
                        IFCajuste_cat = 'Columns'
                                            
                    # for IfcBean, passa a ser Structural Columns
                    if IFCselect == 'IfcBean':
                        IFCajuste_aux = IFCselect
                        IFCajuste_cat = 'Columns'
                        
                    # contem Ifc no nome, remove str Ifc
                    if IFCajuste_cat == 0:
                        fullstring = IFCselect
                        substring = "Ifc"
                        if substring in fullstring:
                            IFCajuste_aux = IFCselect.split("Ifc")
                            IFCajuste_cat = IFCajuste_aux[1]
                        
                    #Se a categoria selecionada do Rvt for Structural Columns, remove str Structural
                    if cat.Name == 'Structural Columns':
                        RVTajuste_aux = str(cat.Name).split(" ")
                        saju = RVTajuste_aux[1]
                        #RVTajuste_cat.append(saju)   

                    # Se o elemento selecionado do rvt for = o elemento iterado
                    if IFCajuste_cat == cat.Name or IFCajuste_cat == saju or IFCselect == cat.Name or IFCselect == saju:
                        RVTListCat.append(cat)
                        RVTListEle.append(i)
                        
                        
            #RVTele_instance = []
            RVTvalue = []    
            for i in RVTListEle:
                aux = i.LookupParameter(str(self.RVTselect_parameter))
                if aux.HasValue:
                    print(teste.AsString())
                    RVTvalue.append(j)
                    #RVTele_instance.append(par)
                    print("aqui")

            IFCListEle = self.select_types
            #print(self.select_types)
            IFCaux = []    
            for j in IFCListEle: #criar lista com elementos do ifc de acordo com o q foi selecionado em IFCelement
                teste2 = j.get_info() #ver metodo > ifc fiz acima quando separo as strings
                for k in teste2:
                    if k == nome_parametro:
                        info = j[info_index]
                        par =  info.split(":")
                        #pega valor atribuido ao parametro
                        nome_parametro1 = pa[0]
                        valor_parametro1 = par[1]

                        # print(teste2)
                        # print(k)
            IFCaux.append(j)

            #FAZER O MESMO PARA IFC E COMPARAR OS RESULTADOS
            # self.selectPar
            # IFCListEle = self.select_types
            # IFCaux = []    
            # for j in IFCListEle: #criar lista com elementos do ifc de acordo com o q foi selecionado em IFCelement
            #     #teste2 = par.get_info() #ver metodo > ifc fiz acima quando separo as strings
            #     teste3 = j.(self.selectPar):
            #     print(teste2)
            #     print(teste3)
            #     IFCaux.append(j)
                    
                    
            # if i > 20:
            #     break
            # IFCaux = valor_parametro
            # print(IFCaux)

            """
            #RVTselect_element = Categoria selecionada no RVT
            if RVTajuste_cat == IFCajuste_cat:
                print("===============================================")
                RVTaux = cat.GetParameters(self.RVTselect_parameter)
                print(RVTaux.GetValue())
                IFCaux = nome_parametro
                print(IFCaux)
                if RVTaux == IFCaux:
                
                    #Coordinates by Location > Structural Framing
                    if self.selectCat.Name == "Structural Framing":
                        #coord = [self.RVTElementsbyCat[0].Location.Curve.GetEndPoint(0), self.RVTElementsbyCat[0].Location.Curve.GetEndPoint(1)]
                        SF_location = cat.Location #self.RVTElementsbyCat[0]
                        startpoint = cat.Location.Curve.GetEndPoint(0)
                        startpointX = startpoint.X
                        startpointY = startpoint.Y
                        startpointZ = startpoint.Z
                        #print(startpoint)

                        endpoint = cat.Location.Curve.GetEndPoint(1)
                        endpointX = endpoint.X
                        endpointY = endpoint.Y
                        endpointZ = endpoint.Z
                        RVTpoints.append([((startpoint.X + endpoint.X)/2), ((startpoint.Y-endpoint.Y)/2), ((startpoint.Z-endpoint.Z)/2)])
                        #print(RVTpoints)
                    
                    #print(self.selectCat.Name)
                    #Coordinates by Location > Structural Columns
                    if self.selectCat.Name == "Structural Columns":
                        SC_location = cat.Location
                        point = cat.Location.Point
                        pointX = point.X
                        pointY = point.Y
                        pointZ = point.Z
                        RVTpoints.append([point.X, point.Y, point.Z])
                        # print(pointX)
                        # print(point)
            """
            #print(RVTpoints[1])
                #Coordinates by Location > Floors
                #if self.selectCat.Name == "Floors":
                #Location = Class Location
            
            #METODO P/ CONFERIR SE O IFC SELECIONADO NA PASTA É O MESMO INSERIDO NO RVT
            #METODO LE ESSE IFC PELO REVIT PARA PEGAR A SUA ORIGEM
            #Select link 
            Links = FilteredElementCollector(doc)\
            .OfCategory(BuiltInCategory.OST_RvtLinks)\
            .WhereElementIsNotElementType()\
            .ToElements()

            #Pega o nome do arquivo pelo Rvt
            for i in Links:
                link = (i.Name)
            
            nome,tipo = link.split(":")
            #print(nome)

            #Pega nome do arquivo pela Pasta
            path_name = str(self.path)
            nome = path_name.split("/")
            nmr = 0
            for i in nome:
                nmr = nmr + 1

            NomeSeparado = (nome[nmr-1]).split("',")

            IfcName = NomeSeparado[0]
            #print(IfcName)
            nome_ifc = str(IfcName)

            #Select the link if your Name = Name ifc_file
            # i=0
            # while (nome != nome_ifc):
            #     if nome == nome_ifc:
            #         LinkRvt = nome
            #     if i > 30:
            #         print("Arquivo não encontrado!")
            #         break
            #     i = i + 1
            # print(LinkRvt)
            #-------------------------

            # print("-----------------------")
            # print(self.RVTElementsbyCat[0].Name)
            # print(par_RVTelements[0].Name)
            # print(self.RVTselect_element)

            RVTpoints = []
            for i in self.RVTElementsbyCat:
                if i.Name == self.RVTselect_element:
                    if self.selectCat.Name == "Structural Framing":
                        #coord = [self.RVTElementsbyCat[0].Location.Curve.GetEndPoint(0), self.RVTElementsbyCat[0].Location.Curve.GetEndPoint(1)]
                        SF_location = cat.Location #self.RVTElementsbyCat[0]
                        startpoint = cat.Location.Curve.GetEndPoint(0)
                        startpointX = startpoint.X
                        startpointY = startpoint.Y
                        startpointZ = startpoint.Z
                        #print(startpoint)

                        endpoint = cat.Location.Curve.GetEndPoint(1)
                        endpointX = endpoint.X
                        endpointY = endpoint.Y
                        endpointZ = endpoint.Z
                        RVTpoints.append([((startpoint.X + endpoint.X)/2), ((startpoint.Y-endpoint.Y)/2), ((startpoint.Z-endpoint.Z)/2)])
                        #print(RVTpoints)
                    
                    #print(self.selectCat.Name)
                    #Coordinates by Location > Structural Columns
                    if self.selectCat.Name == "Structural Columns":
                        SC_location = cat.Location
                        point = cat.Location.Point
                        pointX = point.X
                        pointY = point.Y
                        pointZ = point.Z
                        RVTpoints.append([point.X, point.Y, point.Z])
                        # print(pointX)
                        # print(point)
            
            #Diferença entre origens
            #RVToriginproject base point - IFCorigin internal origin = diference

            #Select Coordinates IFC           
            products = self.select_types
            for j in RVTpoints:
                i = 0
                position = []
                for product in self.select_types:
                    #position.append([product.Name, product.ObjectPlacement.RelativePlacement.Location[0][0], product.ObjectPlacement.RelativePlacement.Location[0][1]])
                    position.append([product.ObjectPlacement.RelativePlacement.Location[0][0], product.ObjectPlacement.RelativePlacement.Location[0][1], product.ObjectPlacement.RelativePlacement.Location[0][2]])
                    #print(position)
                    posicao_ele = product.ObjectPlacement.RelativePlacement.Location[0][0]
                    #print(position)
                    if j == position:
                         print("FOOI")
                    #     j.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).Set.(self.RVTselect_parameter))
               

            """  if position[0][0] == j.location[0][0]:
                    if position[0][1] == j.location[0][1]:
                         if position[0][2] == j.location[0][2]:
                            #se posicao dos elementos for a mesma, seta o parametro do rvt
                            TransactionManager.Instance.EnsureInTransaction(doc)
                            seta = j.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
                            conf = seta.Set(new_Value)
                            TransactionManager.Instance.TransactionTaskDone()
                        else: break
                    else: break
                else: break
    """




            # print(types)
            # return out_names, out_par

        # def FeedViewsTable():
        #     collector = FilteredElementCollector(doc).OfClass(View3D).ToElements()
        #     for v in collector:
        #         if not v.IsTemplate:
        #             # Create a new row
        #             rowPosition = self.tableWidget_all.rowCount()
        #             self.tableWidget_all.insertRow(rowPosition)
        #             # Populate this row
        #             self.tableWidget_all.setItem(rowPosition , 0, QTableWidgetItem(str(v.Id)))
        #             self.tableWidget_all.setItem(rowPosition , 1, QTableWidgetItem(v.Name))
        #     header = self.tableWidget_all.horizontalHeader()
        #     header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        #     header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        # FeedViewsTable()

        self.btn_folder.clicked.connect(SelectPath)
        #sinal combobox
        self.comboBox_IFCelement_2.currentIndexChanged.connect(PopulateSelectParametersIFC)
        self.comboBox_RVTelement.currentIndexChanged.connect(PopulateSelectParametersRVT)
        self.comboBox_RVTparameter.currentIndexChanged.connect(Done)
        #self.pushButton_refresh.clicked.connect(PopulateElementsTable)
        

        print(ifc_file)


    # Buttons actions
    
if __name__=="__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
        ui = MainWindow()
        ui.show()
        #main()
        app.exec_()

