from flask import Flask, render_template, send_file, request, jsonify, url_for
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
import os
from config import UPLOAD_FOLDER, OUTPUT_FOLDER
from rdf.builder import RDFGraphBuilder

app = Flask(__name__)
api = Api(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

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

# Initialize routes
from api.routes import initialize_routes
initialize_routes(api)

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
