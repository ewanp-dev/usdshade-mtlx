import os
import sys
from typing import Any, List

from pxr import Sdf, Usd

sys.path.append(os.path.abspath(".."))

from input import SdfShaderInput

from database.database import MtlxItem
from utils import ConvertStringToSdfPath, TimeExecution


class SdfMtlxShaderSpec:

    def __init__(self, parentPrim, node, nodeName = None) -> None:

        self.parentPrim = parentPrim
        self.database   = MtlxItem(node)
        self.node       = self.database.node
        self.id         = self.database.node_id
        self.nodeName   = nodeName if nodeName else self.id[3:] # removes the 'ND_'
        
        self.__setup()

    def __setup(self) -> None:
        self.shaderPrimSpec = Sdf.PrimSpec(self.parentPrim, self.nodeName, Sdf.SpecifierDef, "Shader")

        idAttribute = Sdf.AttributeSpec(self.shaderPrimSpec, "info:id", Sdf.ValueTypeNames.Token)
        idAttribute.default = self.id
        idAttribute.SetInfo("variability", Sdf.VariabilityUniform)

        for output in self.database.GetOutputs():
            Sdf.AttributeSpec(self.shaderPrimSpec, f"outputs:{output}", self.database.GetOutputType(output))

    def GetPrimSpec(self) -> Sdf.PrimSpec:
        return self.shaderPrimSpec

    def CreateAttribute(self, name, value = None, customData = None) -> None:
        # TODO: Return input
        valueType = self.database.GetInputType(name)
        inputName = name if name.startswith("inputs:") else f"inputs:{name}"

        if not customData:
            dataDictionary = self.database.GetInputMetadata(name)
        else:
            dataDictionary = {**self.database.GetInputMetadata(name), **customData}

        return SdfShaderInput(self.shaderPrimSpec, inputName, valueType, value, dataDictionary)

    def GetInputs(self, authoredOnly: bool = True) -> List[Any]:
        return

if __name__ == "__main__":

    @TimeExecution
    def main():

        layer: Sdf.Layer = Sdf.Layer.CreateNew("shader_test_v001.usd")
            
        rootPrimSpec: Sdf.PrimSpec = Sdf.PrimSpec(layer, "root", Sdf.SpecifierDef, "Scope")
        materialPrimSpec: Sdf.PrimSpec = Sdf.PrimSpec(rootPrimSpec, "mtl", Sdf.SpecifierDef, "Material")
        shaderSpec = SdfMtlxShaderSpec(materialPrimSpec, "ND_standard_surface_surfaceshader_100")
        shaderSpec.CreateAttribute("base_color", (0, 1, 0))

        layer.Save()

    main()
