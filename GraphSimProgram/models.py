from __future__ import annotations

class Vertex():
    def __init__(self:Vertex, name:str) -> None:
        self.neighbours = []
        self.name = name
        self.color = 0