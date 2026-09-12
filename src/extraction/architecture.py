from pydantic import BaseModel, ConfigDict, Field, model_validator


class Component(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[a-z][a-z0-9_]{0,39}$")
    label: str = Field(min_length=1, max_length=200)
    technology: str | None = Field(max_length=200)
    evidence: str = Field(min_length=1, max_length=500)


class Connection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str
    target: str
    label: str | None = Field(max_length=200)
    evidence: str = Field(min_length=1, max_length=500)


class Boundary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1, max_length=200)
    component_ids: list[str] = Field(max_length=50)
    evidence: str = Field(min_length=1, max_length=500)


class ArchitectureObservation(BaseModel):
    """Model-proposed observations; human review is still required."""
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(max_length=200)
    components: list[Component] = Field(max_length=50)
    connections: list[Connection] = Field(max_length=100)
    boundaries: list[Boundary] = Field(max_length=20)
    uncertainties: list[str] = Field(max_length=50)
    inferences: list[str] = Field(max_length=50)

    @model_validator(mode="after")
    def validate_references(self) -> "ArchitectureObservation":
        ids = {c.id for c in self.components}
        if len(ids) != len(self.components):
            raise ValueError("Duplicate component IDs")
        edges = set()
        for edge in self.connections:
            if edge.source not in ids or edge.target not in ids:
                raise ValueError("Connection references an unknown component")
            identity = (edge.source, edge.target, edge.label)
            if identity in edges:
                raise ValueError("Duplicate connection")
            edges.add(identity)
        for boundary in self.boundaries:
            if not set(boundary.component_ids) <= ids:
                raise ValueError("Boundary references an unknown component")
        if not self.components and not self.uncertainties:
            raise ValueError("An empty analysis must explain its uncertainty")
        return self
