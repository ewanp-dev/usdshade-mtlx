import os
import sys

from pxr import Sdf

sys.path.append(os.path.abspath(".."))

from BaseUtils import ConvertStringToSdfPath


class SdfMtlXSpec:

    def __init__(self, parentPrim, materialName):
        self.__materialName = materialName
        self.__parentPrim = parentPrim
        self.__materialSpec = Sdf.PrimSpec(parentPrim, materialName, Sdf.SpecifierDef, "Material")

    def GetPrimSpec(self) -> Sdf.PrimSpec:
        return self.__materialSpec

    def AssignToPrimSpec(self, primSpec: Sdf.PrimSpec, purpose=None) -> None:
        materialBindingRelationship = Sdf.RelationshipSpec(primSpec, "material:binding", custom = False)
        materialBindingRelationship.targetPathList.Append(self.GetPrimSpec().path)

        # TODO: Need further testing with this
        schemas = Sdf.TokenListOp.Create(appendedItems = ["MaterialBindingAPI"])
        primSpec.SetInfo("apiSchemas", schemas)

    def ConnectToShaderSpec(self, shaderSpec, sourceName: str = None) -> None:
        if ( len(shaderSpec.database.GetOutputs()) == 1 ):
            sourceName = f"outputs:{shaderSpec.database.GetOutputs()[0]}"

        sourcePath = shaderSpec.GetPrimSpec().path.AppendProperty(sourceName)
        materialOutputAttribute = Sdf.AttributeSpec(self.__materialSpec, "outputs:surface", Sdf.ValueTypeNames.Token)
        materialOutputAttribute.connectionPathList.Append(sourcePath)
