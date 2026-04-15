import os
import sys
from pathlib import Path
from typing import Any

from pxr import Sdf

sys.path.append(str(Path(__file__).parent.parent))

from database.database import MtlxItem
from utils import ConvertStringToSdfPath, TimeExecution

# NOTE: I might deprecate this class unless I can find a better use for it

class SdfShaderInput:
    """
    A class representation of a shader input for easier input manipulation
    """

    def __init__(self, primSpec: Sdf.PrimSpec, inputName: str, inputType: Any, inputValue: Any = None, customData = None) -> None:
        """
        Constructor

        :param spec:       The input PrimSpec to assign the AttributeSpec to
        :param name:       The name of the created AttributeSpec.
        :param type:       The data type of the AttributeSpec.
        :param value:      The default value of the AttributeSpec.
        :param customData: Sets the customData to the given data.
        """

        # TODO: Add getters and setters
        # TODO: Add a way to create time sampled inputs
        # TODO: Make all public members private

        self.primSpec   = primSpec
        self.inputName  = inputName
        self.inputType  = inputType
        self.inputValue = inputValue
        self.customData = customData

        self._attributeSpec = Sdf.AttributeSpec(self.primSpec, self.inputName, self.inputType)
        self._attributeSpec.default = self.inputValue
        self._attributeSpec.customData = self.customData

    @property
    def attributeSpec(self):
        return self._attributeSpec

    def Set(self, inputValue: Any) -> None:
        self.inputValue = inputValue
        self._attributeSpec.default = self.inputValue 




