import pytest
from pxr import Sdf
from sdf.input import SdfShaderInput
from sdf.shader import SdfMtlxShaderSpec

# NOTE: Just creating a simple layer setup as the input class needs it to run
# layer: Sdf.Layer = Sdf.Layer.CreateAnonymous()
# rootPrimSpec: Sdf.PrimSpec = Sdf.PrimSpec(layer, "root", Sdf.SpecifierDef, "Scope")
# materialPrimSpec: Sdf.PrimSpec = Sdf.PrimSpec(rootPrimSpec, "mtl", Sdf.SpecifierDef, "Material")
# materialShaderSpec = SdfMtlxShaderSpec(materialPrimSpec, "ND_standard_surface_surfaceshader_100")

@pytest.fixture
def FixtureShaderSpec() -> SdfMtlxShaderSpec:
    """
    A default standard surface shader spec
    """
    layer: Sdf.Layer = Sdf.Layer.CreateAnonymous()
    materialPrimSpec: Sdf.PrimSpec = Sdf.PrimSpec(layer, "mtl", Sdf.SpecifierDef, "Material")
    yield SdfMtlxShaderSpec(materialPrimSpec, "ND_standard_surface_surfaceshader_100")

@pytest.fixture
def FixtureShaderInput(FixtureShaderSpec) -> SdfShaderInput:
    """
    A base_color input for the default standard surface
    """
    return FixtureShaderSpec.CreateAttribute("base_color", (0, 1, 0))

def test_GetInputType(FixtureShaderInput) -> None:
    """
    TEST: Ensure that getting the input returns a USD friendly attribute spec
    """
    assert(type(FixtureShaderInput.attributeSpec) == Sdf.AttributeSpec)

def test_SetAttributeType(FixtureShaderInput) -> None:
    """
    TEST: Ensuring that the Set() method works and is changing the underlying attributeSpec
    """
    FixtureShaderInput.Set((1, 0, 0))
    assert(FixtureShaderInput.inputValue == (1, 0, 0))

@pytest.mark.parametrize("inputName, inputValue", [
    ("base_color", (0.18, 0.18, 0.18)),
    ("specular_roughness", 0.35),
    ("metalness", 1.0)
])
def test_CreatingShaderAttributes(FixtureShaderSpec, inputName, inputValue) -> None:
    """
    TEST: Testing to make sure input names and values translate properly into the ShaderInput class
    """
    attribute = FixtureShaderSpec.CreateAttribute(inputName, inputValue)

    assert(attribute.inputName == f"inputs:{inputName}")
    assert(attribute.inputValue == inputValue)
