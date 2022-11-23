# coding=utf-8
# !/usr/bin/python

import clr
import sys
import System
from System.Collections.Generic import List

# Dev path
assembly_path = r"C:\Program Files\Autodesk\Revit 2021"
sys.path.append(assembly_path)

pyt27_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt27_path)

pyt26_path = r'C:\Program Files (x86)\IronPython 2.6\Lib'
sys.path.append(pyt27_path)

# Dynamo Nodes
clr.AddReference("RevitNodes")
import Revit

try:
    clr.ImportExtensions(Revit)
    clr.ImportExtensions(Revit.Elements)
    clr.ImportExtensions(Revit.GeometryConversion)
except:
    pass

# RevitAPI
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

try:
    # ExcelAPI
    clr.AddReference('Microsoft.Office.Interop.Excel')
    import Microsoft.Office.Interop.Excel as Excel
except:
    pass

BASEttb = {'ABNT (420x297mm)': [27.7, 21],
           'ABNT (580x297mm)': [27.7, 37],
           'ABNT (580x420mm)': [40, 37],
           'ABNT (580x594mm)': [57.4, 37],
           'ABNT (580x841mm)': [82.1, 37],
           'ABNT (841x297mm)': [27.7, 63.1],
           'ABNT (841x420mm)': [40, 63.1],
           'ABNT (841x594mm)': [57.4, 63.1],
           'ABNT (841x841mm)': [82.1, 63.1],
           'ABNT (1189x297mm)': [27.7, 97.9],
           'ABNT (1189x420mm)': [40, 97.9],
           'ABNT (1189x594mm)': [57.4, 97.9],
           'ABNT (1189x841mm)': [82.1, 97.9],
           'SIDE BOTTOM (420x297mm)': [25.3, 38.5],
           'SIDE RIGHT (420x297mm)': [27.7, 21]
           }


def IsAlmostEqual(one, two, tolerance=0.1):
    dif = abs(one - two)
    if dif > tolerance:
        return False
    else:
        return True


def ElementGetRoom(element, doc):
    """
    :param element: Elemento cuja room precisa ser encontrada
    :param doc: Documento em que o elemento se encontra
    :return: Elemento que representa a room
    """

    output = None
    rooms = []
    docs = [doc]
    roomcat = Autodesk.Revit.DB.BuiltInCategory.OST_Rooms
    links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

    for lnk in links:
        if lnk.GetLinkDocument() not in docs:
            docs.append(lnk.GetLinkDocument())
    for docu in docs:
        colrooms = FilteredElementCollector(docu).OfCategory(roomcat).ToElements()
        for room in colrooms:
            rooms.append(room)

    elebb = element.BoundingBox.ToRevitType()
    elept = (elebb.Max + elebb.Min) / 2

    for room in rooms:
        if room.IsPointInRoom(elept):
            output = room

    return output


def ElementBuiltInCategory(ele):
    """
	:param ele: Elemento cuja categoria sera retornada
	:return: Categoria interna do revit
	"""
    catname = ele.Category.Name
    bic = System.Enum.GetValues(BuiltInCategory)
    for i in bic:
        catname = catname.replace(" ", "")
        if str(i) == "OST_" + catname or str(i) == "OST_" + catname[:-1]:
            return i


def ElementGetDocElevation(element, doc):
    """
    :param doc:Documento onde os elementos da lista se encontram
    :param element: Elemento cujo level é retornado
    :return: Level
    """
    docelevations = list()
    elementlv = 0
    collector = FilteredElementCollector(doc).OfClass(Level).ToElements()
    for ele in collector:
        docelevations.append(ele.Elevation)
    try:
        elementlv = doc.GetElement(element.LevelId).Elevation
    except:
        elebb = element.get_BoundingBox(None)
        elementlv = elebb.Min.Z
    finally:
        closestlvl = min(docelevations, key=lambda x: abs(x - elementlv))
        output = collector[docelevations.index(closestlvl)]
    return output


def ElevationGetNexLevel(lvl, doc):
    """

    :param lvl: Elevation que será utilziada de referência
    :param doc: Documento onde serão procurados os levels
    :return: Próximo level
    """

    def GetElevation(level):
        return level.Elevation

    docelevations = list()
    myelevation = lvl.Elevation
    collector = ToList(FilteredElementCollector(doc).OfClass(Level).ToElements())

    for l in collector:
        docelevations.append(l.Elevation)

    docelevations.sort()
    collector.sort(key=GetElevation)

    if myelevation in docelevations:
        lvlind = docelevations.index(myelevation)
        if lvlind != docelevations.index(docelevations[-1]):
            return collector[lvlind + 1]
        else:
            return collector[lvlind]
    else:
        return None


def ElementGetFace(ele):
    """
    :param ele: Elemento cuja face será retornada
    :obs: A face retornada será a face que interessa para a análise de intersecções
    """
    
    out_inst = []
    out_symb = []


    # Instancegeometry e symbolgeomery são salvas nessas listas na mesma ordem
    inst_faces = list()
    inst_faces = None
    symb_faces = list()
    symb_faces = None

    geoOPT = Options()
    geoOPT.DetailLevel = ViewDetailLevel.Coarse
    geoOPT.ComputeReferences = True
    geoOPT.IncludeNonVisibleObjects = True

    eleCAT = ele.Category.Name

    curAREA = 0

    maxDOT = 1
    minDOT = 0
    testeLEN = 0

    if eleCAT == "Floors":
        maxDOT = 0
        minDOT = 1

    ele_geo = ToList(ele.get_Geometry(geoOPT).GetEnumerator())

    # Encontra a representação solida mais completa do elemento
    for geo in ele_geo:
        if geo.GetType() == Autodesk.Revit.DB.Solid:
            geo_faces = geo.Faces
            if geo_faces.Size > testeLEN:
                testeLEN = geo_faces.Size
                inst_faces = ToList(geo_faces)
                symb_faces = ToList(geo_faces)
                ele_face = inst_faces[0]   
        # Se for geometryinstance, tem que utilzar a face do symbol geometry, mas analisar interseccoes no instancegeometry
        elif geo.GetType() == Autodesk.Revit.DB.GeometryInstance:
            geo_instance = geo.GetInstanceGeometry()
            for ele in geo_instance:
                if ele.GetType() == Autodesk.Revit.DB.Solid:
                    geo_faces = ele.Faces
                    if geo_faces.Size > testeLEN:
                        testeLEN = geo_faces.Size
                        inst_faces = ToList(geo_faces)
                        ele_face = inst_faces[0]
            testeLEN = 0
            geo_symbol = geo.GetSymbolGeometry().GetEnumerator()
            for ele in geo_symbol:
                if ele.GetType() == Autodesk.Revit.DB.Solid:
                    geo_faces = ele.Faces
                    if geo_faces.Size > testeLEN:
                        testeLEN = geo_faces.Size
                        symb_faces = ToList(geo_faces)
    
    out_inst.append(ele_face)
    out_symb.append(symb_faces[inst_faces.index(ele_face)])

    # Filtra face com maior area e com a orientação correta
    for i, fc in enumerate(inst_faces):
        try:
            fcNRM = fc.FaceNormal.Normalize()
        except:
            continue
        fcAREA = fc.Area
        up = XYZ().BasisZ
        prod = up.DotProduct(fcNRM)
        if maxDOT > prod >= minDOT or minDOT > prod > -maxDOT:
            if fcAREA > curAREA:
                out_inst[0] = fc
                out_symb[0] = symb_faces[i]
                curAREA = fcAREA

    # Analisa faces restantes e remove faces redundantes
    for i, ofc in enumerate(inst_faces):
        for fc in out_inst:
            try:
                fcNRM = fc.FaceNormal
                ofcNRM = ofc.FaceNormal
            except:
                continue
            if ofcNRM.IsAlmostEqualTo(fcNRM) and ofc.Area != fc.Area:
                out_inst.append(ofc)
                out_symb.append(symb_faces[i])

    return out_inst, out_symb


def FittingsGetLines(inst):
    """
    :param inst: Instância do pipe fitting
    :return: Center lines da instância
    """
    output = list()

    opt = Options()
    opt.DetailLevel = ViewDetailLevel.Coarse
    enumGEO = inst.get_Geometry(opt).GetEnumerator()
    eleGEO = [i.GetInstanceGeometry() for i in enumGEO][0]
    for geo in eleGEO:
        tp = geo.GetType()
        if tp == Line or tp == Arc:
            output.append(geo)

    return output


def FittingsGetDiameter(ppf):
    conex = ppf.MEPModel.ConnectorManager.Connectors
    for c in conex:
        output = c.Radius * 2

    return output


