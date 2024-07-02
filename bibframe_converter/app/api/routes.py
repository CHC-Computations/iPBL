from flask import request, jsonify
from flask_restful import Resource
import os
from rdf.builder import RDFGraphBuilder
from config import UPLOAD_FOLDER, OUTPUT_FOLDER

class FileUploadAPI(Resource):
    def post(self):
        """Upload CSV file and get RDF output"""
        if 'file' not in request.files:
            return {'error': 'No file part in the request'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No file selected for uploading'}, 400
        format = request.form['format']
        display = 'display' in request.form
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            builder = RDFGraphBuilder()
            builder.add_triples_from_csv(file_path).build()
            output_file_path = os.path.join(OUTPUT_FOLDER, f'output.{format}')
            builder.build().serialize(destination=output_file_path, format=format)
            with open(output_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            response = {'content': content, 'format': format, 'filename': f'output.{format}', 'success': True}
            if not display:
                response.pop('content')
            return jsonify(response)
        return {'error': 'File upload failed'}, 400

def initialize_routes(api):
    api.add_resource(FileUploadAPI, '/api/upload')
