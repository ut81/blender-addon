import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty, FloatProperty

class OBJECT_PT_SimpleShapeGeneratorPanel(Panel):
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

        # Sliders for X, Y, and Z coordinates
        layout.prop(context.scene, "x_coordinate")
        layout.prop(context.scene, "y_coordinate")
        layout.prop(context.scene, "z_coordinate")

        # Simple 2D preview
        layout.label(text="Preview:")
        col = layout.column()
        col.prop(context.scene, "preview_scale", slider=True)
        col = layout.column(align=True)
        col.operator("object.update_shape_preview", text="Update Preview")
        col.operator("object.delete_shape_previews", text="Delete Preview")
        col.operator("object.create_shape_from_preview", text="Create Shape from Preview")

        # Button to create the selected shape
        layout.operator("object.create_simple_shape", text="Create Shape")
class UpdateShapePreviewOperator(Operator):
    bl_idname = "object.update_shape_preview"
    bl_label = "Update Shape Preview"

    def execute(self, context):
        shape_type = context.scene.shape_type
        x_coord = context.scene.x_coordinate
        y_coord = context.scene.y_coordinate
        scale = context.scene.preview_scale

       

        # Create a basic 2D preview of the shape
        if shape_type == 'CIRCLE':
            bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1 * scale, location=(x_coord, y_coord, 0))
        elif shape_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1 * scale, enter_editmode=False, align='WORLD', location=(x_coord, y_coord, 0))
        elif shape_type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1 * scale, location=(x_coord, y_coord, 0))

        # Rename the created object to the specified name pattern
        preview_object = bpy.context.active_object
        new_name = context.scene.new_shape_name + "__preview"
        preview_object.name = new_name

        return {'FINISHED'}

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

    def validate_name(self, context, new_name):
        # Check if the name is valid (e.g., does not contain special characters)
        if not new_name.isalnum():
            self.report({'ERROR'}, "Shape name contains invalid characters. Please use letters and numbers only.")
            return False

        # Check if the name already exists in the scene
        if new_name in bpy.data.objects:
            self.report({'ERROR'}, f"A shape with the name '{new_name}' already exists. Please choose a different name.")
            return False

        return True
    def invoke(self, context, event):
        # Open the custom modal dialog to get the shape name and coordinates
        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):
        shape_type = context.scene.shape_type
        new_name = self.new_shape_name
        x_coord = self.x_coordinate
        y_coord = self.y_coordinate
        z_coord = self.z_coordinate
    
      # Validate the shape name
        if not self.validate_name(context, new_name):
            return {'CANCELLED'}
            
        if shape_type == 'CIRCLE':
            
            bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1 * context.scene.preview_scale, location=(x_coord, y_coord, z_coord))
        elif shape_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1 * context.scene.preview_scale, enter_editmode=False, align='WORLD', location=(x_coord, y_coord, z_coord))
        elif shape_type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1 * context.scene.preview_scale, location=(x_coord, y_coord, z_coord))

        
       # Rename the newly created object
        new_object = bpy.context.active_object
        new_object.name = new_name

        # Select all objects except the newly created one
        bpy.ops.object.select_all(action='SELECT')
        new_object.select_set(False)

        # Remove the selected objects
        bpy.ops.object.delete()

        self.report({'INFO'}, f'Shape name: {new_name}, Position: ({x_coord}, {y_coord}, {z_coord})')

        return {'FINISHED'}


class DeleteShapePreviewsOperator(Operator):
    bl_idname = "object.delete_shape_previews"
    bl_label = "Delete Shape Previews"

    def execute(self, context):
        # Clear all objects with names ending in "__preview"
        for obj in bpy.data.objects:
            if obj.name.startswith("__preview"):
                bpy.data.objects.remove(obj)

        return {'FINISHED'}



class CreateShapeFromPreviewOperator(Operator):
    bl_idname = "object.create_shape_from_preview"
    bl_label = "Create Shape from Preview"

    new_shape_name: StringProperty(
        name="New Shape Name",
        description="Enter a name for the new shape",
        default="",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):
        new_name = self.new_shape_name

        if not new_name:
            self.report({'ERROR'}, "Please enter a name for the new shape.")
            return {'CANCELLED'}

        selected_object = bpy.context.active_object

        if selected_object and selected_object.name.startswith("__preview"):
            # Duplicate the selected preview object
            new_object = selected_object.copy()
            new_object.data = selected_object.data.copy()
            bpy.context.collection.objects.link(new_object)
            new_object.name = new_name

            # Select and delete all objects with names ending in "__preview"
            for obj in bpy.data.objects:
                if obj.name.endswith("__preview"):
                    bpy.data.objects.remove(obj)

            self.report({'INFO'}, f"Shape '{new_name}' created.")
        else:
            self.report({'ERROR'}, "No preview object selected.")

        return {'FINISHED'}




def register():
    bpy.utils.register_class(OBJECT_PT_SimpleShapeGeneratorPanel)
    bpy.utils.register_class(UpdateShapePreviewOperator)
    bpy.utils.register_class(CreateSimpleShapeOperator)
    bpy.utils.register_class(DeleteShapePreviewsOperator)
    bpy.utils.register_class(CreateShapeFromPreviewOperator)

    bpy.types.Scene.shape_type = bpy.props.EnumProperty(
        items=[('CIRCLE', 'Circle', 'Create a circle'), ('CUBE', 'Cube', 'Create a cube'), ('SPHERE', 'Sphere', 'Create a sphere')],
        name="Shape Type",
        default='CIRCLE'
    )
    bpy.types.Scene.new_shape_name = bpy.props.StringProperty()
    bpy.types.Scene.preview_scale = FloatProperty(name="Preview Scale", default=1, min=0.1, max=10)
    bpy.types.Scene.x_coordinate = FloatProperty(name="X Coordinate", default=0)
    bpy.types.Scene.y_coordinate = FloatProperty(name="Y Coordinate", default=0)
    bpy.types.Scene.z_coordinate = FloatProperty(name="Z Coordinate", default=0)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_SimpleShapeGeneratorPanel)
    bpy.utils.unregister_class(UpdateShapePreviewOperator)
    bpy.utils.unregister_class(CreateSimpleShapeOperator)
    del bpy.types.Scene.shape_type
    del bpy.types.Scene.new_shape_name
    del bpy.types.Scene.preview_scale
    del bpy.types.Scene.x_coordinate
    del bpy.types.Scene.y_coordinate
    del bpy.types.Scene.z_coordinate
if __name__ == "__main__":
    register()
