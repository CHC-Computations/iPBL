# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:33:57 2024

@author: patry
"""

import csv
import os
from flask import Flask, request, redirect, url_for, send_file, render_template
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS

app = Flask(__name__)
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
        self.graph.bind("bibframe", BIBFRAME)
        self.graph.bind("skos", SKOS)
        return self

    def add_triple(self, subject, predicate, obj):
        subject = URIRef(subject)
        predicate = URIRef(predicate)
        obj = Literal(obj)
        self.graph.add((subject, predicate, obj))
        return self

    def add_triples_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                self.add_triple(row['subject'], row['predicate'], row['object'])
        return self

    def build(self):
        return self.graph

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        builder = RDFGraphBuilder()
        builder.add_triples_from_csv(file_path).build()
        output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.ttl')
        builder.build().serialize(destination=output_file_path, format='turtle')
        return redirect(url_for('download_file', filename='output.ttl'))
    return redirect(request.url)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
