import json
from typing import List

from pxr import Gf, Sdf, Sdr, Vt

"""
TODO:
    - Document code properly
    - Run unit tests for this class
    - Change naming to fit Materialx better
    - Cross compare with old database 
"""

class MaterialxSdrDatabase:

    def __init__(self) -> None:
        self.registry: Sdr.Registry = Sdr.Registry()
        self.nodes = {}
        self.types = [ type for type in dir(Sdf.ValueTypeNames) if not type.startswith("__") ]
        self.__GetMaterialxNodes()
        self.__WriteToJson()

    def __IsUsdMatrix(self, input) -> bool:
        # need to check this amongst all inputs of all shaders to make sure nothing is missed
        matrixTypes = [
            Gf.Matrix2d, Gf.Matrix2f, Gf.Matrix3d, Gf.Matrix3f, Gf.Matrix4d, Gf.Matrix4f ]

        if ( type(input) in matrixTypes ):
            return True
        return False

    def __IsUsdVector(self, input) -> bool:
        vectorTypes = [
            Gf.Vec2d, Gf.Vec2f, Gf.Vec2h, Gf.Vec2i, 
            Gf.Vec3d, Gf.Vec3f, Gf.Vec3h, Gf.Vec3i, 
            Gf.Vec4d, Gf.Vec4f, Gf.Vec4h, Gf.Vec4i ]

        if ( type(input) in vectorTypes ):
            return True
        return False

    def __ConvertValues(self, input):
        if self.__IsUsdMatrix(input):
            convertedValue = tuple([tuple(i) for i in input])
        elif self.__IsUsdVector(input):
            convertedValue = tuple(input)
        else:
            convertedValue = input

        return convertedValue

    def __ConvertDataTypes(self, type):
        stringType = str(type[0])
        if stringType[-2:] == "[]": stringType = stringType.replace("[]", "array") # Accounting for the registry's way of representing arrays

        return [ type for type in self.types if type.lower() == stringType ][0]

    def __GetMaterialxNodes(self) -> None:
        for node in self.registry.GetNodeNames():
            if not node.startswith("ND_"): continue

            shaderNode: Sdr.ShaderNode = self.registry.GetShaderNodeByIdentifier(node)
            inputNames: List[str]      = shaderNode.GetInputNames()
            outputNames: List[str]     = shaderNode.GetOutputNames()
            metadata: dict             = shaderNode.GetMetadata()

            _node  = {}
            inputs = {}
            for input in inputNames:
                """
                inputName : {
                            type: Sdf.ValueTypeName,
                            defaultValue: Any,
                            metadata: { name : value }
                            }
                """
                _input = {}
                inputProperty         = shaderNode.GetInput(input)
                inputPropertyName     = inputProperty.GetName()
                inputPropertyType     = inputProperty.GetTypeAsSdfType()
                inputPropertyValue    = inputProperty.GetDefaultValue()
                inputPropertyMetadata = inputProperty.GetMetadata()

                convertedType  = self.__ConvertDataTypes(inputPropertyType)
                convertedValue = self.__ConvertValues(inputPropertyValue)

                _input["type"]          = convertedType
                _input["default_value"] = convertedValue
                _input["metadata"]      = inputPropertyMetadata

                inputs[inputPropertyName] = _input

            outputs = {}
            for output in outputNames:
                """
                outputName : {
                             type : Sdf.ValueTypeName,
                             default_value : Any,
                             metadata : { name : value }
                             }
                """
                _output = {}
                outputProperty         = shaderNode.GetOutput(output)
                outputPropertyName     = outputProperty.GetName()
                outputPropertyType     = outputProperty.GetTypeAsSdfType()
                outputPropertyValue    = outputProperty.GetDefaultValueAsSdfType()
                outputPropertyMetadata = outputProperty.GetMetadata()

                convertedType = self.__ConvertDataTypes(outputPropertyType)

                if type(outputPropertyValue) == Vt.StringArray:
                    convertedValue = [[]]
                elif type(outputPropertyValue) == Vt.Vec3fArray or type(outputPropertyValue) == Vt.Vec4fArray:
                    convertedValue = []
                else:
                    convertedValue = self.__ConvertValues(outputPropertyValue)

                _output["type"]          = convertedType
                _output["default_value"] = convertedValue
                _output["metadata"]      = outputPropertyMetadata

                outputs[outputPropertyName] = _output

            _node["inputs"]   = inputs
            _node["outputs"]  = outputs
            _node["metadata"] = outputPropertyMetadata
            
            self.nodes[node] = _node

    def __WriteToJson(self) -> None:
        with open("database.json", "w") as file:
            file.write(json.dumps(self.nodes, sort_keys = True, indent = 4))

if __name__ == "__main__":
    MaterialxSdrDatabase()
