import os
import sys
from typing import List

from pxr import Sdf

from Material import SdfMtlXSpec
from Shader import SdfMtlXShaderSpec

sys.path.append(os.path.abspath(".."))
from BaseUtils import ConvertStringToSdfPath, TimeExecution
from database.database import MaterialXItem


class SdfMtlx:


    def __init__(self) -> None:
        pass

    def CreateMaterialSpec(parentPrim, materialName) -> SdfMtlXSpec:
        # TODO: Add custom specifier option
        return SdfMtlXSpec(parentPrim, materialName)

    def CreateShaderSpec(parentPrim, node, nodeName = None) -> SdfMtlXShaderSpec:
        return SdfMtlXShaderSpec(parentPrim, node, nodeName)


if __name__ == "__main__":

    def Test() -> None:
        layer = Sdf.Layer.CreateNew("sdfmtlx_test.usd")
        
        rootPrimSpec = Sdf.PrimSpec(layer, "root", Sdf.SpecifierDef, "Scope")

        geoPrimSpec = Sdf.PrimSpec(rootPrimSpec, "geo", Sdf.SpecifierDef, "Xform")
        cubePrimSpec = Sdf.PrimSpec(geoPrimSpec, "cube1", Sdf.SpecifierDef, "Cube")

        mtlPrimSpec = Sdf.PrimSpec(rootPrimSpec, "mtl", Sdf.SpecifierDef, "Scope")
        materialPrimSpec = SdfMtlx.CreateMaterialSpec(mtlPrimSpec, "mtl_test")
        materialPrimSpec.AssignToPrimSpec(geoPrimSpec)

        shaderSpec = SdfMtlx.CreateShaderSpec(materialPrimSpec.GetPrimSpec(), "ND_standard_surface_surfaceshader_100")
        shaderSpec.CreateAttribute("base_color", (1.0, 0.0, 0.0))

        materialPrimSpec.ConnectToShaderSpec(shaderSpec)

        layer.Save()

    Test()

