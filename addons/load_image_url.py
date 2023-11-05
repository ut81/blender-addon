bl_info = {
    "name": "load image with url",
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
import os
import uuid
class ImageLoaderPanel(bpy.types.Panel):
    bl_label = "Image Loader"
    bl_idname = "PT_ImageLoaderPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Load an image from file or URL:")

        # File Path
        layout.prop(context.scene, "image_path", text="File Path")

        # Image URL
        layout.prop(context.scene, "image_url", text="Image URL")

        # Load Image Button
        layout.operator("image.load_from_file", text="Load Image from File")
        layout.operator("image.load_from_url", text="Load Image from URL")

class LoadImageFromFileOperator(bpy.types.Operator):
    bl_idname = "image.load_from_file"
    bl_label = "Load Image from File"

    def execute(self, context):
        file_path = context.scene.image_path
        bpy.ops.object.load_background_image(filepath=file_path)
        return {'FINISHED'}
class LoadImageFromURLOperator(bpy.types.Operator):
    bl_idname = "image.load_from_url"
    bl_label = "Load Image from URL"
    
    # Add a new property to store the user-defined save path
    save_path: bpy.props.StringProperty(name="Save Path", subtype='FILE_PATH')

    def execute(self, context):
        import requests

        image_url = context.scene.image_url
        response = requests.get(image_url)

        if response.status_code == 200:
            image_data = response.content

            # Use the user-defined save path or a default path
            unique_filename = f"{str(uuid.uuid4())}.jpg"
            save_path = self.save_path or os.path.join(os.path.expanduser('~'),unique_filename)

            # Ensure the directory exists before saving the image
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Save the downloaded image to the specified path
            with open(save_path, 'wb') as f:
                f.write(image_data)

            print(f"Image downloaded and saved to {save_path}")

            # Open the downloaded image in Blender's image editor
            bpy.ops.object.load_background_image(filepath=save_path)
        else:
            self.report({'ERROR'}, f"Failed to download image from URL (Status code: {response.status_code})")

        return {'FINISHED'}


def register():
    bpy.utils.register_class(ImageLoaderPanel)
    bpy.utils.register_class(LoadImageFromFileOperator)
    bpy.utils.register_class(LoadImageFromURLOperator)
    bpy.types.Scene.image_path = bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')
    bpy.types.Scene.image_url = bpy.props.StringProperty(name="Image URL")

def unregister():
    bpy.utils.unregister_class(ImageLoaderPanel)
    bpy.utils.unregister_class(LoadImageFromFileOperator)
    bpy.utils.unregister_class(LoadImageFromURLOperator)
    del bpy.types.Scene.image_path
    del bpy.types.Scene.image_url

if __name__ == "__main__":
    register()
