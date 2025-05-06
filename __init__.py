from .glb_converter import GLBToSTLNode

NODE_CLASS_MAPPINGS = {
    "GLBToSTLNode": GLBToSTLNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GLBToSTLNode": "GLB to STL Converter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
