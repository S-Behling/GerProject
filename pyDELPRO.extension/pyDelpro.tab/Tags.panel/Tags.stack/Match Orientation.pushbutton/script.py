"""
Match Tag Orientation

Match orientatiion to the pre-selected tag.

TESTADO: RVT 2020

--------------------------------------------------------
RevitPythonWrapper: revitpythonwrapper.readthedocs.io

"""

import os
#from collections import namedtuple

from pyrevit import revit, DB, forms, script

import rpw
from rpw import doc, uidoc, DB, UI

from tags_wrapper import *


#Point = namedtuple('Point', ['X', 'Y','Z'])

cView = doc.ActiveView
Tags = rpw.ui.Selection()

         
if cView.ViewType in [DB.ViewType.FloorPlan, DB.ViewType.CeilingPlan, DB.ViewType.Detail, DB.ViewType.AreaPlan, DB.ViewType.Section, DB.ViewType.Elevation]:
        
    if len(Tags) < 1:
        UI.TaskDialog.Show('pyRevitPlus', 'A tag must preselected')
    if len(Tags) > 1:
        UI.TaskDialog.Show('pyRevitPlus', 'Select a SINGLE tag')
    else:
        cTag = Tags[0]
        cOrientation = cTag.TagOrientation
    
        with forms.WarningBar(title='Pick tag One by One. ESCAPE to end.'):
            match_orientation(cTag.Category, cOrientation)
        