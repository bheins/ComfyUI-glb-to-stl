# AI_ASSISTED

# GLB to STL Node

This custom node converts a 3D mesh from GLB format to STL format. It is designed to be used within the ComfyUI framework.
I created this as a stop gap to allow me to turn drawings or 2d images into STL files for my 3d printer.

## Usage Instructions

1. **Add the Node**: Include the `GLBToSTLNode` in your ComfyUI workflow.
2. **Input the Source Mesh**: Provide the path to the GLB file you wish to convert in the `source_mesh` input.
3. **Specify Output Path**: Enter the desired file path for the output STL file in the `output_path` input.
4. **Run the Node**: Execute the node to perform the conversion.

## Input Specifications

- **source_mesh**: 
  - Type: File Path (GLB format)
  - Description: The path to the input GLB file that you want to convert.

- **output_path**: 
  - Type: String
  - Description: The path where the resulting STL file will be saved.

## Output Specifications

- The node will produce an STL file at the specified `output_path` upon successful conversion.

## Dependencies

- Ensure that you have the necessary libraries installed for handling GLB and STL file formats. This may include libraries such as `pythreejs`, `numpy-stl`, or others depending on your implementation.

## Example

```python
# Example usage in a ComfyUI workflow
glb_to_stl_node = GLBToSTLNode()
glb_to_stl_node.source_mesh = "path/to/input.glb"
glb_to_stl_node.output_path = "path/to/output.stl"
glb_to_stl_node.process()
```

## Notes

- Make sure the input GLB file is valid and accessible.
- Check permissions for the output directory to avoid write errors.