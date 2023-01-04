#! python3

"""Teste descricaoo"""

import clr
import os
import pathlib
import sys
import traceback
import json
import time

script_path = pathlib.Path(__file__).parent.absolute()
#path_parent = os.path.join(str(script_path.parent.parent.parent), "libs")
path_parent = os.path.join(str(script_path.parent), "libs")


sys.path.append(path_parent)

from System.Collections.Generic import*

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QHeaderView
from ui_parametros import Ui_MainWindow


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

#LISTA CATEGORIAS
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
    if i.Name == "Pipe Accessories" or i.Name == "Pipe Fittings" or i.Name == "Pipes" or i.Name == "Doors" or i.Name == "Colums"\
    or i.Name == "Rooms" or i.Name == "Roofs" or i.Name == "Furniture": # modelo generico
        lista_Categorias.append(i.Name)
        par_categorias.append(i)


def setParameter(ele, eleDes, nome):
    #nome = nome.replace("\'", "\"")
    
    strselectPar = str(selectPar)
    TipoOrigem
    TipoDestino
    parametroOrigem = par.GetParameters("strselectPar")
    parametroDestino
    value = eleDes[nome]
    param = ele.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
    param.Set(value)
    #print(param.AsString())

    

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
        
        #print("--------")
        print(lista_Categorias)

        #=================================================
        #Popula comboBox com categorias:
        for type in lista_Categorias:
            type = str(type)
            self.comboBox_categoriaOrigem.addItem(type, type)
            self.comboBox_categoriaDestino.addItem(type, type)
            self.comboBox_categoriaOrigem2.addItem(type, type)


        #=================================================
        #Ativa/Desativa comboBox 'categoria de destino' Se check
        def ActivateCatDestino():
            #Ativa
            if not self.checkBox_mesmaCategoria.checkState():
                self.comboBox_categoriaDestino.setEnabled(1)    
            #Desativa 
            else:
                self.comboBox_categoriaDestino.setEnabled(0)

        #=================================================
        #Ativa/Desativa comboBox 'familia de destino' Se check
        def ActivateTypesDestino():
            #Ativa
            if not self.checkBox_mesmaFamilia.checkState(): 
                self.comboBox_familiaDestino.setEnabled(1) 
            #Desativa      
            else:
                self.comboBox_familiaDestino.setEnabled(0)
            
            PopulateTypesDestino()
         
        #=================================================
        #Popula tipos de acordo com categoria selecionada
        def PopulateTypes():

            #ORIGEM
            
            #Guarda categoria selecionada pelo usuario
            SelectCategoria = self.comboBox_categoriaOrigem.currentIndex()
            self.Categoria = par_categorias[SelectCategoria-1]

            #Seleciona Id da Categoria
            IdCat = self.Categoria.Id
            #print(IdCat)
            
            
            #Familia instanciada ou tipos

            #Se tipo
            if not self.checkBox_familiaInstancia.checkState():

                #lista tipos da categoria
                self.ElementsbyCat = FilteredElementCollector(doc)\
                                    .OfCategoryId(IdCat).WhereElementIsElementType().ToElements()

                #print("Tipo")

                i = 0
                ElementsbyCats = []
                Types = []
                for ele in self.ElementsbyCat:
                    ElementsbyCats.append(ele.FamilyName)
                    ParametroType = ele.GetParameters("Type Name")
                    Types.append(ParametroType[i].AsString())
                    # print(ele.FamilyName)
                    # print(ele.GetType())
                    #para = ele.GetOrderedParameters()
                    
                    # print(pras[0].AsString(), "for")
                    # for p in pras:
                    #     print(p.AsString())
                    
                    # OBS: dois tipos de familia, familia carregada/familysymbol e familia do modelo/familytype
                    # familysymbol: familia = nome do elemento; familytype: family = parede basica, parede cortina e type = tijolos, ceramica...  

                #Popula comboBox Familias
                self.tipos = []
                for type in Types: #ElementsbyCats:
                    self.comboBox_FamiliaOrigem.addItem(type, type)
                    self.tipos.append(type)

                #Se mesma categoria
                if self.checkBox_mesmaCategoria.checkState():
                    for type in Types: #ElementsbyCats:
                        self.comboBox_familiaDestino.addItem(type, type)
                else:
                    PopulateTypesDestino()

                    
            #Se instancia    
            else:

                #Seleciona instancias da categoria
                self.ElementsbyCat = FilteredElementCollector(doc)\
                                    .OfCategoryId(IdCat).WhereElementIsNotElementType().ToElements()

                #print("Instancias")
                #Seleciona instancias
                self.ElementsbyCats = []
                #self.OrgData = []
                for ele in self.ElementsbyCat:
                    #self.OrgData.append(ele)
                    self.ElementsbyCats.append(ele.Name)
                    #print(ele.Name)

                myset = set(self.ElementsbyCats)
                self.UniqueEleCats = list(myset)
                print(self.UniqueEleCats)
                print(myset)
                
                #IdEle = ele.GetTypeId
                                
                #Popula comboBox Familias
                #self.tipos = []
                #i = 0
                for type in self.UniqueEleCats:
                    self.comboBox_FamiliaOrigem.addItem(type, type)
                    #print(t, "t")  #pegar instancias da categoria
                    #self.tipos.append(t)
                   # i = i + 1
                
                #Se mesma categoria
                if self.checkBox_mesmaCategoria.checkState():
                    for type in ElementsbyCats:
                        self.comboBox_familiaDestino.addItem(type, type)
                
                else:
                    PopulateTypesDestino()
 
        #======================================================
        #Popula tipos de destino se categorias != 
        #de acordo com a categoria selecionada
        def PopulateTypesDestino():
            #Popula combobox Familias Destino
            SelectCategoriaDes = self.comboBox_categoriaDestino.currentIndex()
            self.CategoriaDes = par_categorias[SelectCategoriaDes-1]
            IdCatDes = self.CategoriaDes.Id

            #Se Types 
            if not self.checkBox_familiaInstancia.checkState():
                #lista tipos da categoria
                self.ElementsbyCatDes = FilteredElementCollector(doc)\
                                    .OfCategoryId(IdCatDes).WhereElementIsElementType().ToElements() 

                ElementsbyCatsDes = []
                TypesDes = []
                i = 0
                for ele in self.ElementsbyCatDes:
                    ElementsbyCatsDes.append(ele.FamilyName)
                    ParametroTypeDes = ele.GetParameters("Type Name")
                    TypesDes.append(ParametroTypeDes[i].AsString())

                #print("Tipos")
                #Lista familias da categoria selecionada
                ElementsbyCatsDes = []
                for ele in self.ElementsbyCatDes: 
                    ElementsbyCatsDes.append(ele.FamilyName) 
                    #print(ele.FamilyName)

                #Popula familias de destino
                for type in TypesDes: #ElementsbyCatsDes:
                    self.comboBox_familiaDestino.addItem(type, type)
            
            #Se Instancias
            else: 
                #lista instancias da categoria
                self.ElementsbyCatDes = FilteredElementCollector(doc)\
                                    .OfCategoryId(IdCatDes).WhereElementIsNotElementType().ToElements()

                #print("instancia")
                #Seleciona instancias da categoria selecionada
                ElementsbyCatsDes = []
                for ele in self.ElementsbyCatDes:
                    ElementsbyCatsDes.append(ele.Name)
                    print(ele.Name)
                
                myset_Des = set(ElementsbyCatsDes)
                self.UniqueEleCats_Des = list(myset_Des)

                print(self.UniqueEleCats_Des)
                print(myset_Des)

                #Popula familias de destino
                for type in self.UniqueEleCats_Des:
                    self.comboBox_familiaDestino.addItem(type, type)

        #======================================================
        #Popula parametros origem e destino, se familias =
        # origem > familia de origem, destino > familia de origem
        def PopulateParameters():

            #ORIGEM
            #Pega ID da familia selecionada
            selectId = self.comboBox_FamiliaOrigem.currentIndex()
             
            self.selectEle = self.ElementsbyCat[selectId-1] 
            #self.Org = self.tipos[selectId-1]

            #Printa Parametros
            for par in self.selectEle.Parameters:
                print("=================")
                print(par.Definition.Name)
                print(par.AsValueString())
                print(par.AsInteger())
                print("=================")
            
            #Lista todos os parametros da familia
            self.allParam = []
            for par in self.selectEle.Parameters:   #self.RVTElementsbyCat[0].Parameters:
	            self.allParam.append(par.Definition.Name)
                
            #Se mesma familia
            if self.checkBox_mesmaFamilia.checkState():
                for type in self.allParam:
                    self.comboBox_parametroOrigem.addItem(type, type)

                for i in self.allParam:
                    self.comboBox_parametroDestino_2.addItem(i, i)
                
                #print(self.allParam)

            #Se familias diferentes
            # else:
            #     print("selecione familia 2")
            
        #======================================================
        #Popula parameros origem e destino, se familias !=
        # origem > familia de origem, destino > familia de destino
        def PopulateParametersFamila2():

                selectIdDes = self.comboBox_familiaDestino.currentIndex()
                self.selectEleDes = self.ElementsbyCatDes[selectIdDes-1] #par_categorias[selectIdDes-1]
                #Pega Id da categoria
                IdDes = self.selectEleDes.Id
                #print(IdDes)

                #Seleciona parametros da familia selecionada
                self.allParam2 = []
                for par2 in self.selectEleDes.Parameters: #self.RVTElementsbyCatDes[0].Parameters:
                    self.allParam2.append(par2.Definition.Name)
                

                #Popula parametros Origem
                for type in self.allParam:
                    self.comboBox_parametroOrigem.addItem(type, type)
                
                #print("parametros origem:", self.allParam)

                #Popula parametros Destino
                for j in self.allParam2:
                    self.comboBox_parametroDestino_2.addItem(j, j)
                
                #print("parametros destino:", self.allParam2)
        
        
        #======================================================
        #ABA CRIACAO DE VALORES
        #Popula combobox com os tipos de acordo com a categoria
        def PopulateTypes2():
            #ORIGEM
            SelectCategoria2 = self.comboBox_categoriaOrigem2.currentIndex()
            self.Categoria2 = par_categorias[SelectCategoria2-1]

            IdCat2 = self.Categoria2.Id
            #print(IdCat2)
            
            #Familia instanciada ou tipos
            #Adicionar checkinbox
            #if not self.checkBox_familiaInstancia_2.checkState():

                #lista elementos da categoria
                #Tipos
            #     self.ElementsbyCat2 = FilteredElementCollector(doc)\
            #                         .OfCategoryId(IdCat2).WhereElementIsElementType().ToElements()
              
            #     i = 0
            #     ElementsbyCats2 = []
            #     for ele in self.ElementsbyCat2:
            #         ElementsbyCats2.append(ele.FamilyName)
            #         print(ele.FamilyName)
            #         print(ele.GetType())
            #         # OBS: dois tipos de familia, familia carregada/familysymbol e familia do modelo/familytype
            #         # familysymbol: familia = nome do elemento; familytype: family = parede basica, parede cortina e type = tijolos, ceramica...  
            #         i = i + 1
            
            #     for type in ElementsbyCats2:
            #         self.comboBox_FamiliaOrigem2.addItem(type, type)
                    
                
            # else:
                #Instancias
            self.ElementsbyCat2 = FilteredElementCollector(doc)\
                                .OfCategoryId(IdCat2).WhereElementIsNotElementType().ToElements()

            #Seleciona instancias
            ElementsbyCats2 = []
            for ele in self.ElementsbyCat2:
                ElementsbyCats2.append(ele.Name)
                #print(ele.Name)
        
            for type in ElementsbyCats2:
                self.comboBox_familiaOrigem2.addItem(type, type)

        #======================================================
        #ABA CRIAÇÃO DE VALORES
        #Popula combobox com os parametros de acordo com o tipo
        def PopulateParameters2():

            selectIdcat = self.comboBox_familiaOrigem2.currentIndex()
            self.selectCat2 = par_categorias[selectIdcat-1]
            #Pega Id da categoria
            Idcat = self.selectCat2.Id
            #print(Idcat)
            
            #lista todos elementos da categoria
            self.RVTElementsbyCat2 = FilteredElementCollector(doc)\
                                 .OfCategoryId(Idcat).ToElements().WhereElementIsNotElementType().ToElements()
            #print(self.RVTElementsbyCat2[0])

            allParam3 = []
            for par in self.RVTElementsbyCat2[0].Parameters:
	            allParam3.append(par.Definition.Name)
            
            for type in allParam3:
                self.comboBox_parametroOrigem2.addItem(type, type)

        #======================================================
        #Zera abela
        def ClearRows():
            while self.tableWidget_tabela.rowCount() > 0:
                self.tableWidget_tabela.removeRow(0)

        #======================================================
        #Preenche tabela
        def Row():
            
            #Limpa tabela
            ClearRows()

            #print(self.selectEle)
            #FamilyInstance or Celling, Floor...
            if self.selectEle == "FamilyInstance":
                print("instancia")

            # if len(self.selectEle) > 0:
            #     print("teste")
            # else:
            #     x = 0
            #     for e in self.selectEle:
            #         #if x < len(self.selectEle):
            #         #    i = self.selectEle[x]
            #         #else: x = -1
            #         rowPosition = self.tableWidget_tabela.rowCount()
            #         #print(rowPosition)
            #         self.tableWidget_tabela.insertRow(rowPosition) 
            #         self.tableWidget_tabela.setItem(rowPosition , 0, QTableWidgetItem(str(e)))
            #         self.tableWidget_tabela.setItem(rowPosition , 1, QTableWidgetItem(e))
            #         self.tableWidget_tabela.setItem(rowPosition , 2, QTableWidgetItem(e))
            #         self.tableWidget_tabela.setItem(rowPosition , 3, QTableWidgetItem("teste VZ"))
            #         x = x + 1

         #set se tipe(mesmo e !=), set se instancia (mesma e !=)   
        
        #======================================================
        #Seta valores

        def Set(): 
            ok = input("Tem certeza que deseja setar os parametros? digite ok se é isso mesmo que deseja, caso contrario, feche a janela")
            substring = "ok"

            if substring in ok or "OK":
                #print(ok)

                selectId = self.comboBox_familiaDestino.currentIndex()
                self.selectEleIns = self.UniqueEleCats_Des[selectId-1] 
                print(self.selectEleIns, "ins des")

                selectId2 = self.comboBox_FamiliaOrigem.currentIndex()
                self.selectEleIns_Des = self.UniqueEleCats[selectId2-1] 
                print(self.selectEleIns_Des, "ins org")

                #Inicia Edicao
                TransactionManager.Instance.ForceCloseTransaction()
                s = Transaction(doc, "search")
                s.Start()

                #[[parametro origem]]
                ParametroOrigemId = self.comboBox_parametroOrigem.currentIndex()
                #ParametroOrigemId = self.comboBox_parametroOrigem.currentText()
                selectPar = self.allParam[ParametroOrigemId-1] #parametro selecionado
                strselectPar = selectPar #ParametroOrigemId #str(selectPar)
                
                #[[parametro destino]]
                ParametroDestinoId = self.comboBox_parametroDestino_2.currentIndex()
                selectParDes = self.allParam2[ParametroDestinoId-1] #parametro selecionado
                strselectParDes = selectParDes #str(selectParDes)

                #Lista todos os parametros
                NameSelect = self.selectEle.Parameters

                #SE TIPO
                if not (self.checkBox_familiaInstancia.checkState()):

                    for i in NameSelect:
                    #if i.HasValue:
                    #Guarda valor do parametro de origem
                        if str(i.Definition.Name) == str(strselectPar):
                            #print("achou equivalencia")
                            print(str(i.Definition.Name))

                            # ????????????????????????????????????????????
                            #Como adivinhar o tipo do parametro selecionado?
                            #Criar input para  o usuario escolher se o tipodo parametro é texto ou numero?
                            #??????????????????????????????????????????????

                            #Não muda o valor se tipo de parametro e diferente (ex: int =! str)
                            if i.AsValueString() != None:
                                value = i.AsValueString()
                                print(i.AsValueString())
                                print("1")
                            if i.AsString() != None:
                                value = i.AsString()
                                print(i.AsString())
                                print("2")
                            elif i.AsInteger() != None:
                                value = i.AsInteger()
                                print(i.AsInteger())
                                print("3")
                                print(i.AsString())
                                print(i.AsValueString())
                                print("Verifique se o parametro de origem possui um valor aplicado")
                            
                            print("valor do parametro", value)

                    #Printa tipo
                    #print("é tipo", self.selectEle)

                    #Lista todos os parametros
                    NameSelect = self.selectEle.Parameters
                
                    #---------------------PARA TESTE-------------------------
                    
                    #print("printa parametros elementos origem")
                    for i in NameSelect:
                        print(i.Definition.Name)

                    #print("printa todos os parametros do elemento selecionado")
                    #print(self.allParam)
                    for i in self.allParam:
                        print(i)

                    #---------------------------------------------------------
                    
                    #Percorre elementos da categoria
                    for ele in self.ElementsbyCat:

                        parametro = str(strselectPar)

                        #Seleciona parametro nome do tipo
                        typeName_ListElements = ele.GetParameters("Type Name")
                        typeName_element = self.selectEleDes.GetParameters("Type Name")

                        #Printa Valor / nome do tipo
                        #print("type element:",typeName_element[0].Definition.Name) 
                        #print("List:", typeName_ListElements[0].Definition.Name)
            
                        name = ele.GetParameters(parametro)
                        #print(name)

                        #Se o tipo atual for = ao tipo selecionado
                        if (typeName_element[0].AsString() == typeName_ListElements[0].AsString()):
                            #print(typeName_ListElements[0].AsString()) 
                            #print(typeName_element[0].AsString()) 
                            #name.Set(value)
                            #print(value)
                            #seta2 = self.selectEleDes.GetParameter(parametro)
                            seta = self.selectEleDes.LookupParameter(parametro)
                            #print(seta.Definition.Name)
                            #print(seta.Definition.ParameterType, "<< type")
                            #print(seta.Definition.GetType)
                            seta.Set(value)
                            #print(seta.AsString())
                            

                #SE INSTANCIA    #PAROU AQUI ============================================================================================
                if self.checkBox_familiaInstancia.checkState():

                    #Loop com a lista de todos os parametros do elemento de origem (selectEle.Parameters)
                    for i in NameSelect:
                           
                        # Se o nome do parametro i = nome do parametro selecionado
                        if str(i.Definition.Name) == str(strselectPar):
                            # parameterOrg = str(i.Definition.Name)
                            # value = self.selectEle.LookupParameter(parameterOrg)

                            #Loop para encontrar valor do parametro
                            for ele in self.ElementsbyCat: #self.ElementsbyCatDes:
                                #Tipo dos elemetos
                                typeName_ListElements = ele.GetParameters("Type Name")
                                typeName_element = self.selectEleDes.GetParameters("Type Name")
                                #Se o tipo selecionado for igual ao corrente (no for) guarda o valor
                                if (typeName_element[0].AsString() == typeName_ListElements[0].AsString()):
                                    temValor = ele.LookupParameter(str(strselectPar))
                                    print(temValor.HasValue)
                                    print(temValor.AsValueString())
                                    #para garantir que o parametro possui valor
                                    if temValor.HasValue and temValor.AsString != "None":  
                                        #guarda valor contido no parametro de origem selecionado pelo usuario                                    
                                        valor = temValor.AsString()
                                        # if valor == "s":
                                        #     break
                                        if valor != "" or valor != None or valor != 0:
                                             print("achou valor", valor)
                                             break
                                            
                            
                            # ????????????? 
                            # Como adivinhar o tipo do parametro selecionado?
                            # Criar input para  o usuario escolher se o tipodo parametro é texto ou numero?
                            # Não muda o valor se tipo de parametro e diferente (ex: int =! str)
                            # ?????????????

                            '''
                            MELHORIA: PARA FUNCIONAR COM PARAMETROS DE OUTROS TIPOS Q N STRING
                            # Se o conteudo do parametro i != 0 ou " " 
                            if i.Definition.Name != 0 or i.Definition.Name != " ":
                                #variavel value recebe conteudo do parametro
                                value = valor.AsString()
                            else:
                                #variavel value recebe conteudo do parametro e printa msg de aviso
                                value = i.Definition.Name
                                print("Verifique se o parametro de origem possui um valor aplicado")
                            # ------------------ PARA TESTE -----------------------

                            if i.AsValueString() != None:
                                value = valor.AsValueString()
                                print(i.AsValueString())
                                print("1")
                            if i.AsString() != None:
                                value = valor.AsString()
                                print(i.AsString())
                                print("2")
                            elif i.AsInteger() != None:
                                value = valor.AsInteger()
                                print(i.AsInteger())
                                print("3")
                                print(i.AsString())
                                print(i.AsValueString())
                                print("Verifique se o parametro de origem possui um valor aplicado")
                            
                            print("value:", value)
                            # -------------------------------------------------------
                            '''
                    
                    
                    #Percorre todos as familias da categoria selecionada
                    for ele in self.ElementsbyCat:

                        #Se mesma familia
                        if self.checkBox_mesmaFamilia.checkState():
                            #Elemento de destino = elemento de origem 

                            if ele.Name == self.selectEle: #se o elemento da categoria atual foi = ao selecionado

                                #Percorre elementos da categoria de destino
                                for i in self.ElementsbyCatDes:

                                    if i.Name == self.selectEleDes:

                                        #se o nome do elemento da lista for o elemento de destino
                                        if name == eleDes: #self.selectEle.Name:
                                            
                                            seta = self.selectEleDes.LookupParameter(str(selectParDes))
                                            seta.Set(valor)
                                            print(seta.AsString())

                        #Se familias diferentes
                        else:
                            
                            print("--------------------")
                            print(ele.Name, ": ele.Name")
                            print("--------------------")
                            # typeName_element = self.selectEle.LookupParameter("Type Name") #Tipo selecionado
                            # typeName_ele = ele.GetParameters("Type Name")

                            # print(typeName_ele.AsString(), "<< as string 1")
                            # print(typeName_ele.AsValueString(), "<< as string")

                            # self.selectEleIns_Des
                            # self.selectEleIns

                            if ele.Name == self.selectEleIns: #se o elemento da categoria atual foi = ao selecionado
                                parametro = str(strselectPar) # Parametro origem selecionado
                                
                                #Percorre elementos da categoria de destino
                                for i in self.ElementsbyCatDes:

                                    currentType = i.GetParameters("Type Name")

                                    if i.Name == self.selectEleIns_Des:
                                            
                                        seta = self.selectEleDes.LookupParameter(str(selectParDes))
                                        seta.Set(valor)
                                        print("seta 1")
                                        print(seta.AsString())
                                    

                                        #Se o tipo atual (for) = ao tipo selecionado
                                        if (typeName_element[0].AsString() == currentType[0].AsString()):

                                            seta = i.LookupParameter(str(selectParDes))
                                            seta.Set(valor)
                                            print("seta 2")
                                            print(seta.AsString())

                                    #Elemento de destino != elemento de origem
                                    #eleDes = self.selectEleDes.LookupParameter("Type Name")

                                    #nome do elemento de origem
                                    # name = ele.Name
                                    # print("familias", name, eleDes.Name, NameSelect)
                                
                                eleDes = self.selectEleDes.LookupParameter("Type Name")
                                name = ele.Name

                                #Se o nome do tipo corrente no for = nome do tipo selecionado
                                if name == eleDes:

                                    for i in self.ElementsbyCatDes:
                                        print(i.Name, eleDes.Name)

                                        #Se familia selecionada pelo usuario for = a familia corrente no laco
                                        if eleDes.Name == i.Name:
                                            print(name)
                                            print("e instancia")
                                        
                                            parametro = str(strselectPar)
                                            seta = ele.LookupParameter(parametro)
                                            print("paametro elecionado", seta)
                                            print(seta)
                                            print(value)
                                            
                                            # print(selecionaPar) 
                                            # getValor = selecionaParOrg.AsString()
                                            selecionaPar = self.selectEleDes.LookupParameter(strselectParDes)
                                            print(selecionaPar)
                                            selecionaPar.Set(value)
                                            print(seta.AsString())
                        
                #Finaliza edicao
                s.Commit()
                s.Dispose()
                #seta valores
                #get value in parameter origem selecionado  e set value parameter destino
            else:
                print("Feche as janelas")

        #==========================================================
        #SINAIS
        # > ComboBox
        self.comboBox_categoriaOrigem.currentIndexChanged.connect(PopulateTypes)
        self.comboBox_FamiliaOrigem.currentIndexChanged.connect(PopulateParameters)
        self.comboBox_familiaDestino.currentIndexChanged.connect(PopulateParametersFamila2)
        #self.comboBox_categoriaDestino.currentIndexChanged.connect(PopulateTypesDestino)
        self.comboBox_categoriaOrigem2.currentIndexChanged.connect(PopulateTypes2)
        self.comboBox_parametroDestino_2.currentIndexChanged.connect(Row)
        #self.comboBox_familiaDestino.currentIndexChanged.connect(PopulateTypesDestino)
        #self.comboBox_familiaOrigem2.currentIndexChanged.connect(PopulateParameters2)

        # > CheckBox
        self.checkBox_mesmaCategoria.stateChanged.connect(ActivateCatDestino)
        self.checkBox_mesmaFamilia.stateChanged.connect(ActivateTypesDestino)

        # > OK
        self.pushButton_ok.clicked.connect(Set)

if __name__=="__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
        ui = MainWindow()
        ui.show()
        #main()
        app.exec_()
#<<<END

