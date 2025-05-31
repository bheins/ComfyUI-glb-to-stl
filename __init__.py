from .glb_converter import Mesh3DExporterNode
from .mesh_simplifier import MeshSimplifierNode

NODE_CLASS_MAPPINGS = {
    "Mesh3DExporterNode": Mesh3DExporterNode,
    "MeshSimplifierNode": MeshSimplifierNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Mesh3DExporterNode": "Mesh3D Exporter",
    "MeshSimplifierNode": "Mesh Simplifier"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
