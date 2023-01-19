# coding=utf-8
# !/usr/bin/python

import clr
import sys
import System
from System.Collections.Generic import List

# adding Iron Python Path to System Variable.
# Needed to import any Iron Python module
ipython_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(ipython_path)

pyt27_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt27_path)

pyt26_path = r'C:\Program Files (x86)\IronPython 2.6\Lib'
sys.path.append(pyt27_path)

# <<< Iron Python Modules >>>
# BEGIN

# Import traceback module from Iron Python
import traceback
import csv
import StrongBox
import random as rnd
import math

# END

# Import System Libraries
clr.AddReference("System.Core")
from System.Collections.Generic import List as SystemList

# Import Linq
clr.ImportExtensions(System.Linq)

# Import Dynamo Library Nodes - Geometry
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript import Geometry as DynamoGeometry

# Import Dynamo Library Nodes - Core
clr.AddReference('DSCoreNodes')
from DSCore import List as DynamoList

# Import Dynamo Library Nodes - Core
clr.AddReference('DSCoreNodes')
from DSCore import Color as DynamoColor

# Import Dynamo Geometry Color
# https://forum.dynamobim.com/t/geometrycolor-bygeometrycolor-inside-python/52724
clr.AddReference('GeometryColor')
from Modifiers import GeometryColor as DynamoGeometryColorize

# Import Dynamo Library Nodes - Revit
clr.AddReference("RevitNodes")
import Revit as RevitNodes

# Import ToDSType(bool) extension method
clr.ImportExtensions(RevitNodes.Elements)
clr.ImportExtensions(RevitNodes.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import Revit API
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import Revit User Interface API
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

# Import Revit IFC API
# https://forum.dynamobim.com/t/ifcexportutils/4833/7?u=ricardo_freitas
clr.AddReference('RevitAPIIFC')
from Autodesk.Revit.DB.IFC import *

# Import Dynamo Services
import clr
clr.AddReference('DynamoServices')
from Dynamo import Events as DynamoEvents

# Active Dynamo Workspace Path
workspaceFullPath = DynamoEvents.ExecutionEvents.ActiveSession.CurrentWorkspacePath
workspacePath = '\\'.join(workspaceFullPath.split('\\')[0:-1])

# Dev path
assembly_path = r"C:\Program Files\Autodesk\Revit 2021"
sys.path.append(assembly_path)

# Dynamo Nodes
clr.AddReference("RevitNodes")
import Revit

try:
    clr.ImportExtensions(Revit)
    clr.ImportExtensions(Revit.Elements)
    clr.ImportExtensions(Revit.GeometryConversion)
except:
    pass

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

# FUNCOES 
# >>>
def GetRoomFinishes(doc, room, includeLinkedElements=False, subFaceType=None):
    """
    Gets Rooms Finishes
    SubFaceType enum
    
    Bottom	
    A horizontal face at the bottom of the room, 
    as defined by the room's level and base offset, 
    or a face of the room that is bounded below by a room-bounding element.

    Top
    A horizontal top face of the room as defined by the room's level and height, 
    or a face of the room that is bounded above by a room-bounding element.

    Side	
    Any face which does not meet the criteria to be Top or Bottom.
    """
    calculator = SpatialElementGeometryCalculator(doc)
    calculatorResults = calculator.CalculateSpatialElementGeometry(room)

    roomSolid = calculatorResults.GetGeometry()
    finishes = []
    for face in roomSolid.Faces:
        # Retorna face vazia se não encontrar um elemento delimitador do Room
        # Por exemplo um Room sem forro
        boundaryFaces = calculatorResults.GetBoundaryFaceInfo(face)

        if boundaryFaces.Any():
            for bface in boundaryFaces:
                faceType = bface.SubfaceType

                if renner == 1:
                    if isinstance(faceType, Ceiling):
                        desativaPar = faceType.LookupParameter("Room Bounding")
                        desativaPar.Set(False)

                if (subFaceType is not None) and (faceType != subFaceType):
                    continue
                
                hostId = bface.SpatialBoundaryElement.HostElementId
                hostDoc = doc
                
                hostFromLink = True if hostId.IntegerValue == -1 else False

                if includeLinkedElements and hostFromLink:
                    # Get host Id from link
                    linkedElementId = bface.SpatialBoundaryElement.LinkedElementId
                    hostId = linkedElementId
                    
                    # Get host linked document
                    linkInstanceId = bface.SpatialBoundaryElement.LinkInstanceId
                    linkedDocument = doc.GetElement(linkInstanceId).GetLinkDocument()
                    hostDoc = linkedDocument

                hostElement = hostDoc.GetElement(hostId)

                if hostElement is not None:
                    hostElementType = hostDoc.GetElement(hostElement.GetTypeId())
                    finishes.append(hostElement)

    return finishes

def VolumeComputationsControl(enable=True):
    """
    Enable/Disable Volume Computations
    """
    # Start Transaction
    TransactionManager.Instance.EnsureInTransaction(doc)

    areaVolumeSettings = AreaVolumeSettings.GetAreaVolumeSettings(doc)
    areaVolumeSettings.ComputeVolumes = enable

    # End Transaction
    TransactionManager.Instance.TransactionTaskDone()

def RoomTopFinishHeight(room, topFinish):

    roomLevelElevation = doc.GetElement(room.LevelId).Elevation

    topFinishLevelElevation = doc.GetElement(topFinish.LevelId).Elevation

    value_To_discount = 0
    if isinstance(topFinish, Ceiling):
        topFinishOffset = topFinish.get_Parameter(BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM).AsDouble()
      
    elif isinstance(topFinish, Floor):
        topFinishOffset = topFinish.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).AsDouble()

        # Desconta a espessura do Floor
        value_To_discount = topFinish.get_Parameter(BuiltInParameter.FLOOR_ATTR_THICKNESS_PARAM).AsDouble()
    
    elif isinstance(topFinish, FootPrintRoof):
        topFinishOffset = topFinish.get_Parameter(BuiltInParameter.ROOF_LEVEL_OFFSET_PARAM).AsDouble()

        # Coloca 10 cm de transpasse para cima
        #value_To_discount = -UnitsConvertionTools(doc).MToInternalLength(0.1)

    else:
        topFinishOffset = 0

    return ((topFinishLevelElevation + topFinishOffset) - roomLevelElevation) - value_To_discount

