bl_info = {
    "name": "Sculpture Craft 3.0",
    "author": "ut",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new color Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty,FloatVectorProperty
import os

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
        # Conditionally show the import operator button for the "CUSTOM" shape type

        if context.scene.shape_type == 'CUSTOM':

            layout.label(text="Import Custom Shape:")
            layout.operator("import_mesh.stl", text="Import STL", icon='FILE_NEW')
            layout.operator("import_image.to_plane", text="Import Image as Plane", icon='IMAGE_DATA')
            # Custom operator to load a background image
            layout.operator("object.load_background_image", text="Load Background Image", icon='IMAGE_DATA')
            layout.operator("object.load_reference_image", text="Load Reference Image", icon='IMAGE_DATA')
            layout.operator("object.open_camera_background_image", text="Set Camera Background Image", icon='IMAGE_DATA')
            layout.operator("object.import_glb", text="Import GLB", icon='IMPORT')


        if context.scene.shape_type != 'CUSTOM':
            layout.label(text="Shape Color:")
            layout.prop(context.scene.new_shape_operator, "shape_color", text="")

            # Button to create the selected shape
            layout.operator("object.create_simple_shape", text="Create Shape")
            layout.operator("object.change_shape_color", text="Change Shape Color")





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
    scale_factor: FloatProperty(
        name="Scale Factor",
        description="Scale factor for the shape",
        default=1.0,
    )
    cylinder_radius: FloatProperty(
        name="Cylinder Radius",
        description="Radius of the cylinder",
        default=1.0,
    )
    cylinder_height: FloatProperty(
        name="Cylinder Height",
        description="Height of the cylinder",
        default=2.0,
    )
    create_camera: bpy.props.BoolProperty(
        name="Create Camera",
        description="Create a new camera",
        default=False,
    )
    create_light: bpy.props.BoolProperty(
        name="Create Light",
        description="Create a new light",
        default=False,
    )
    light_type: bpy.props.EnumProperty(
        name="Light Type",
        description="Type of light to create",
        items=[('POINT', 'Point', 'Point light source'),
               ('SUN', 'Sun', 'Sunlight'),
               ('SPOT', 'Spot', 'Spotlight'),
               ('AREA', 'Area', 'Area light')],
        default='POINT',
    )
    custom_shape_file: StringProperty(
    name="Background Image File",
    description="Select a background image for the camera",
    subtype='FILE_PATH'
    )



    def draw(self, context):
        layout = self.layout
        shape_type = context.scene.shape_type

        layout.prop(self, "new_shape_name")
        layout.prop(self, "x_coordinate")
        layout.prop(self, "y_coordinate")
        layout.prop(self, "z_coordinate")
        layout.prop(self, "scale_factor")
        layout.prop(self, "create_camera")
        layout.prop(self, "create_light")

        if shape_type == 'CYLINDER':
            layout.prop(self, "cylinder_radius")
            layout.prop(self, "cylinder_height")
            if self.create_light:
                layout.prop(self, "light_type")
        elif shape_type == 'CUSTOM':
            layout.prop(self, "custom_shape_file")
            layout.operator("object.set_camera_background_image", text="Set Camera Background Image", icon='IMAGE_DATA')
        elif self.create_light:
            layout.prop(self, "light_type")

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
        scale_factor = self.scale_factor

        # Validate the shape name
        if not self.validate_name(context, new_name):
            return {'CANCELLED'}

        if shape_type == 'CIRCLE':
            bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1 * scale_factor, location=(x_coord, y_coord, z_coord))
        elif shape_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1 * scale_factor, enter_editmode=False, align='WORLD', location=(x_coord, y_coord, z_coord))
        elif shape_type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1 * scale_factor, location=(x_coord, y_coord, z_coord))
        elif shape_type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=self.cylinder_radius*0.5, depth=self.cylinder_height*scale_factor*0.3 , location=(x_coord, y_coord, z_coord))
        elif shape_type == 'PLANE':
            bpy.ops.mesh.primitive_plane_add(size=1 * scale_factor, enter_editmode=False, align='WORLD', location=(x_coord, y_coord, z_coord))
        elif shape_type == 'TORUS':
            bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(x_coord, y_coord, z_coord))
        elif shape_type == 'GRID':
            bpy.ops.mesh.primitive_grid_add(x_subdivisions=10, y_subdivisions=10, size=1 * scale_factor, enter_editmode=False, align='WORLD', location=(x_coord, y_coord, z_coord))
        elif shape_type == 'MONKEY':
            bpy.ops.mesh.primitive_monkey_add(size=1 * scale_factor, enter_editmode=False, align='WORLD', location=(x_coord, y_coord, z_coord))
        elif shape_type == 'ICOSPHERE':
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1 * scale_factor, location=(x_coord, y_coord, z_coord))

        # Rename the newly created object
        bpy.context.active_object.name = new_name

        active_object = bpy.context.active_object
        active_object.data.materials.clear()
        mat = bpy.data.materials.new(name="Shape_Material")
        active_object.data.materials.append(mat)
        # Access the shape_color property through new_shape_operator
        mat.diffuse_color = context.scene.new_shape_operator.shape_color
        if self.create_camera:
            
            bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(x_coord + 5, y_coord + 5, z_coord + 5))

        if self.create_light:
            if self.light_type == 'POINT':
                bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(x_coord - 5, y_coord - 5, z_coord + 5))
            elif self.light_type == 'SUN':
                bpy.ops.object.light_add(type='SUN', align='WORLD', location=(x_coord - 5, y_coord - 5, z_coord + 5))
            elif self.light_type == 'SPOT':
                bpy.ops.object.light_add(type='SPOT', align='WORLD', location=(x_coord - 5, y_coord - 5, z_coord + 5))
            elif self.light_type == 'AREA':
                bpy.ops.object.light_add(type='AREA', radius=1, align='WORLD', location=(x_coord - 5, y_coord - 5, z_coord + 5))




        self.report({'INFO'}, f'Shape name: {new_name}, Position: ({x_coord}, {y_coord}, {z_coord}), Scale: {scale_factor}')

        return {'FINISHED'}