def FamilyGetAllParameters(fam, doc):
    """
    :param fam: Familia cujos parâmetros serão lidos
    :param doc: Documento em que as instancias da familia serão procuradas
    """
    listpar = []
    parnames = []

    output = []

    collectedINST = []
    collectedPAR = []

    col = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()

    for inst in col:
        instFAM = inst.Symbol.Family
        if instFAM.Name == fam.Name and instFAM.Name not in collectedINST:
            famPAR = fam.Parameters
            typePAR = inst.Symbol.Parameters
            instPAR = inst.Parameters
            for par in famPAR:
                listpar.append(par)
            for par in typePAR:
                listpar.append(par)
            for par in instPAR:
                listpar.append(par)
            collectedINST.append(instFAM.Name)

    for par in listpar:
        parnames.append(par.Definition.Name)
    parnames.sort()

    for nome in parnames:
        for par in listpar:
            parNAME = par.Definition.Name
            if parNAME == nome and parNAME not in collectedPAR:
                output.append(par)
                collectedPAR.append(parNAME)

    return output


def ViewPlanByRoom(room, vpfamilytype, offset, doc):
    """
    :param offset: Offset da cropbox em relação à room
    :param room: Elemento room base de criação para a vista
    :param vpfamilytype: Family Type da view
    :param doc: Documento do projeto
    :return: Nova vista de planta baixa
    """
    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    ofs = UnitUtils.ConvertToInternalUnits(offset, uiunit)

    level = ElementGetDocElevation(room, doc)
    roombb = room.BoundingBox.ToRevitType()
    viewtypeid = ElementId(vpfamilytype.Id)

    newview = ViewPlan.Create(doc, viewtypeid, level.Id)

    bbmax = roombb.Max
    bbmin = roombb.Min

    newbb = BoundingBoxXYZ()
    newbb.Max = XYZ(bbmax.X + ofs, bbmax.Y + ofs, bbmax.Z)
    newbb.Min = XYZ(bbmin.X - ofs, bbmin.Y - ofs, bbmin.Z)

    newview.CropBoxActive = True
    newview.CropBox = newbb

    return newview


def ViewPlanByRoomAndLevel(room, level, vpfamilytype, offset, doc):
    """
    :param level: Level base da vista criada
    :param offset: Offset da cropbox em relação à room
    :param room: Elemento room base de criação para a vista
    :param vpfamilytype: Family Type da view
    :param doc: Documento do projeto
    :return: Nova vista de planta baixa
    """
    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    ofs = UnitUtils.ConvertToInternalUnits(offset, uiunit)

    roombb = room.BoundingBox.ToRevitType()
    viewtypeid = ElementId(vpfamilytype.Id)
    levelid = ElementId(level.Id)

    newview = ViewPlan.Create(doc, viewtypeid, levelid)

    bbmax = roombb.Max
    bbmin = roombb.Min

    newbb = BoundingBoxXYZ()
    newbb.Max = XYZ(bbmax.X + ofs, bbmax.Y + ofs, bbmax.Z)
    newbb.Min = XYZ(bbmin.X - ofs, bbmin.Y - ofs, bbmin.Z)

    newview.CropBoxActive = True
    newview.CropBox = newbb

    return newview


def ViewPlanByWall(wall, viewft, off, doc):
    """
    :param wall: Parede referência
    :param doc: Documento em que as vistas serão criadas
    :param viewft: View Family Type utilizada na vista criada
    :return: Vista de planta baixa rotacionada e com cropview
    """
    bbpoints = []
    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits

    offset = UnitUtils.ConvertToInternalUnits(off, uiunit)
    viewTypeId = viewft.Id
    level = wall.LevelId

    try:
        wallview = ViewPlan.Create(doc, viewTypeId, level)
    except:
        level = ElementGetDocElevation(wall, doc)
        wallview = ViewPlan.Create(doc, viewTypeId, level.Id)

    wllcurve = wall.Location.Curve

    if isinstance(wllcurve, Arc):
        wllcurve = Line.CreateBound(wllcurve.GetEndPoint(0), wllcurve.GetEndPoint(1))

    wdir = wllcurve.Direction
    wdirUV = UV(wdir.X, wdir.Y)
    xdirUV = UV(1, 0)
    angtoview = wdirUV.AngleTo(xdirUV)
    center = 0.5 * (wllcurve.GetEndPoint(0) + wllcurve.GetEndPoint(1))

    # Cria uma curva alinhada com a vista
    rot = Transform.CreateRotationAtPoint(XYZ.BasisZ, angtoview, center)
    rotcurve = wllcurve.CreateTransformed(rot)
    newline1 = rotcurve.CreateOffset(offset, XYZ.BasisZ)
    newline2 = rotcurve.CreateOffset(-offset, XYZ.BasisZ)

    bbpoints.append(newline1.GetEndPoint(0))
    bbpoints.append(newline1.GetEndPoint(1))
    bbpoints.append(newline2.GetEndPoint(0))
    bbpoints.append(newline2.GetEndPoint(1))

    newcpbox = BoundingBoxByPoints(bbpoints)

    # Nova ViewCrop
    wallview.CropBoxActive = True
    try:
        wallview.CropBox = newcpbox
    except:
        pass

    ViewPlanRotate(wallview, 3.14159 - angtoview, doc)

    return wallview


def ViewPlanRotate(myview, ang, doc):
    """
    :param myview: Vista que será rotacionada
    :param doc: Documento em que a vista se encontra
    :param ang: Angulo para rotacionar
    :return: Vista rotacionada
    """

    def GetViewCropBoxElement(rotview, doc):
        """
        :param rotview: Vista cujo cropbox será procurado
        :param doc: Documento onde a vista se encontra
        :return: CropBox element
        """
        TransactionManager.Instance.ForceCloseTransaction()
        tGroup = TransactionGroup(doc, "Temp to find crop box element")
        tGroup.Start()
        trans1 = Transaction(doc, "Temp to find crop box element")
        trans1.Start()
        myview.CropBoxVisible = False
        trans1.Commit()

        shownElems = FilteredElementCollector(doc, rotview.Id).ToElementIds()

        trans1.Start()
        rotview.CropBoxVisible = True
        trans1.Commit()

        cropBoxElement = FilteredElementCollector(doc, rotview.Id).Excluding(shownElems).FirstElement()
        tGroup.RollBack()
        TransactionManager.Instance.EnsureInTransaction(doc)

        return cropBoxElement

    crop = GetViewCropBoxElement(myview, doc)
    bb = myview.CropBox
    center = 0.5 * (bb.Max + bb.Min)
    axis = Line.CreateBound(center, center + XYZ.BasisZ)

    # Rotaciona a vista
    ElementTransformUtils.RotateElement(doc, crop.Id, axis, ang)

    return myview