def eCelling(room, topFinish):

    # roomLevelElevation = doc.GetElement(room.LevelId).Elevation

    # topFinishLevelElevation = doc.GetElement(topFinish.LevelId).Elevation
    TransactionManager.Instance.EnsureInTransaction(doc)

    value_To_discount = 0
    if isinstance(topFinish, Ceiling):
        desativaCelling = topFinish.get_Parameter(BuiltInParameter.WALL_ATTR_ROOM_BOUNDING).Set(False)
    
    TransactionManager.Instance.TransactionTaskDone()

    doc.Regenerate()


class UnitsConvertionTools:
    def __init__(self, doc):
        self.doc = doc
    
    def GetLengthDisplayUnits(self):
        return self.doc.GetUnits().GetFormatOptions(UnitType.UT_Length).DisplayUnits

    def GetAreaDisplayUnits(self):
        return self.doc.GetUnits().GetFormatOptions(UnitType.UT_Area).DisplayUnits

    def GetAngleDisplayUnits(self):
        return self.doc.GetUnits().GetFormatOptions(UnitType.UT_Angle).DisplayUnits

    def InternalLengthToCM(self, x):
        return UnitUtils.ConvertFromInternalUnits(x, DisplayUnitType.DUT_CENTIMETERS)

    def InternalLengthToDisplayUnits(self, x):
        return UnitUtils.ConvertFromInternalUnits(x, self.GetLengthDisplayUnits())
    
    def InternalAreaToDisplayUnits(self, x):
        return UnitUtils.ConvertFromInternalUnits(x, self.GetAreaDisplayUnits())
    
    def LengthDisplayUnitsToInternal(self, x):
        return UnitUtils.ConvertToInternalUnits(x, self.GetLengthDisplayUnits())

    def AreaDisplayUnitsToInternal(self, x):
        return UnitUtils.ConvertToInternalUnits(x, self.GetAreaDisplayUnits())

    def AngleDisplayUnitsToInternal(self, x):
        return UnitUtils.ConvertToInternalUnits(x, self.GetAngleDisplayUnits())

    def CMToInternalLength(self, x):
        return UnitUtils.ConvertToInternalUnits(x, DisplayUnitType.DUT_CENTIMETERS)

    def MToInternalLength(self, x):
        return UnitUtils.ConvertToInternalUnits(x, DisplayUnitType.DUT_METERS)
    
    def SquareCMToInternalArea(self, x):
        return UnitUtils.ConvertToInternalUnits(x, DisplayUnitType.DUT_SQUARE_CENTIMETERS)
    
    def SquareMToInternalArea(self, x):
        return UnitUtils.ConvertToInternalUnits(x, DisplayUnitType.DUT_SQUARE_METERS)

    def SquareCMToSquareM(self, x):
        return UnitUtils.Convert(x, DisplayUnitType.DUT_SQUARE_CENTIMETERS, DisplayUnitType.DUT_SQUARE_METERS)

    def SquareMToSquareCM(self, x):
        return UnitUtils.Convert(x, DisplayUnitType.DUT_SQUARE_METERS, DisplayUnitType.DUT_SQUARE_CENTIMETERS)

    def CMToDisplayUnits(self, x):
        lengthDisplayUnits = self.GetLengthDisplayUnits()
        
        return UnitUtils.Convert(x, DisplayUnitType.DUT_CENTIMETERS, lengthDisplayUnits)

    def DisplayUnitsToCM(self, x):
        lengthDisplayUnits = self.GetLengthDisplayUnits()
        
        return UnitUtils.Convert(x, lengthDisplayUnits, DisplayUnitType.DUT_CENTIMETERS)
