from typing import Text, Optional
import os
from flask import Flask, send_from_directory, make_response, request
from flask.cli import ScriptInfo

import table_annotator.img
import table_annotator.io

IMAGE_PATH = "image_path"


def create_app(script_info: Optional[ScriptInfo] = None, image_path: Text = "images"):
    app = Flask(__name__)
    app.config[IMAGE_PATH] = image_path
    app.logger.info(f'Starting server serving images from {image_path}')

    @app.route('/images')
    def list_images():

        files = os.listdir(app.config[IMAGE_PATH])
        allowed_extensions = {".jpeg", ".jpg"}
        relevant_files = [f for f in files
                          if os.path.splitext(f)[1] in allowed_extensions]
        images_with_metadata = []
        for f in relevant_files:
            image = table_annotator.io.read_image(
                os.path.join(app.config[IMAGE_PATH], f))
            width, height = table_annotator.img.get_dimensions(image)
            center = {"x": width//2, "y": height // 2}
            images_with_metadata.append({"src": f"image/{f}", "width": width,
                                         "height": height, "center": center,
                                         "name": f})
        return {"images": images_with_metadata}

    @app.route('/image/<name>')
    def get_image(name):
        return send_from_directory(app.config[IMAGE_PATH], name)

    @app.route('/tables/<image_name>', methods=["POST"])
    def store_tables(image_name):
        image_basename = os.path.basename(image_name)
        if not os.path.isfile(os.path.join(app.config[IMAGE_PATH], image_basename)):
            return make_response({"msg": "The image for which you tried to save "
                                         "table data does not exist."}, 404)

        json_file_name = os.path.splitext(image_basename)[0] + ".json"
        json_file_path = os.path.join(app.config[IMAGE_PATH], json_file_name)
        table_annotator.io.write_json(json_file_path, request.json)

        return {"msg": "okay!"}

    @app.route('/tables/<image_name>', methods=["GET"])
    def get_tables(image_name):
        image_basename = os.path.basename(image_name)
        if not os.path.isfile(os.path.join(app.config[IMAGE_PATH], image_basename)):
            return make_response({"msg": "The image for which you tried to retrieve "
                                         "table data does not exist."}, 404)

        json_file_name = os.path.splitext(image_basename)[0] + ".json"
        json_file_path = os.path.join(app.config[IMAGE_PATH], json_file_name)

        if not os.path.isfile(json_file_path):
            return {"tables": []}

        tables = table_annotator.io.read_json(json_file_path)

        return {"tables": tables}

    return app