class ColorProperties(bpy.types.PropertyGroup):
    shape_color: FloatVectorProperty(
        name="Shape Color",
        subtype='COLOR',
        size=4,
        default=(1.0, 0.0, 0.0, 1.0),
        min=0.0,
        max=1.0,
    )
    
class ImportGLBOperator(bpy.types.Operator):
    bl_idname = "object.import_glb"
    bl_label = "Import GLB"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        try:
            bpy.ops.import_scene.gltf(filepath=self.filepath)
        except Exception as e:
            self.report({'ERROR'}, f"Error importing GLB file: {str(e)}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Imported GLB file: {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class LightPropertiesPanel(bpy.types.Panel):
    bl_label = "Light Properties"
    bl_idname = "OBJECT_PT_LightPropertiesPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        for obj in bpy.context.scene.collection.all_objects:
            if obj.type == 'LIGHT':
                layout.label(text="Light Properties for " + obj.name)
                layout.prop(obj.data, "type", text="Light Type")
                layout.prop(obj.data, "color", text="Light Color")
                layout.prop(obj.data, "energy", text="Strength")
class ExportPanel(bpy.types.Panel):
    bl_label = "Export Options"
    bl_idname = "OBJECT_PT_ExportPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Export as .STL button
        layout.operator("export_mesh.stl", text="Export as .STL")

        # Export as .glb button
        layout.operator("export_scene.gltf", text="Export as .glb")

        # Export with custom path, filename, and format
        layout.label(text="Export with Custom Path, Filename, and Format:")
        layout.prop(context.scene, "export_path")
        layout.prop(context.scene, "export_filename")
        layout.prop(context.scene, "export_format")

        # Export button
        layout.operator("export_scene.export_with_options", text="Export")
class ExportWithOptionsOperator(bpy.types.Operator):
    bl_idname = "export_scene.export_with_options"
    bl_label = "Export with Custom Path, Filename, and Format"
    
    def execute(self, context):
        export_path = context.scene.export_path
        export_filename = context.scene.export_filename

        if context.scene.export_format == 'STL':
            bpy.ops.export_mesh.stl(filepath=export_path + export_filename + '.stl')
            self.report({'INFO'}, f'Exported {export_filename}.stl to {export_path}')

        elif context.scene.export_format == 'GLB':
            bpy.ops.export_scene.gltf(filepath=export_path + export_filename + '.glb', export_format='GLB')
            self.report({'INFO'}, f'Exported {export_filename}.glb to {export_path}')

        return {'FINISHED'}
                    
class OpenCameraBackgroundImageOperator(Operator):
    bl_idname = "object.open_camera_background_image"
    bl_label = "Set Camera Background Image"

    filepath: StringProperty(
        subtype='FILE_PATH',
        description="Path to the background image file",
    )

    def execute(self, context):
        camera_object = None
        for obj in bpy.context.scene.collection.all_objects:
            if obj.type == 'CAMERA':
                camera_object = obj
                break

        if camera_object is not None:
            if self.filepath:
                # Clear existing background images
                camera_object.data.background_images.clear()

                # Create a new background image
                bg_image = camera_object.data.background_images.new()
                bg_image.image = bpy.data.images.load(self.filepath)

                # Show the background image in the 3D view for the camera object
                camera_object.data.show_background_images = True

                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "No file selected for the camera background image.")
        else:
            self.report({'ERROR'}, "No camera found in the scene.")

        return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



