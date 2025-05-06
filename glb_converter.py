import os
import trimesh
import numpy as np
from pygltflib import GLTF2

class GLBToSTLNode:
    def __init__(self):
        self.output_dir = "outputsglb_to_stl"
        os.makedirs(self.output_dir, exist_ok=True)
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mesh": ("MESH", {"default": None}),  # Specify compatibility with ComfyUI-3D-Pack MESH type
                "output_filename": ("STRING", {"default": "output.stl"}),
                "min_size": ("FLOAT", {"default": 10.0, "min": 0.1, "max": 1000.0, "step": 0.1}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("stl_path",)
    FUNCTION = "convert"
    CATEGORY = "3D"
    OUTPUT_NODE = True

    def convert(self, mesh, output_filename, min_size):
        try:
            # Debug print to inspect mesh structure
            print(f"Mesh type: {type(mesh)}")
            print(f"Mesh attributes: {dir(mesh)}")

            # Get vertices and faces from the mesh (ComfyUI-3D-Pack format)
            vertices = getattr(mesh, 'v', None)
            faces = getattr(mesh, 'f', None)

            if vertices is None or faces is None:
                raise ValueError("Invalid mesh data: could not find v (vertices) or f (faces)")

            # Convert from torch tensor to numpy if needed
            if hasattr(vertices, 'cpu') and hasattr(vertices, 'numpy'):
                vertices = vertices.cpu().numpy()
            if hasattr(faces, 'cpu') and hasattr(faces, 'numpy'):
                faces = faces.cpu().numpy()

            # Ensure proper shape
            if len(vertices.shape) != 2 or vertices.shape[1] != 3:
                raise ValueError(f"Invalid vertices shape: {vertices.shape}")
            if len(faces.shape) != 2 or faces.shape[1] != 3:
                raise ValueError(f"Invalid faces shape: {faces.shape}")

            # Create trimesh from mesh data directly using numpy arrays
            mesh_obj = trimesh.Trimesh(vertices=vertices, faces=faces)
            
            # Debug print for mesh validation
            print(f"Mesh validation - vertices: {len(mesh_obj.vertices)}, faces: {len(mesh_obj.faces)}")
            
            if not mesh_obj.is_watertight:
                print("Warning: Mesh is not watertight, but will attempt to export anyway")

            # After creating trimesh object but before export, add scaling logic
            current_size = mesh_obj.bounding_box.extents
            min_current_size = np.min(current_size)
            
            if min_current_size < min_size:
                scale_factor = min_size / min_current_size
                print(f"Mesh is too small (smallest dimension: {min_current_size:.2f}). Scaling up by factor of {scale_factor:.2f}")
                mesh_obj.apply_scale(scale_factor)

            # Handle output filename extension
            base_name = os.path.splitext(output_filename)[0]
            output_filename = f"{base_name}.stl"
            
            # Ensure output directory exists
            os.makedirs(self.output_dir, exist_ok=True)
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Export as STL without redundant file_obj parameter
            print(f"Attempting to export STL to: {output_path}")
            mesh_obj.export(output_path, file_type='stl')
            
            if not os.path.exists(output_path):
                raise ValueError("Failed to save STL file")
                
            print(f"Successfully exported STL to: {output_path}")
            return (output_path,)
            
        except Exception as e:
            print(f"Error converting mesh to STL: {str(e)}")
            return ("",)  # Return empty string instead of None for better workflow compatibility