def CropViewGenerator(cat_list, myview, offset, doc):
    """

    :param cat_list: Lista contendo a categoria dos elementos que devem ser consideradas para gerar a crop view
    :param myview: Vista que sera recortada
    :param doc: Documento das vistas
    :return: Vista com a cropview definida
    """

    ele_bbs = []
    docs = [doc]
    elements = []
    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    offset = UnitUtils.ConvertToInternalUnits(offset, uiunit)

    floorplan_types = [ViewType.AreaPlan, ViewType.CeilingPlan, ViewType.FloorPlan, ViewType.EngineeringPlan]
    elevation_types = [ViewType.Elevation, ViewType.Section]

    typed_list = List[BuiltInCategory](cat_list)
    filter = ElementMulticategoryFilter(typed_list)

    rvt_links = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()

    for lnk in rvt_links:
        if lnk.GetLinkDocument() not in docs:
            docs.append(lnk.GetLinkDocument())

    for dc in docs:
        if dc == doc:
            col = FilteredElementCollector(dc, myview.Id).WherePasses(
                filter).WhereElementIsNotElementType().ToElements()
        else:
            col = FilteredElementCollector(dc).WherePasses(
                filter).WhereElementIsNotElementType().ToElements()
        for ele in col:
            elements.append(ele)

    for ele in elements:
        if ele.Document.IsLinked:
            ele_bb = ele.get_BoundingBox(myview)
            newbb = BoundingBoxXYZ()
            newbb.Max = ele_bb.Max
            newbb.Min = ele_bb.Min
            ele_bbs.append(newbb)
        else:
            ele_bbs.append(ele.get_BoundingBox(myview))

    bb = BoundingBoxByBoundingBoxes(ele_bbs)

    bb.Max += XYZ(offset, offset, offset)
    bb.Min -= XYZ(offset, offset, offset)

    myview.CropBoxActive = True

    # Aplica cropview
    if myview.ViewType in floorplan_types:
        myview.CropBox = bb
    elif myview.ViewType in elevation_types:
        # Cria um novo sistema de coordenadas baseado no sistema de coordenadas da vista
        t = Transform.Identity
        t.BasisX = myview.CropBox.Transform.BasisX
        t.BasisY = myview.CropBox.Transform.BasisY
        t.BasisZ = myview.CropBox.Transform.BasisZ

        bb.Transform = t

        bb_width = bb.Max.X - bb.Min.X
        bb_height = bb.Max.Z - bb.Min.Z
        bb_center = (bb.Max + bb.Min) / 2

        pt_one = XYZ(bb_width / 2 + t.Origin.X, -bb_height / 2 + bb_center.Z, 0)
        pt_two = XYZ(bb_width / 2 + t.Origin.X, bb_height / 2 + bb_center.Z, 0)
        pt_three = XYZ(-bb_width / 2 + t.Origin.X, bb_height / 2 + bb_center.Z, 0)
        pt_four = XYZ(-bb_width / 2 + t.Origin.X, -bb_height / 2 + bb_center.Z, 0)

        new_crop = CurveLoop()

        line_one = Line.CreateBound(pt_one, pt_two).CreateTransformed(bb.Transform)
        new_crop.Append(line_one)
        line_two = Line.CreateBound(pt_two, pt_three).CreateTransformed(bb.Transform)
        new_crop.Append(line_two)
        line_three = Line.CreateBound(pt_three, pt_four).CreateTransformed(bb.Transform)
        new_crop.Append(line_three)
        line_four = Line.CreateBound(pt_four, pt_one).CreateTransformed(bb.Transform)
        new_crop.Append(line_four)

        view_shapeman = myview.GetCropRegionShapeManager()
        view_shapeman.SetCropShape(new_crop)

    elif myview.ViewType == ViewType.ThreeD:
        myview.IsSectionBoxActive = True
        myview.SetSectionBox(bb)
        myview.CropBoxActive = True

        # Define a cropview da vista 3d
        new3Dcb = myview.CropBox
        CBtranform = new3Dcb.Transform
        CBinverse = CBtranform.Inverse
        CBnewmax = CBinverse.OfPoint(bb.Max)
        CBnewmin = CBinverse.OfPoint(bb.Min)
        CBheight = CBnewmax.Y - CBnewmin.Y
        CBwidth = CBnewmax.X - CBnewmin.X
        CBdif = abs(CBheight - CBwidth)

        # Mantém a proporção quadrada
        if CBheight > CBwidth:
            new3Dcb.Max = XYZ(CBnewmax.X + (CBdif / 2) + 0.5, CBnewmax.Y + 0.5, CBnewmax.Z)
            new3Dcb.Min = XYZ(CBnewmin.X - (CBdif / 2) - 0.5, CBnewmin.Y - 0.5, CBnewmin.Z)
        else:
            new3Dcb.Max = XYZ(CBnewmax.X, CBnewmax.Y + (CBdif / 2) + 0.5, CBnewmax.Z)
            new3Dcb.Min = XYZ(CBnewmin.X, CBnewmin.Y - (CBdif / 2) - 0.5, CBnewmin.Z)
        myview.CropBox = new3Dcb
    else:
        TaskDialog.Show("Atenção", "Erro ao criar cropview: Tipo de vista não suportado.")

    return myview


def ViewScheduleByElement(ele, params, filterpar, filterval, schWDT, doc):
    """
    :param ele: Elemento referência utilizado para criar a tabela
    :param params: Parâmetros utilizados na tabela
    :param filterpar: Parâmetro utilizado para filtrar
    :param filterval: Valor do parâmetro filtro
    :param schWDT: Largura total da tabela
    :param doc: Documento em que a tabela será craida
    :return: Schedule View
    """
    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    schWIDTH = UnitUtils.ConvertToInternalUnits(schWDT, uiunit)
    paramscount = len(params)

    try:
        eleCAT = ele.Family.FamilyCategory
    except:
        eleCAT = ele.Category

    # Cria schedule e aplica configurações padrões
    newschedule = ViewSchedule.CreateSchedule(doc, eleCAT.Id)
    schdef = newschedule.Definition
    schdef.IsItemized = False
    schdef.IncludeLinkedFiles = True

    # Insere parâmetros na tabela
    for par in params:
        try:
            newfield = schdef.AddField(par)
            nfNAME = newfield.GetName()
        except:
            continue
        if newfield.UnitType == UnitType.UT_Length:
            fieldWDT = UnitUtils.ConvertToInternalUnits(1.2, uiunit)
            newfield.SheetColumnWidth = fieldWDT
            schWIDTH -= fieldWDT
            paramscount -= 1
        elif nfNAME == "Type Mark" or nfNAME == "Count" or nfNAME == "Mark":
            fieldWDT = UnitUtils.ConvertToInternalUnits(0.7, uiunit)
            newfield.SheetColumnWidth = fieldWDT
            schWIDTH -= fieldWDT
            paramscount -= 1
        if par.GetName(doc) == filterpar.GetName(doc):
            filtertype = ScheduleFilterType.Equal
            filter = ScheduleFilter(newfield.FieldId, filtertype, filterval)
            schdef.AddFilter(filter)

    # Mantém o tamanho das colunas dividadas pelo tamanho total da schedule
    fieldCOUNT = schdef.GetFieldCount()
    for i in range(0, fieldCOUNT - 1):
        field = schdef.GetField(i)
        if field.GetName() != "Mark" and field.GetName() != "Type Mark" and field.GetName() != "Count" and field.UnitType != UnitType.UT_Length:
            fieldWDT = schWIDTH / paramscount
            field.SheetColumnWidth = fieldWDT

    return newschedule


def DSCurveToViewElevation(vft, vpt, refline, height, distref, off, doc, returnmark=False):
    """
    :param vft: View Family Type utilizada para criar as elevações
    :param vpt: Id da View Plan onde a Elevation Marker vai ser criada
    :param refline: Linha utilizada para criação da elevação
    :param height: Altura da cropview (em internal units)
    :param distref: Distância da elevação da linha de referência (em project units)
    :param off: Offset da cropview (em project units)
    :param doc: Documento em que a elevação vai ser criada
    :return: Nova elevação
    """

    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    offset = UnitUtils.ConvertToInternalUnits(off, uiunit)
    distref = UnitUtils.ConvertToInternalUnits(distref, uiunit)

    if isinstance(refline, Arc):
        refline = Line.CreateBound(refline.GetEndPoint(0), refline.GetEndPoint(1))
    # Offset da viewcrop no extend
    newsp = refline.GetEndPoint(0)
    newep = refline.GetEndPoint(1)
    newsp2 = XYZ(newsp.X, newsp.Y, newsp.Z + height)
    newep2 = XYZ(newep.X, newep.Y, newep.Z + height)

    # Formato da nova ViewCrop
    l1 = Line.CreateBound(newsp, newep)
    l2 = Line.CreateBound(newep, newep2)
    l3 = Line.CreateBound(newep2, newsp2)
    l4 = Line.CreateBound(newsp2, newsp)

    # Linha distante da referência e Base de giro
    elevationLIN = refline.CreateOffset(-distref, XYZ.BasisZ)
    elevationPT = (elevationLIN.GetEndPoint(0) + elevationLIN.GetEndPoint(1)) / 2
    elptRotate = XYZ(elevationPT.X, elevationPT.Y, elevationPT.Z + 1)
    ln = Line.CreateBound(elevationPT, elptRotate)

    # Cria elevação e marker
    eleMarker = ElevationMarker.CreateElevationMarker(doc, vft.Id, elevationPT, 25)
    newelev = eleMarker.CreateElevation(doc, vpt, 0)

    # Ângulo entre a elevção e a parede
    vdirx = newelev.ViewDirection.X
    vdiry = newelev.ViewDirection.Y
    wdir = refline.Direction

    vdirUV = UV(vdirx, vdiry)
    wdirUV = UV(wdir.X, wdir.Y)

    # Rotaciona a elevação
    ang = vdirUV.AngleTo(wdirUV) + 1.5707963268
    ElementTransformUtils.RotateElement(doc, eleMarker.Id, ln, ang)

    # Nova ViewCrop
    crmanager = newelev.GetCropRegionShapeManager()
    newloop = []
    newloop.Add(l1)
    newloop.Add(l2)
    newloop.Add(l3)
    newloop.Add(l4)
    try:
        cloop = CurveLoop.Create(newloop)
        cloopNRM = cloop.GetPlane().Normal
        cloopOFF = CurveLoop.CreateViaOffset(cloop, offset, cloopNRM)
        crmanager.SetCropShape(cloopOFF)
    except:
        pass

    if returnmark:
        return newelev, eleMarker
    else:
        return newelev


