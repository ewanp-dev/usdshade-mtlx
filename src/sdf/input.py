import os
import sys
from typing import Any

from pxr import Sdf

sys.path.append(os.path.abspath(".."))

from database.database import MtlxItem
from utils import ConvertStringToSdfPath, TimeExecution


class SdfShaderInput:
    """
    A class representation of a shader input for easier input manipulation
    """

    def __init__(
        self,
        spec,
        name: str,
        type,
        value: Any = None,
        customData = None) -> None:
        """
        Constructor
        """

        self.name = name
        self.type = type
        self.value = value
        print(self.value)
        self.customData = customData
        self.input = Sdf.AttributeSpec(spec, name, type)
        self.input.default = value
        self.input.customData = self.customData
