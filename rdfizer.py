# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:19:21 2024

@author: patry
"""

import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS
import os

class RDFGraphFactory:
    def __init__(self):
        self.graph = Graph()
        self.namespace_manager()

    def namespace_manager(self):
        SCHEMA = Namespace("http://schema.org/")
        BIBFRAME = Namespace("http://id.loc.gov/ontologies/bibframe/")
        self.graph.bind("schema", SCHEMA)
        self.graph.bind("bibframe", BIBFRAME)
        self.graph.bind("skos", SKOS)

    def create_graph_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                subject = URIRef(row['subject'])
                predicate = URIRef(row['predicate'])
                obj = Literal(row['object'])
                self.graph.add((subject, predicate, obj))

    def save_graph(self, file_path):
        self.graph.serialize(destination=file_path, format='turtle')

class RDFGraphClient:
    def __init__(self, factory):
        self.factory = factory

    def create_and_save_graph(self, csv_file_path, output_file_path):
        self.factory.create_graph_from_csv(csv_file_path)
        self.factory.save_graph(output_file_path)

if __name__ == "__main__":
    csv_file_path = 'example.csv'
    factory = RDFGraphFactory()
    client = RDFGraphClient(factory)
    client.create_and_save_graph(csv_file_path, 'output.ttl')
