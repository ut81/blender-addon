import bpy

class SimpleShapeGeneratorPanel(bpy.types.Panel):
    bl_label = "Simple Shape Generator"
    bl_idname = "PT_SimpleShapeGeneratorPanel"
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

class CreateSimpleShapeOperator(bpy.types.Operator):
    bl_idname = "object.create_simple_shape"
    bl_label = "Create Simple Shape"

    def execute(self, context):
        if context.scene.shape_type == 'CIRCLE':
            bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1, location=(10, 0, 0))
        elif context.scene.shape_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
            
        elif context.scene.shape_type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 10, 0))

        return {'FINISHED'}

def register():
    bpy.utils.register_class(SimpleShapeGeneratorPanel)
    bpy.utils.register_class(CreateSimpleShapeOperator)
    bpy.types.Scene.shape_type = bpy.props.EnumProperty(
        items=[('CIRCLE', 'Circle', 'Create a circle'), ('CUBE', 'Cube', 'Create a cube'), ('SPHERE', 'Sphere', 'Create a sphere')],
        name="Shape Type",
        default='CIRCLE'
    )

def unregister():
    bpy.utils.unregister_class(SimpleShapeGeneratorPanel)
    bpy.utils.unregister_class(CreateSimpleShapeOperator)
    del bpy.types.Scene.shape_type

if __name__ == "__main__":
    register()
