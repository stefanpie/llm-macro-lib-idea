from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class MacroAttribute(BaseModel):
    name: str = Field(..., description="Name of the macro attribute")
    default: Optional[str] = Field(
        default=None,
        description='Default value for the attribute, if any. Should be a string literal of the default value, e.g. "1", "32\'h00000000", "true", "ENABLED", etc.; these are verilog literal values.',
    )
    description: Optional[str] = Field(
        default=None, description="Human-readable description of the attribute"
    )


class MacroPort(BaseModel):
    name: str = Field(..., description="Port name")
    direction: Literal["input", "output", "inout"] = Field(
        ..., description="Direction of the port: input, output, or inout"
    )
    width: int = Field(1, description="Bit-width of the port (default: 1)")
    description: Optional[str] = Field(
        default=None, description="Human-readable description of the port"
    )


class Macro(BaseModel):
    name: str = Field(..., description="Macro name")
    description: str = Field(..., description="Description of the macro")
    ports: List[MacroPort] = Field(
        ..., description="List of ports belonging to the macro"
    )
    attributes: List[MacroAttribute] = Field(
        default_factory=list,
        description="List of attributes (i.e. parameters) for the macro",
    )


class MacroCollection(BaseModel):
    macros: List[Macro] = Field(..., description="Collection of Macro definitions")
