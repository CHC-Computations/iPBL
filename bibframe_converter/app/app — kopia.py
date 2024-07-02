import csv
import os
from flask import Flask, request, redirect, url_for, send_file, render_template, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS

app = Flask(__name__)
api = Api(app)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

class RDFGraphBuilder:
    def __init__(self):
        self.graph = Graph()
        self.namespace_manager()

    def namespace_manager(self):
        SCHEMA = Namespace("http://schema.org/")
        BIBFRAME = Namespace("http://id.loc.gov/ontologies/bibframe/")
        self.graph.bind("schema", SCHEMA)
        self.graph.bind("bf", BIBFRAME)
        self.graph.bind("skos", SKOS)
        return self

    def add_triple(self, subject, predicate, obj):
        subject = URIRef(subject)
        predicate = URIRef(predicate)
        if obj.startswith("http://") or obj.startswith("https://"):
            obj = URIRef(obj)
        else:
            obj = Literal(obj)
        self.graph.add((subject, predicate, obj))
        return self

    def add_triples_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                subject = row['subject']
                rdf_type = row['type']
                self.add_triple(subject, RDF.type, rdf_type)
                self.add_triple(subject, row['predicate'], row['object'])
        return self

    def build(self):
        return self.graph

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    format = request.form['format']
    display = 'display' in request.form
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        builder = RDFGraphBuilder()
        builder.add_triples_from_csv(file_path).build()
        output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f'output.{format}')
        builder.build().serialize(destination=output_file_path, format=format)
        with open(output_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        response = {'content': content, 'format': format, 'filename': f'output.{format}', 'success': True}
        if not display:
            response.pop('content')
        return jsonify(response)
    return jsonify({'error': 'File upload failed'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

@app.route('/image')
def serve_image():
    return send_file('/mnt/data/image.png', mimetype='image/png')

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
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            builder = RDFGraphBuilder()
            builder.add_triples_from_csv(file_path).build()
            output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f'output.{format}')
            builder.build().serialize(destination=output_file_path, format=format)
            with open(output_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            response = {'content': content, 'format': format, 'filename': f'output.{format}', 'success': True}
            if not display:
                response.pop('content')
            return jsonify(response)
        return {'error': 'File upload failed'}, 400

api.add_resource(FileUploadAPI, '/api/upload')

### Swagger UI setup ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CSV to RDF API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True)