def DSCurveToViewSection(curve, vsfamilytype, offset, height, doc):
    """
    :param curve: Linha base para criação do corte
    :param vsfamilytype: View Section Family Type
    :param offset: Offset da crop view em relação à linha base
    :param height: Altura da cropview
    :param doc: Documento do projeto
    :return: View Section
    """
    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    ofs = UnitUtils.ConvertToInternalUnits(offset, uiunit)
    viewdepth = UnitUtils.ConvertToInternalUnits(300, uiunit)
    h = UnitUtils.ConvertToInternalUnits(height, uiunit)

    if isinstance(curve, Arc):
        curve = Line.CreateBound(curve.GetEndPoint(0), curve.GetEndPoint(1))

    sp = curve.GetEndPoint(0)
    ep = curve.GetEndPoint(1)
    v = ep - sp
    curvelen = curve.Length

    # BB da vista
    bbmin = XYZ(-curvelen / 2, sp.Z - ofs, -0.5 / 2)
    bbmax = XYZ(curvelen / 2, sp.Z + h + ofs, 0.5 / 2)

    midpoint = sp + 0.5 * v
    linedir = v.Normalize()
    up = XYZ.BasisZ
    viewdir = linedir.CrossProduct(up)

    t = Transform.Identity
    t.Origin = midpoint
    t.BasisX = linedir
    t.BasisY = up
    t.BasisZ = viewdir

    vsbb = BoundingBoxXYZ()
    vsbb.Transform = t
    vsbb.Min = bbmin
    vsbb.Max = bbmax

    try:
        vftid = ElementId(vsfamilytype.Id)
    except:
        vftid = vsfamilytype.Id

    section = ViewSection.CreateSection(doc, vftid, vsbb)
    sectionDEP = section.get_Parameter(BuiltInParameter.VIEWER_BOUND_OFFSET_FAR)
    sectionDEP.Set(viewdepth)


    # Aplica viewcrop correta

    # Offset da viewcrop no extend
    newsp2 = XYZ(sp.X, sp.Y, sp.Z + h)
    newep2 = XYZ(ep.X, ep.Y, ep.Z + h)

    # Formato da nova ViewCrop
    l1 = Line.CreateBound(sp, ep)
    l2 = Line.CreateBound(ep, newep2)
    l3 = Line.CreateBound(newep2, newsp2)
    l4 = Line.CreateBound(newsp2, sp)

    # Nova ViewCrop
    crmanager = section.GetCropRegionShapeManager()
    newloop = []
    newloop.Add(l1)
    newloop.Add(l2)
    newloop.Add(l3)
    newloop.Add(l4)

    try:
        cloop = CurveLoop.Create(newloop)
        cloopNRM = cloop.GetPlane().Normal
        cloopOFF = CurveLoop.CreateViaOffset(cloop, ofs, cloopNRM)
        crmanager.SetCropShape(cloopOFF)
    except:
        pass

    # Confere se o corte esta olhando para a linha de referencia (a origem do corte deve ser inversa ao primeiro ponto da curva)
    if section.Origin.DistanceTo(curve.GetEndPoint(0)) < section.Origin.DistanceTo(curve.GetEndPoint(1)):
        sec_list = List[ElementId]([section.Id])
        plane = Plane.CreateByNormalAndOrigin(section.ViewDirection, section.Origin)
        ElementTransformUtils.MirrorElements(doc, sec_list, plane, False)

    return section


def LineIntersectPoints(line, linelist, ignorez=False):
    """
    :param line: Linha principal
    :param linelist: Lista de linhas para analisar possíveis intersecções
    :param ignorez: Se true, ignora a diferença de altura das linhas
    :return: Pontos de intersecção
    """
    interpts = []
    useline = line
    # Cria StrongBox para receber os resultados da intersecção
    results = clr.Reference[IntersectionResultArray]()

    if ignorez:
        linesp = line.GetEndPoint(0)
        lineep = line.GetEndPoint(1)
        newsp = XYZ(linesp.X, linesp.Y, 0)
        newep = XYZ(lineep.X, lineep.Y, 0)
        useline = Line.CreateBound(newsp, newep)

    for l in linelist:
        usel = l
        if ignorez:
            lsp = l.GetEndPoint(0)
            lep = l.GetEndPoint(1)
            usel = Line.CreateBound(XYZ(lsp.X, lsp.Y, 0), XYZ(lep.X, lep.Y, 0))
        inters = useline.Intersect(usel, results)
        if inters == SetComparisonResult.Overlap:
            intpt = results.get_Item(0).XYZPoint
            interpts.append(intpt)

    return interpts


def LinesRemoveOverlap(list_line):
    """

    :param list_line: Lista de linhas a serem analizadas
    :return: Lista sem linhas sobrepostas
    """
    for l in list_line:
        templist = list_line[:]
        templist.remove(l)
        for i in range(0, len(templist)):
            l_sp = l.GetEndPoint(0)
            l_ep = l.GetEndPoint(1)
            other_sp = templist[i].GetEndPoint(0)
            other_ep = templist[i].GetEndPoint(1)

            if l_sp == other_sp and l_ep == other_ep or l_sp == other_ep and l_ep == other_sp:
                list_line.remove(l)

    return list_line


def ToList(array):
    """
    :param array: Array que será convertido
    :return: Lista em python
    """
    output = list()
    if not isinstance(array, str):
        for item in array:
            output.append(item)
    else:
        output = [array]
    return output


def PointToDoc(point, doc, prototype=False):
    """
    :param doc: Documento do arquivo em questão
    :param prototype: Define se o ponto será ou não convertido para um ponto do Dynamo
    :param point: Ponto criado a partir do método XYZ, mas com valores em unidades do documento
    :return: Ponto XYZ na mesma posição
    """

    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    x = UnitUtils.ConvertToInternalUnits(point.X, uiunit)
    y = UnitUtils.ConvertToInternalUnits(point.Y, uiunit)
    z = UnitUtils.ConvertToInternalUnits(point.Z, uiunit)
    newpt = XYZ(x, y, z)
    if prototype:
        newpt = newpt.ToPoint()
    return newpt


def RoundPointOnFaceLocation(mypt, face, doc):
    """
    :param mypt: Ponto na face cujas coordenadas serão arredondadas
    :param face: Face de referência
    :param doc: Documento do projeto
    """

    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits

    directions = ["U", "V"]
    newptDIR = []
    facePTS = []
    ptDIST = 100000

    faceBB = face.GetBoundingBox()
    bbMin = faceBB.Min
    facePTS.append(bbMin)
    bbMax = faceBB.Max
    facePTS.append(bbMax)
    bbMin_ = UV(bbMax.U, bbMin.V)
    facePTS.append(bbMin_)
    bbMax_ = UV(bbMin.U, bbMax.V)
    facePTS.append(bbMax_)

    # Extremidade mais próxima do ponto
    for facePT in facePTS:
        dist = facePT.DistanceTo(mypt)
        if dist < ptDIST:
            refPT = facePT
            ptDIST = dist

    for dir in directions:
        # Posição em U ou V do ponto que será convertido
        if dir == "U":
            myptDir = UnitUtils.ConvertFromInternalUnits(mypt.U, uiunit)
            refPTDir = UnitUtils.ConvertFromInternalUnits(refPT.U, uiunit)
        else:
            myptDir = UnitUtils.ConvertFromInternalUnits(mypt.V, uiunit)
            refPTDir = UnitUtils.ConvertFromInternalUnits(refPT.V, uiunit)

        # Distância do ponto principal do ponto de referência em U ou V
        dif = abs(refPTDir - myptDir)

        # Resto da distância
        restDif = round(dif % 1, 3)
        toMove = 1 - abs(restDif)

        # Se o ponto principal está acima do ponto referência
        if myptDir > refPTDir:
            if restDif > 0.49:
                newDir = myptDir + toMove
            elif restDif < 0.49:
                newDir = myptDir - restDif
            else:
                newDir = myptDir

        # Se o ponto principal está abaixo do ponto de referência
        else:
            if restDif > 0.49:
                newDir = myptDir - toMove
            elif restDif < 0.49:
                newDir = myptDir + restDif
            else:
                newDir = myptDir

        newptDIR.append(UnitUtils.ConvertToInternalUnits(newDir, uiunit))

    newPT = UV(newptDIR[0], newptDIR[1])

    return newPT, refPT


