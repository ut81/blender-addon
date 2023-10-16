import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty

class OBJECT_PT_SimpleShapeGeneratorPanel(bpy.types.Panel):
    bl_label = "Simple Shape Generator"
    bl_idname = "OBJECT_PT_SimpleShapeGeneratorPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Dropdown to select shape type
        layout.label(text="Select Shape:")
        layout.prop(context.scene, "shape_type")

        # Button to create the selected shape
        layout.operator("object.create_simple_shape", text="Create Shape")

class CreateSimpleShapeOperator(Operator):
    bl_idname = "object.create_simple_shape"
    bl_label = "Create Simple Shape"

    # Properties for the custom modal dialog
    new_shape_name: StringProperty(
        name="Shape Name",
        description="Enter a name for the new shape",
        default="pizza",
    )
    x_coordinate: FloatProperty(
        name="X Coordinate",
        description="X coordinate for the shape",
        default=0,
    )
    y_coordinate: FloatProperty(
        name="Y Coordinate",
        description="Y coordinate for the shape",
        default=0,
    )
    z_coordinate: FloatProperty(
        name="Z Coordinate",
        description="Z coordinate for the shape",
        default=0,
    )

    def invoke(self, context, event):
        # Open the custom modal dialog to get the shape name and coordinates
        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):
        shape_type = context.scene.shape_type
        new_name = self.new_shape_name
        x_coord = self.x_coordinate
        y_coord = self.y_coordinate
        z_coord = self.z_coordinate

        if shape_type == 'CIRCLE':
            bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1, location=(x_coord, y_coord, z_coord))
        elif shape_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x_coord, y_coord, z_coord))
        elif shape_type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(x_coord, y_coord, z_coord))

        # Rename the newly created object
        bpy.context.active_object.name = new_name

        self.report({'INFO'}, f'Shape name: {new_name}, Position: ({x_coord}, {y_coord}, {z_coord})')

        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_PT_SimpleShapeGeneratorPanel)
    bpy.utils.register_class(CreateSimpleShapeOperator)
    bpy.types.Scene.shape_type = bpy.props.EnumProperty(
        items=[('CIRCLE', 'Circle', 'Create a circle'), ('CUBE', 'Cube', 'Create a cube'), ('SPHERE', 'Sphere', 'Create a sphere')],
        name="Shape Type",
        default='CIRCLE'
    )
    bpy.types.Scene.new_shape_name = bpy.props.StringProperty()

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_SimpleShapeGeneratorPanel)
    bpy.utils.unregister_class(CreateSimpleShapeOperator)
    del bpy.types.Scene.shape_type
    del bpy.types.Scene.new_shape_name

if __name__ == "__main__":
    register()
