bl_info = {
    "name": "Place Cube Add on",
    "author": "utsav",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Add Object",
}





import bpy

class OBJECT_OT_PlaceCube(bpy.types.Operator):
    bl_idname = "object.place_cube"
    bl_label = "Place Cube at Coordinates"
    bl_options = {'REGISTER', 'UNDO'}

# Get the active scene
    
# Now you can work with the 'scene' object

    object_name: bpy.props.EnumProperty(
        items=[(obj.name, obj.name, obj.name) for obj in bpy.context.scene.objects if obj.type == 'MESH'],
        name="Select Object"
    )

    x_coord: bpy.props.FloatProperty(name="X Coordinate")
    y_coord: bpy.props.FloatProperty(name="Y Coordinate")
    z_coord: bpy.props.FloatProperty(name="Z Coordinate")

    def execute(self, context):
        # Create a new cube
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(self.x_coord, self.y_coord, self.z_coord))
        new_cube = bpy.context.active_object

        # Parent the cube to the selected object (if an object is selected)
        selected_obj = bpy.data.objects.get(self.object_name)
        if selected_obj:
            new_cube.select_set(True)
            bpy.context.view_layer.objects.active = selected_obj
            bpy.ops.object.parent_set(type='OBJECT')

        return {'FINISHED'}

class OBJECT_PT_PlaceCubePanel(bpy.types.Panel):
    bl_label = "Place Cube at Coordinates"
    bl_idname = "OBJECT_PT_place_cube"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Operator for placing the cube
        operator = layout.operator("object.place_cube")

        # Dropdown to select an object
        layout.prop(operator, "object_name")

        # Input fields for coordinates
        layout.prop(operator, "x_coord")
        layout.prop(operator, "y_coord")
        layout.prop(operator, "z_coord")

def register():
    bpy.utils.register_class(OBJECT_OT_PlaceCube)
    bpy.utils.register_class(OBJECT_PT_PlaceCubePanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_PlaceCube)
    bpy.utils.unregister_class(OBJECT_PT_PlaceCubePanel)

if __name__ == "__main__":
    register()
