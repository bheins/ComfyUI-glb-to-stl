import os
import trimesh
import numpy as np
import pymeshlab
from pygltflib import GLTF2

class Mesh3DExporterNode:
    def __init__(self):
        # Use absolute path for output directory
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output", "mesh_exports"))
        os.makedirs(self.output_dir, exist_ok=True)
        
    SUPPORTED_FORMATS = {
        "STL Binary": {"extension": ".stl", "type": "stl"},
        "STL ASCII": {"extension": ".stl", "type": "stl-ascii"},
        "3MF": {"extension": ".3mf", "type": "3mf"},
        "OBJ": {"extension": ".obj", "type": "obj"},
        "PLY Binary": {"extension": ".ply", "type": "ply"},
        "PLY ASCII": {"extension": ".ply", "type": "ply-ascii"},
    }
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mesh": ("MESH", {"default": None}),  # Specify compatibility with ComfyUI-3D-Pack MESH type
                "output_filename": ("STRING", {"default": "output"}),
                "format": (list(cls.SUPPORTED_FORMATS.keys()), {"default": "STL Binary"}),
                "target_size_mm": ("FLOAT", {"default": 100.0, "min": 1.0, "max": 1000.0, "step": 1.0}),
                "min_size": ("FLOAT", {"default": 10.0, "min": 0.1, "max": 1000.0, "step": 0.1}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "convert"
    CATEGORY = "3D"
    OUTPUT_NODE = True

    def convert(self, mesh, output_filename, format, target_size_mm, min_size):
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
            if not base_name:
                base_name = "output"
            
            # Get format details from SUPPORTED_FORMATS
            format_info = self.SUPPORTED_FORMATS[format]
            output_filename = f"{base_name}{format_info['extension']}"
            
            # Get absolute output path
            output_path = os.path.abspath(os.path.join(self.output_dir, output_filename))
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Apply target size scaling if specified
            if target_size_mm > 0:
                current_size = mesh_obj.bounding_box.extents
                max_current_size = np.max(current_size)
                scale_factor = target_size_mm / max_current_size
                print(f"Scaling mesh to target size {target_size_mm}mm (current max size: {max_current_size:.2f}mm)")
                mesh_obj.apply_scale(scale_factor)
            elif min_size > 0:  # Apply minimum size scaling only if target_size not specified
                current_size = mesh_obj.bounding_box.extents
                min_current_size = np.min(current_size)
                if min_current_size < min_size:
                    scale_factor = min_size / min_current_size
                    print(f"Mesh is too small (smallest dimension: {min_current_size:.2f}). Scaling up by factor of {scale_factor:.2f}")
                    mesh_obj.apply_scale(scale_factor)
            
            print(f"Attempting to export {format} to: {output_path}")
            
            if format == "3MF":
                try:
                    # Export using pymeshlab for 3MF
                    ms = pymeshlab.MeshSet()
                    # Create a new mesh from vertex and face arrays
                    ms.add_mesh(vertex_matrix=mesh_obj.vertices, face_matrix=mesh_obj.faces)
                    ms.save_current_mesh(output_path)
                except Exception as e:
                    print(f"Error with pymeshlab export: {str(e)}")
                    # Fallback to trimesh export
                    mesh_obj.export(file_obj=output_path, file_type='3mf')
            else:
                # Export using trimesh with the specified format type
                mesh_obj.export(
                    file_obj=output_path,
                    file_type=format_info['type']
                )
            
            if not os.path.exists(output_path):
                raise ValueError(f"Failed to save {format} file at {output_path}")
                
            print(f"Successfully exported {format} to: {output_path}")
            return (output_path,)
            
        except Exception as e:
            print(f"Error exporting mesh: {str(e)}")
            return ("")