class ChangeShapeColorOperator(bpy.types.Operator):
    bl_idname = "object.change_shape_color"
    bl_label = "Change Shape Color"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):
        color = context.scene.new_shape_operator.shape_color
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            if obj.type == 'MESH':
                if obj.data.materials:
                    obj.data.materials[0].diffuse_color = color

        self.report({'INFO'}, f'Changed color of {len(selected_objects)} selected objects to {color}')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_PT_SimpleShapeGeneratorPanel)
    bpy.utils.register_class(CreateSimpleShapeOperator)
    bpy.utils.register_class(OpenCameraBackgroundImageOperator)
    bpy.utils.register_class(ChangeShapeColorOperator)
    bpy.utils.register_class(ImportGLBOperator)
    bpy.utils.register_class(LightPropertiesPanel)


    bpy.types.Scene.shape_type = bpy.props.EnumProperty(
        items=[
            ('CIRCLE', 'Circle', 'Create a circle'),
            ('CUBE', 'Cube', 'Create a cube'),
            ('SPHERE', 'Sphere', 'Create a sphere'),
            ('ICOSPHERE', 'Icosphere', 'Create an Icosphere'),
            ('CYLINDER', 'Cylinder', 'Create a cylinder'),
            ('CONE', 'Cone', 'Create a cone'),
            ('PLANE', 'Plane', 'Create a plane'),
            ('TORUS', 'Torus', 'Create a torus'),
            ('GRID', 'Grid', 'Create a grid'),
            ('MONKEY', 'Monkey', 'Create a monkey (Suzanne)'),
            ('CUSTOM', 'Custom', 'Import a custom shape')],
        name="Shape Type",
        default='CIRCLE',
    )

    bpy.utils.register_class(ColorProperties)
    bpy.types.Scene.new_shape_operator = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.export_path = bpy.props.StringProperty(name="Export Path", default="", subtype='FILE_PATH')
    bpy.types.Scene.export_filename = bpy.props.StringProperty(name="Export Filename", default="custom_export")
    bpy.types.Scene.export_format = bpy.props.EnumProperty(
        name="Export Format",
        items=[
            ('STL', 'STL', 'Export as .STL'),
            ('GLB', 'GLB', 'Export as .glb')
        ],
        default='STL'
    )

    bpy.utils.register_class(ExportPanel)
    bpy.utils.register_class(ExportWithOptionsOperator)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_SimpleShapeGeneratorPanel)
    bpy.utils.unregister_class(CreateSimpleShapeOperator)
    bpy.utils.unregister_class(OpenCameraBackgroundImageOperator)
    bpy.utils.unregister_class(ChangeShapeColorOperator)
    bpy.utils.unregister_class(ImportGLBOperator)
    bpy.utils.register_class(LightPropertiesPanel)
    bpy.utils.unregister_class(ColorProperties)

    del bpy.types.Scene.shape_type
    del bpy.types.Scene.new_shape_name
    del bpy.types.Scene.custom_shape_file
    bpy.utils.unregister_class(ExportPanel)
    bpy.utils.unregister_class(ExportWithOptionsOperator)  # Unregister the custom export operator
    del bpy.types.Scene.export_path
    del bpy.types.Scene.export_filename
    del bpy.types.Scene.export_format

if __name__ == "__main__":
    register()
