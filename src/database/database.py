import json
import os
from typing import Any, List

from pxr import Sdf

"""
TODO:
    - Fully docstring all functions
    - Improve functionality
"""

class MaterialXItem:
    """
    A container for a MaterialX item, contains the necessary information
    to create MaterialX shaders
    """

    def __init__(self, node: str = "") -> None:
        """
        Constructor

        :param node: The name of the MaterialX node to access.
        """
        with open(f"{os.path.abspath('..')}/database/database.json") as file:
            self.data = json.load(file)

        if node not in self.data.keys():
            raise Exception("Invalid Node!")

        self.node: str = node
        if ( self.node == "ND_standard_surface_surfaceshader_100" ):
            self.node_id: str = "ND_standard_surface_surfaceshader"
        
        else:
            self.node_id: str = self.node

        self.__convert_data(self.node)

        self.__inputs  = self.data[self.node]["inputs"]
        self.__outputs = self.data[self.node]["outputs"]

    def __convert_data(self, node: str) -> None:
        """
        Converts the data types in json from Strings to USD friendly data types

        :param node: The input node(materialx shader name).
        """
        inputs = self.data[node]["inputs"]
        for inputAttribute in inputs.keys():
            inputs[inputAttribute]["type"] = getattr(Sdf.ValueTypeNames, inputs[inputAttribute]["type"])

        outputs = self.data[node]["outputs"]
        for outputAttribute in outputs.keys():
            outputs[outputAttribute]["type"] = getattr(Sdf.ValueTypeNames, outputs[outputAttribute]["type"])

    def __checkInput(self, input: str) -> None:
        if not input in self.__inputs.keys(): raise Exception("Invalid Input!")

    def __checkOutput(self, output: str) -> None:
        if not output in self.__outputs.keys(): raise Exception("Invalid Output!")

    def GetInputs(self) -> List[str]:
        """
        Returns a list of all available inputs for the MaterialX node
        """
        return list(self.__inputs.keys())

    def GetOutputs(self) -> List[str]:
        """
        Returns a list of all available outputs for the MaterialX node
        """
        return list(self.__outputs.keys())
    
    def GetMetadata(self) -> List[str]:
        """
        Returns a list of all available metadata for the MaterialX node
        """
        return self.data[self.node]["metadata"]

    def GetInputType(self, input: str) -> Sdf.ValueTypeName:
        self.__checkInput(input)
        return self.__inputs[input]["type"]

    def GetInputValue(self, input: str) -> Any:
        self.__checkInput(input)
        return self.__inputs[input]["default_value"]

    def GetInputMetadata(self, input: str) -> dict:
        self.__checkInput(input)
        return self.__inputs[input]["metadata"]

    def GetOutputType(self, output: str) -> Sdf.ValueTypeName:
        self.__checkOutput(output)
        return self.__outputs[output]["type"]

    def GetOutputValue(self, output: str) -> Any:
        self.__checkOutput(output)
        return self.__outputs[output]["default_value"]

    def GetOutputMetadata(self, output: str) -> dict:
        self.__checkOutput(output)
        return self.__outputs[output]["metadata"]


def GetMaterialXNodes() -> List[str]:
    """
    Returns a list of all available MaterialX nodes

    :return: Returns a list of strings containing the names of each possible MaterialX node.
    """
    with open(f"{os.path.abspath('..')}/database/database.json") as file:
        data: dict = json.load(file)

    return list(data.keys())

if __name__ == "__main__":
    surfaceShaderItem = MaterialXItem("ND_standard_surface_surfaceshader_100")