def GroupPointsByDistance(mypoints, dist):
    """
    :param points: Lista de pontos que será analisada
    :param dist: Distância máxima entre os pontos para serem agrupados
    :param doc: Documento do arquivo do projeto
    """
    points = mypoints[:]
    for pt in points:
        if not isinstance(pt, list):
            replace = False
            mindist = UnitUtils.ConvertToInternalUnits(dist, DisplayUnitType.DUT_CENTIMETERS)
            group = [pt]
            otherPTS = points[:]
            otherPTS.remove(otherPTS[points.index(pt)])
            for opt in otherPTS:
                if not isinstance(opt, list):
                    odist = pt.DistanceTo(opt)
                    if opt.X == pt.X and opt.Y == pt.Y and opt.Z== pt.Z:
                        points.remove(opt)
                        continue
                    if odist <= mindist:
                        replace = True
                        points.remove(opt)
                        group.append(opt)
                        mindist += odist
            if replace:
                points[points.index(pt)] = group

    return points


def TemporaryHideAnnotations(doc, view):
    refplanes = FilteredElementCollector(doc).OfClass(ReferencePlane).ToElementIds()
    col = List[ElementId](refplanes)
    rvtlinks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).ToElementIds()
    col2 = List[ElementId](rvtlinks)
    categories = doc.Settings.Categories
    levelCat = categories.get_Item(BuiltInCategory.OST_Levels)
    elevCat = categories.get_Item(BuiltInCategory.OST_ElevationMarks)
    elevSymCat = categories.get_Item(BuiltInCategory.OST_Elev)
    sectCat = categories.get_Item(BuiltInCategory.OST_Sections)
    gridCat = categories.get_Item(BuiltInCategory.OST_Grids)
    textCat = categories.get_Item(BuiltInCategory.OST_TextNotes)
    # Hide the categories
    view.HideCategoryTemporary(gridCat.Id)
    view.HideCategoryTemporary(elevCat.Id)
    view.HideCategoryTemporary(sectCat.Id)
    view.HideCategoryTemporary(levelCat.Id)
    view.HideCategoryTemporary(textCat.Id)
    view.HideCategoryTemporary(elevSymCat.Id)
    view.HideElementsTemporary(col)
    view.HideElementsTemporary(col2)

    return view


def SheetCreateByTemplate(sheetref, duplicviews, doc):
    """
    :param sheetref: Prancha utilizada como referência
    :param duplicviews: Vistas que serão duplicadas
    :param doc: Documento do arquivo
    :return: Nova prancha com vistas e tamanho igual à referência
    """
    ttb = FilteredElementCollector(doc, sheetref.Id).OfCategory(BuiltInCategory.OST_TitleBlocks).FirstElement()

    newsheet = ViewSheet.Create(doc, ttb.GetTypeId())

    for vw in duplicviews:
        if vw.Category.Name == "Viewports":
            pp = vw.GetBoxCenter()
            vwview = vw.ViewId
            newvw = Viewport.Create(doc, newsheet.Id, vwview, pp)
        elif vw.Category.Name == "Schedule Graphics":
            pp = vw.Point
            schview = vw.ScheduleId
            ScheduleSheetInstance.Create(doc, newsheet.Id, schview, pp)

    return newsheet


def SheetLimits(tt, doc, uselabel=False):
    """
    :param doc: Documento do arquivo em questão
    :param uselabel: Usa o espaço designado ao selo e tabelas
    :param tt: Type da Title Block utilizada
    :return:
    """
    bbox = []
    tti = Revit.Elements.FamilyInstance.ByFamilyType(tt)[0]
    ttwidth = tti.GetParameterValueByName("Sheet Width") - 2
    ttheight = tti.GetParameterValueByName("Sheet Height") - 2
    # BB direita
    bbdir = BoundingBoxXYZ()
    bbdir.Min = PointToDoc(XYZ(-18.5, 1, 0), doc)
    bbdir.Max = PointToDoc(XYZ(100, ttheight - 1, 10), doc)
    if uselabel:
        bbdir.Min = PointToDoc(XYZ(-1, 1, 0), doc)
    bbox.append(bbdir.ToProtoType())
    # BB superior
    bbsup = BoundingBoxXYZ()
    bbsup.Min = PointToDoc(XYZ(-ttwidth + 2.5, ttheight - 1, 0), doc)
    bbsup.Max = PointToDoc(XYZ(-1, ttheight + 100, 10), doc)
    bbox.append(bbsup.ToProtoType())
    # BB esquerda
    bbesq = BoundingBoxXYZ()
    bbesq.Min = PointToDoc(XYZ(-ttwidth + -100, 1, 0), doc)
    bbesq.Max = PointToDoc(XYZ(-ttwidth + 2.5, ttheight - 1, 10), doc)
    bbox.append(bbesq.ToProtoType())
    # BB inferior
    bbinf = BoundingBoxXYZ()
    bbinf.Min = PointToDoc(XYZ(-ttwidth + 2.5, -100, 0), doc)
    bbinf.Max = PointToDoc(XYZ(-1, 1, 10), doc)
    bbox.append(bbinf.ToProtoType())

    return bbox


def SheetDimensions(sheet, doc):
    """
    :param sheet: Vista da sheet
    :param doc: Documento do arquivo em questão
    :return: Largura e altura da sheet
    """

    sheetttb = FilteredElementCollector(doc, sheet.Id).OfCategory(BuiltInCategory.OST_TitleBlocks).FirstElement()
    sheewdt = sheetttb.LookupParameter('Sheet Width').AsDouble()
    sheethgt = sheetttb.LookupParameter('Sheet Height').AsDouble()

    return sheewdt, sheethgt


