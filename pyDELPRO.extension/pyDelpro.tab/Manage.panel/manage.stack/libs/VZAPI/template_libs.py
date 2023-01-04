import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')

import clr, os

clr.AddReference('DynamoRevitDS')
import Dynamo 

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

def FindThreeDirectory(target, file_path):
	"""
	:param target: Caminho na árvore de pastas que compõe o script que se deseja encontrar
	:param file_path: Caminho do arquivo referência
	:return: Caminho de uma pasta pertencente a arvore de pasta de um arquivo
	"""
	count = 0
	lastpath = file_path.split(sep="\\")[-1]
	target_path = os.path.dirname(file_path)
	while count < 10:
		if lastpath == target:
			return target_path
			break
		lastpath = target_path.split(sep="\\")[-1]
		target_path = os.path.dirname(target_path)
		count += 1
	return None


dynamoRevit = Dynamo.Applications.DynamoRevit()
currentWorkspace = dynamoRevit.RevitDynamoModel.CurrentWorkspace	
script_path = currentWorkspace.FileName.replace('\Home.dyn', '')

path_parent = FindThreeDirectory("VZ.tab", script_path)
if path_parent is None:
	OUT = TaskDialog.Show("Erro", "Não foi possível carregar a biblioteca RVTAPI. Reinstale o plugin ou contate o desenvolvedor.")
else:
	api_path = os.path.join(path_parent, "libs\\RVTAPI")
	dyna_logo = os.path.join(path_parent, "resources\\VZdynamologo.png")
	lib_path = os.path.join(path_parent, "libs")
	OUT = api_path, dyna_logo, lib_path