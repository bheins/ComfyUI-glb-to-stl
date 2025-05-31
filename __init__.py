from .glb_converter import Mesh3DExporterNode

NODE_CLASS_MAPPINGS = {
    "Mesh3DExporterNode": Mesh3DExporterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Mesh3DExporterNode": "Mesh3D Exporter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