def ViewSheetGetOrigin(viewsheet, doc):
    ttb = FilteredElementCollector(doc, viewsheet.Id).OfCategory(
        BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().FirstElement()

    if ttb is not None:
        bb = ttb.get_BoundingBox(viewsheet)
        origin = XYZ(bb.Max.X, bb.Min.Y, 0)
        if IsAlmostEqual(origin.X, 1, 1) and IsAlmostEqual(origin.Y, -1, 1):
            origin -= origin
        return origin
    else:
        return XYZ(0, 0, 0)


def SheetLegendsSchedules(sheetview, doc):
    """
    :param sheetview: Vista da prancha que será analisada
    :param doc: Documento referente ao arquivo aberto
    """

    output = []
    catlist = [BuiltInCategory.OST_Viewports, BuiltInCategory.OST_ScheduleGraphics]
    icatlist = List[BuiltInCategory](catlist)
    filter = ElementMulticategoryFilter(icatlist)
    viewports = FilteredElementCollector(doc, sheetview.Id).WherePasses(filter).ToElements()

    for vp in viewports:
        if vp.Category.Name == "Viewports":
            vpview = doc.GetElement(vp.ViewId)
            if vpview.ViewType == ViewType.Legend:
                output.append(vp)
        else:
            output.append(vp)

    # Função para retornar o posição em y das tabelas
    def ViewportMaxPt(vps):
        maxpt = vps.get_BoundingBox(sheetview).Max.Y
        return maxpt

    # Organiza a lista conforme posição em y
    output.sort(key=ViewportMaxPt, reverse=True)
    output.remove(output[-1])

    return output


def ViewportOutline(vp, viewsheet=None):
    """
    :param vp: Viewport
    :param viewsheet: Sheet onde a viewport se encontra
    """

    if vp.Category.Name != "Viewports":
        margin = 0.2 / 30.48
        rowsize = 0.2 / 30.48
        viewbb = vp.get_BoundingBox(viewsheet)
        ptmax = viewbb.Max
        ptmin = viewbb.Min
    else:
        viewout = vp.GetBoxOutline()
        ptmax = viewout.MaximumPoint
        ptmin = viewout.MinimumPoint
        margin = 0.3 / 30.48
        rowsize = 0

    newmax = XYZ(ptmax.X - margin, ptmax.Y - margin + rowsize, 0)
    newmin = XYZ(ptmin.X + margin, ptmin.Y + margin, 0)

    newout = Outline(newmin, newmax)
    return newout


def SheetLSCheckIntersection(viewsheet, doc):
    """
    :param viewsheet: Prancha a ser analisada
    :param doc: Documento referente ao arquivo da prancha
    """

    viewsout = []
    sideslist = [-500]
    posdict = {}
    viewsvp = SheetLegendsSchedules(viewsheet, doc)
    space = 0.25 / 30.48

    # Desliga annotations temporariamente
    TransactionManager.Instance.ForceCloseTransaction()
    with Transaction(doc, "HideAnnotations") as tt:
        tt.Start()
        for i, vp in enumerate(viewsvp):
            if vp.Category.Name == "Viewports":
                vpview = doc.GetElement(vp.ViewId)
                TemporaryHideAnnotations(doc, vpview)
        tt.Commit()

    # Outline das views
    for vp in viewsvp:
        newout = ViewportOutline(vp, viewsheet)
        viewsout.append(newout)

    # Cria um dicionário organizado pela posição em x das tabelas
    for i in range(0, len(viewsout)):
        teste = False
        vppos = abs(round(viewsout[i].MinimumPoint.X, 2))
        poskey = str(vppos)
        for pos in sideslist:
            if IsAlmostEqual(vppos, pos):
                poskey = str(pos)
                teste = True
        if not teste:
            sideslist.append(vppos)
            posdict[poskey] = [viewsvp[i]]
        else:
            posdict[poskey].append(viewsvp[i])

    # Move as views para a posição correta
    with Transaction(doc, "MoveViewport") as ttv:
        ttv.Start()
        for k, v in posdict.items():
            for vp in v:
                vpout = ViewportOutline(vp, viewsheet)
                vpmax = vpout.MaximumPoint
                vpmin = vpout.MinimumPoint
                nextpos = XYZ(vpmax.X, vpmin.Y - space, 0)
                nextvp = v.index(vp) + 1
                if nextvp < len(v):
                    nextout = ViewportOutline(v[nextvp], viewsheet)
                    vect = nextpos - nextout.MaximumPoint
                    ElementTransformUtils.MoveElement(doc, v[nextvp].Id, vect)
        ttv.Commit()

    with Transaction(doc, "UnhideAnnotations") as ttu:
        ttu.Start()
        for vp in viewsvp:
            if vp.Category.Name == "Viewports":
                vpview = doc.GetElement(vp.ViewId)
                vpview.DisableTemporaryViewMode(TemporaryViewMode.TemporaryHideIsolate)
        ttu.Commit()

    return viewsheet


def SheetPossiblePlacementPoints(sheet, dist, doc):
    """

    :param sheet: Vista da prancha em que os possiveis pontos serao analisados
    :param dist: Distancia das proximas viewports para as existentes
    :param doc: Documento
    :return: Lista de pontos possiveis para onde inserir uma viewport
    """
    output = []
    vp_outlines = []
    vp_points = []

    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    dist = UnitUtils.ConvertToInternalUnits(dist, uiunit)
    sheet_vps = sheet.GetAllViewports()
    TransactionManager.Instance.ForceCloseTransaction()

    with Transaction(doc, "Annotations") as toff:
        for vp in sheet_vps:
            vp = doc.GetElement(vp)
            vp_view = doc.GetElement(vp.ViewId)
            if vp_view.ViewType != ViewType.Legend:
                # Desliga annotations para analisar tamanho da viewport
                toff.Start()
                TemporaryHideAnnotations(doc, vp_view)

                # Analisa o tamanho da viewport
                vp_outline = vp.GetBoxOutline()
                out_max = vp_outline.MaximumPoint - XYZ(0, 0, vp_outline.MaximumPoint.Z)
                out_min = vp_outline.MinimumPoint - XYZ(0, 0, vp_outline.MinimumPoint.Z)
                vp_outline = Outline(out_min, out_max)
                vp_outlines.append(vp_outline)

                # Guarda os possiveis pontos
                pt_right = out_max + XYZ(dist, 0, 0)
                pt_botton = out_min - XYZ(0, -dist, 0)
                vp_points.append(pt_right)
                vp_points.append(pt_botton)

                # Reativa annotations
                vp_view.DisableTemporaryViewMode(TemporaryViewMode.TemporaryHideIsolate)
                toff.Commit()

        # Testa insterseccao dos pontos
        for pt in vp_points:
            intersect = False
            for out in vp_outlines:
                if out.Contains(pt, 0.01):
                    intersect = True
                    break
            if not intersect:
                output.append(pt)

        if len(output) == 0:
            output = vp_points

    return output


def PlaceSchedulesInstances(lst, pp, sheet, doc):
    """
    :param lst: Lista de schedules a serem colocadas
    :param pp: Ponto de inserção da primeira schedule
    :param doc: Documento do arquivo em questão
    :param sheet: Folha onde as schedules serão inseridas
    :return: Lista das schedules instances
    """

    output = []
    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits

    for sched in lst:
        sch = ScheduleSheetInstance.Create(doc, sheet.Id, sched.Id, pp)
        output.append(sch)
        schbb = sch.get_BoundingBox(sheet)
        schmax = schbb.Max
        schmin = schbb.Min
        schheight = schmax.Y - schmin.Y
        dist = UnitUtils.ConvertToInternalUnits(0.3, uiunit)
        pp = XYZ(pp.X, pp.Y - schheight - dist, pp.Z)

    return output


def ViewportBoundingBox(viewport, prototype=False):
    """
    :param viewport: Viewport cuja boundingbox deseja obter
    :param prototype: Converte para boundingbox do dynamo
    :return: BoundingBox
    """

    viewsheet = viewport.Document.GetElement(viewport.OwnerViewId)
    viewout = ViewportOutline(viewport, viewsheet)

    minpt = viewout.MinimumPoint
    maxpt = viewout.MaximumPoint

    newmaxpt = XYZ(maxpt.X, maxpt.Y, 1)
    newminpt = XYZ(minpt.X, minpt.Y, 0)

    bb = BoundingBoxXYZ()
    bb.Max = newmaxpt
    bb.Min = newminpt

    if prototype:
        bb = bb.ToProtoType()

    return bb


def BoundingBoxByViewports(viewslist, doc=None):
    """
    :param viewslist: Lista de viewports
    :return: BoundingBox
    """

    maxX = []
    minX = []
    maxY = []
    minY = []
    maxpoints = []
    minpoints = []
    for ele in viewslist:
        if ele.Category.Name != "Viewports":
            margin = 0.2 / 30.48
            rowsize = 0.2 / 30.48
            try:
                viewbb = ele.get_BoundingBox(doc.GetElement(ele.OwnerViewId))
            except:
                continue
            ptmax = viewbb.Max
            ptmin = viewbb.Min
            newmax = XYZ(ptmax.X - margin, ptmax.Y - margin + rowsize, 1)
            newmin = XYZ(ptmin.X + margin, ptmin.Y + margin, 0)
        else:
            try:
                eleMinpt = ele.GetBoxOutline().MinimumPoint
                eleMaxpt = ele.GetBoxOutline().MaximumPoint
            except:
                continue
            newmax = XYZ(eleMaxpt.X, eleMaxpt.Y, 1)
            newmin = XYZ(eleMinpt.X, eleMinpt.Y, 0)
        maxpoints.append(newmax)
        minpoints.append(newmin)
    for maxpt in maxpoints:
        maxX.append(maxpt.X)
        maxY.append(maxpt.Y)
    for minpt in minpoints:
        minX.append(minpt.X)
        minY.append(minpt.Y)
    newBB = BoundingBoxXYZ()
    newBB.Min = XYZ(min(minX), min(minY), 0)
    newBB.Max = XYZ(max(maxX), max(maxY), 1)

    return newBB


def BoundingBoxByBoundingBoxes(bblist):
    """
    :param bblist: Lista de boundingbox
    :return: Uma boundingbox que representa o espaço ocupado pelo conjunto
    """

    maxX = []
    minX = []
    maxY = []
    minY = []
    maxZ = []
    minZ = []
    maxpoints = []
    minpoints = []
    for bb in bblist:
        try:
            bbRVT = bb.ToRevitType()
        except:
            bbRVT = bb
        minpt = bbRVT.Min
        maxpt = bbRVT.Max
        maxpoints.append(maxpt)
        minpoints.append(minpt)
    for maxpt in maxpoints:
        maxX.append(maxpt.X)
        maxY.append(maxpt.Y)
        maxZ.append(maxpt.Z)
    for minpt in minpoints:
        minX.append(minpt.X)
        minY.append(minpt.Y)
        minZ.append(minpt.Z)
    newBB = BoundingBoxXYZ()
    newBB.Min = XYZ(min(minX), min(minY), min(minZ))
    newBB.Max = XYZ(max(maxX), max(maxY), max(maxZ))

    return newBB


def BoundingBoxByElements(ele_list):
    """

    :param ele_list: Lista de elementos
    :return: Boundingbox respresentando todos elementos
    """
    ele_bbs = []
    if not isinstance(ele_list, list):
        ele_list = [ele_list]

    for ele in ele_list:
        ele_bb = ele.get_BoundingBox(None)
        if ele_bb is not None:
            ele_bbs.append(ele_bb)

    return BoundingBoxByBoundingBoxes(ele_bbs)


def BoundingBoxByPoints(pointlist):
    """
    :param pointlist: Lista de possíveis pontos
    :return: BoundingBox
    """
    maxX = pointlist[0].X
    maxY = pointlist[0].Y
    maxZ = pointlist[0].Z

    minX = pointlist[0].X
    minY = pointlist[0].Y
    minZ = pointlist[0].Z

    for pt in pointlist:
        if pt.X >= maxX and pt.Y >= maxY and pt.Z >= maxZ:
            mymax = pt
        if pt.X <= minX and pt.Y <= minY and pt.Z <= minZ:
            mymin = pt
    bb = BoundingBoxXYZ()
    bb.Min = mymin
    bb.Max = mymax

    return bb


def ViewportCheckIntersectionProportions(ptr, viewvp, intersectlist):
    """
    :param ptr: Ponto onde a view será inserida
    :param viewvp: Viewport
    :param intersectlist: Lista de boundingbox correspondente as outras viewports na mesma prancha
    :return: boolresult -> True se intersecciona com qualquer uma das outras viewports
    :return: prop -> Proporção (AxL) formada pelo layout da viewport com as outras
    """

    boollist = []
    views = []

    minpt = viewvp.GetBoxOutline().MinimumPoint
    maxpt = viewvp.GetBoxOutline().MaximumPoint
    viewH = maxpt.Y - minpt.Y
    viewW = maxpt.X - minpt.X

    # BB da view
    viewBB = BoundingBoxXYZ()
    viewBB.Min = XYZ(ptr.X, ptr.Y - viewH, 0)
    viewBB.Max = XYZ(ptr.X + viewW, ptr.Y, 1)
    viewBBDS = viewBB.ToProtoType()
    views.append(viewBBDS)
    # Teste de intersecção

    for bb in intersectlist:
        test = bb.Intersects(viewBBDS)
        boollist.append(test)
        views.append(bb)
    if True in boollist:
        boolresult = True
    else:
        boolresult = False

    # Área ocupada pelo conjunto de views naquela posição
    viewsBB = BoundingBoxByBoundingBoxes(views)

    # Cálculo da proporção
    b = viewsBB.Max.X - viewsBB.Min.X
    h = viewsBB.Max.Y - viewsBB.Min.Y
    prop = abs(b - h)

    return boolresult, prop


def ViewportMoveToPoint(ptr, view, centeraligned=False):
    """
    :param ptr: Ponto para onde a viewport será movida
    :param view: Viewport
    :param centeraligned: Se true, alinha com o centro da viewport. Do contrário, alinha com o canto sup esquerdo.
    :return: viewport
    """

    minpt = view.GetBoxOutline().MinimumPoint
    maxpt = view.GetBoxOutline().MaximumPoint

    viewHeight = maxpt.Y - minpt.Y
    viewWidth = maxpt.X - minpt.X

    # Nova posição
    if centeraligned:
        Npt = XYZ(ptr.X, ptr.Y - (viewHeight / 2), 0)
    else:
        Npt = XYZ(ptr.X + (viewWidth / 2), ptr.Y - (viewHeight / 2), 0)

    viewpos = view.SetBoxCenter(Npt)

    return viewpos


def ViewportNextPoints(viewVP, placementpoint, dist, doc):
    """
    :param doc: Documento do arquivo em questão
    :param dist: Distância entre as viewports
    :param viewVP: Viewport
    :param placementpoint: Posição do ponto onde ela foi inserida
    :return: Próximos possíveis pontos
    """

    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    dist = UnitUtils.ConvertToInternalUnits(dist, uiunit)

    # Dimensões e posição da view final
    minpt = viewVP.GetBoxOutline().MinimumPoint
    maxpt = viewVP.GetBoxOutline().MaximumPoint
    viewHeight = maxpt.Y - minpt.Y
    viewWidth = maxpt.X - minpt.X

    # Próximas posições e distancia entre viewports
    newpt1 = XYZ(placementpoint.X, placementpoint.Y - viewHeight - dist, 0)
    newpt2 = XYZ(placementpoint.X + viewWidth + dist, placementpoint.Y, 0)

    return newpt1, newpt2


def TTBlockDef(views, doc, hasschedule=False):
    """
    :param views: Lista de viewports na prancha
    :param doc: Documento do arquivo em questão
    :param hasschedule: True, se existe alguma tabela na prancha
    :return: Type da titleblock sugerida
    """

    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    ttbFamilies = []
    collector = FilteredElementCollector(doc).OfClass(Family).ToElements()

    ttb = {}
    areattb = {}
    tempdict = {}

    for family in collector:
        if "ANS title" in family.Name and "BLANK" not in family.Name and "APR" not in family.Name:
            ttbFamilies.append(family.Name)

    # Substitui as keys da BASEttb pelo nome das famílias de prancha do arquivo
    for i in ttbFamilies:
        for k, v in BASEttb.items():
            old = k.replace('(', "")
            oold = old.replace(')', "")
            if k in i or oold in i:
                ttb[i] = v

    # Remove o espaço das tabelas das pranchas menores
    if hasschedule:
        for k, v in ttb.items():
            if "297" in k and "SIDE" not in k:
                ttb[k][1] -= 18.5

    # Tamanho do conjunto de views
    viewsBB = BoundingBoxByViewports(views)
    viewsH = UnitUtils.ConvertFromInternalUnits(viewsBB.Max.Y - viewsBB.Min.Y, uiunit)
    viewsW = UnitUtils.ConvertFromInternalUnits(viewsBB.Max.X - viewsBB.Min.X, uiunit)

    # Possíveis ttb que poderiam ser usadas (cria um novo dicionário com a área delas)
    for k, v in ttb.items():
        areattb[k] = v[0] * v[1]
        if v[0] > viewsH and v[1] > viewsW:
            tempdict[k] = v[0] * v[1]

    # Escolhe o menor ttb possível
    if len(tempdict) == 0:
        ttbname = (str(max(areattb, key=areattb.get)))
    else:
        ttbname = (str(min(tempdict, key=tempdict.get)))

    for col in collector:
        if col.Name == ttbname:
            symbols = ToList(col.GetFamilySymbolIds())
            ttbfam = doc.GetElement(symbols[0])

    return ttbfam


def PointsTranslateFromSheets(oldWDT, oldHGT, sheet, points, doc):
    """
    :param oldWDT: Largura da antiga prancha
    :param oldHGT: Altura da antiga prancha
    :param sheet: Prancha que será alterada
    :param points: Lista de pontos a serem movidos
    :param doc: Documento do arquivo em questão
    :return:
    """

    output = []

    sheetttb = FilteredElementCollector(doc, sheet.Id).OfCategory(BuiltInCategory.OST_TitleBlocks).FirstElement()
    newWDT = sheetttb.LookupParameter('Sheet Width').AsDouble()
    newHGT = sheetttb.LookupParameter('Sheet Height').AsDouble()

    Xdif = oldWDT - newWDT
    Ydif = newHGT - oldHGT

    for pt in points:
        newpt = XYZ(pt.X + Xdif, pt.Y + Ydif, 0)
        output.append(newpt)

    return output


def SheetChangeSize(actualsheet, newsheetFAM, doc, legend_asview=True):
    """
    :param actualsheet: Prancha atual
    :param newsheetFAM: Família (titleblock) que será utilizada
    :param doc: Documento do arquivo em questão
    :param legend_asview: Caso true, considera as legends como viewports no meio da prancha
    :return: Mesma prancha com viewports e type alterados
    """

    uiunit = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
    viewslocation = []
    schWidth = UnitUtils.ConvertToInternalUnits(18.5, uiunit)

    # Views on sheet
    catlist = [BuiltInCategory.OST_ScheduleGraphics, BuiltInCategory.OST_Viewports]
    icatlist = List[BuiltInCategory](catlist)
    catfilter = ElementMulticategoryFilter(icatlist)
    sheetviews = FilteredElementCollector(doc, actualsheet.Id).WherePasses(catfilter).ToElements()

    # Actual ttb info
    sheetttb = FilteredElementCollector(doc, actualsheet.Id).OfCategory(BuiltInCategory.OST_TitleBlocks).FirstElement()
    actualWDT = sheetttb.LookupParameter('Sheet Width').AsDouble()
    actualHGT = sheetttb.LookupParameter('Sheet Height').AsDouble()
    oldttbName = sheetttb.Symbol.Family.Name
    newttbName = newsheetFAM.Family.Name

    # OLD Points
    for view in sheetviews:
        try:
            viewslocation.append(view.GetBoxCenter())
        except:
            viewslocation.append(view.Point)

    # Change ttb
    sheetttb.Symbol = newsheetFAM

    # New Points
    newpoints = PointsTranslateFromSheets(actualWDT, actualHGT, actualsheet, viewslocation, doc)

    # Vistas que devem ficar na area de schedules
    if legend_asview:
        CATleg = ["Schedule Graphics"]
    else:
        CATleg = ["Schedule Graphics", ViewType.Legend]

    if "SIDE" in newttbName or "297" not in newttbName:
        new = "Right"
    elif "SIDE" not in newttbName and "297" in newttbName:
        new = "Left"
    else:
        new = "Left"
    if "SIDE" in oldttbName or "297" not in oldttbName:
        old = "Right"
    elif "SIDE" not in oldttbName and "297" in oldttbName:
        old = "Left"
    else:
        old = "Right"

    # Move views
    for i, view in enumerate(sheetviews):
        try:
            viewCAT = view.Category.Name
        except:
            viewCAT = ""
        try:
            viewTP = doc.GetElement(view.ViewId).ViewType
        except:
            viewTP = ""
        # Analisa se a prancha atual já e menor em altura para reposicionar as schedules
        if viewCAT in CATleg or viewTP in CATleg:
            if old == "Right" and new == "Left":
                viewpos = XYZ(newpoints[i].X + schWidth, viewslocation[i].Y, 0)
            elif old == "Left" and new == "Right":
                viewpos = XYZ(newpoints[i].X - schWidth, viewslocation[i].Y, 0)
            else:
                viewpos = XYZ(newpoints[i].X, viewslocation[i].Y, 0)
        else:
            viewpos = XYZ(viewslocation[i].X, viewslocation[i].Y, 0)
        vector = newpoints[i].Subtract(viewpos)
        try:
            ElementTransformUtils.MoveElement(doc, view.Id, vector)
        except:
            pass

    return actualsheet


def ViewExportNWC(myview, options, path, filename, doc):
    """
    :param myview: vista que será exportada
    :param options: opcoes de exportacao em dicionario
    :param path: caminho da pasta onde serão salvos os arquivos
    :param filename: nome do arquivo exportado
    :param doc: documento do arquivo do projeto
    """

    opt = NavisworksExportOptions()
    opt.ExportLinks = options["ExportLinks"]
    opt.ExportRoomAsAttribute = options["ExportRoomAsAttribute"]
    opt.ExportRoomGeometry = options["ExportRoomGeometry"]
    opt.ConvertElementProperties = options["ConvertElementProperties"]
    opt.ConvertLights = options["ConvertLights"]
    opt.Coordinates = options["Coordinates"]

    opt.ExportScope = NavisworksExportScope.View
    opt.ViewId = myview
    newfile = doc.Export(path, filename, opt)

    return newfile


def GetWorksheetCellsRange(worksheet):
    """

    :param worksheet: Worksheet que será analisada
    :return: Última coluna e última linha
    """
    import string

    def GenerateExcelColumns():
        alpha = string.ascii_uppercase
        excelcol = []
        for l in alpha:
            excelcol.append(l)
        for l in alpha:
            for n in alpha:
                excelcol.append(l + n)
        return excelcol

    columns = GenerateExcelColumns()
    lastcol = "Z"
    lastlin = "10"

    null_ocurrence = 0
    index = 1  # B

    # Testa colunas
    while null_ocurrence < 2:
        col = worksheet.Range[columns[index] + "1"]
        if col.Value2 is not None:
            lastcol = columns[index]
        else:
            null_ocurrence += 1
        index += 1

    null_ocurrence = 0
    index = 2

    # Testa linhas
    while null_ocurrence < 2:
        lin = worksheet.Range("A" + str(index))
        if lin.Value2 is not None:
            lastlin = str(index)
        else:
            null_ocurrence += 1
        index += 1

    return lastcol, lastlin


def ParametersExportByCategory(eleDIC, paramDIC, savepath):
    """

    :param eleDIC: Dicionário contendo os elementos divididos por categoria, onde a key é a acategoria
    :param paramDIC: Dicionário contendo os parâmetros divididos por categoria, onde a key é a acategoria
    :param savepath: Caminho para salvar o arquivo do excel
    :return: Novo documento do excel
    """
    import string

    def FamilyName(fam):
        try:
            nomenc = fam.Family.Name + " : " + fam.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            return nomenc
        except:
            return fam.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()

    def SuperLookupParameter(paramname, ele):
        try:
            param = ele.LookupParameter(paramname)
        except:
            if isinstance(FamilySymbol):
                param = ele.Family.LookupParameter(paramname)
            else:
                return "Parameter not found"
        else:
            try:
                if param.IsReadOnly:
                    return "Read-only parameter"
            except AttributeError:
                return "Parameter not found"
            else:
                if param.AsString() is not None:
                    return param.AsString()
                else:
                    return param.AsValueString()

    def GenerateExcelColumns():
        alpha = string.ascii_uppercase
        excelcol = []
        for l in alpha:
            excelcol.append(l)
        for l in alpha:
            for n in alpha:
                excelcol.append(l + n)
        return excelcol

    categories = eleDIC.keys()
    excelCOL = GenerateExcelColumns()

    # Inicia uma instância da aplicação
    excel = Excel.ApplicationClass()
    excel.Visible = True

    # Define o arquivo de trabalho
    workbook = excel.Workbooks.Add()

    for cat in categories:
        # Define uma nova worksheet (aba)
        myFAM = eleDIC[cat]  # Famílias da categoria atual
        myPAR = paramDIC[cat]  # Parâmetros da categoria atual
        worksheet = workbook.Worksheets.Add()
        worksheet.Name = cat
        # Insere coluna de famílias e de parâmetros
        for i in range(0, len(myFAM)):
            famNAME = FamilyName(myFAM[i])
            famLINE = str(i + 2)  # +2 pq começa na linha 2
            famCELL = worksheet.Range["A" + famLINE]  # Coluna A e linha i+2
            famCELL.Value2 = famNAME
            # Insere valores de parâmetros nas colunas de parâmetros
            for n in range(0, len(myPAR)):
                parDEF = myPAR[n].Definition
                parTIT = parDEF.Name + " (" + str(parDEF.ParameterType) + ")"
                parCOL = excelCOL[n + 1]  # Letra da coluna correspondente ao parâmetro
                # Renomeia o cabeçalho do parâmetro
                parCELL = worksheet.Range[parCOL + "1"]  # Coluna(letra) + linha 1
                parCELL.Value2 = parTIT
                # Preenche com os valores dos parâmetros
                valVAL = SuperLookupParameter(parDEF.Name, myFAM[i])  # Valor do parâmetro em questão
                valCELL = worksheet.Range[parCOL + famLINE]  # Cell do valor do parâmetro para aquela família
                valCELL.Value2 = valVAL
    workbook.SaveAs(savepath)
    return workbook


def LoadParametersFromExcel(excelpath, families=None):
    """

    :param excelpath: Caminho do arquivo excel
    :param families: Opcional: Caso preenchido, retornará os parâmetros para as famílias informadas aqui. Do contrário,
    lê parâmetros das famílias presentes no excel
    :return: Dicionário contendo as famílias, parâmetros e valores dos parâmetros
    """

    from System.Threading import Thread
    import string

    def WorksheetCheckEmpty(worksheet, app):
        if app.WorksheetFunction.CountA(worksheet.UsedRange) == 0 and worksheet.Shapes.Count == 0:
            return True
        else:
            return False

    dicOUT = {}  # Estrutura padrão dos dicionáios: key = Nome da família/type, value = [nomes dos parâmetros], [valores dos parâmetros]

    # Abrindo o workbook
    excel = Excel.ApplicationClass()
    excel.Visible = True
    try:
        Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo("en-US")
        workbook = excel.Workbooks.Open(excelpath)
    except:
        TaskDialog.Show("Erro", "Não foi poossível abrir o arquivo escolhido.")
        excel.Quit()
        sys.exit()

    # Caso as famílias já estejam explicitadas no excel (por padrão na coluna A2...)
    if families == None:
        # Definindo worksheet
        categories = workbook.Worksheets
        for worksheet in categories:
            if not WorksheetCheckEmpty(worksheet, excel):
                cellrange = GetWorksheetCellsRange(worksheet)
                lastCOL = cellrange[0]
                lastLIN = cellrange[1]
                wrksFAM = worksheet.Range["A2", "A" + lastLIN].Value2
                wrksPAR = worksheet.Range["B1", lastCOL + "1"].Value2
                # Dicionário key não aceita ':'
                for i, fam in enumerate(wrksFAM):
                    famLIN = str(i + 2)
                    famVAL = worksheet.Range["B" + famLIN, lastCOL + famLIN].Value2
                    dicOUT[fam.replace(":", "")] = [wrksPAR, famVAL]
    """
    else:
        for fam in families:
            cat = fam.Category.Name
            try:
                worksheet = workbook.Worksheets(cat)
            except:
                TaskDialog.Show("Atenção", 'Não foi poossível encontrar parâmetros para a categoria: {}. O script continuará a execução para as próximas categorias.'.format(mycategory))
                continue
    """
    return dicOUT
