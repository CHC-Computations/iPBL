import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS
import os

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

class RDFGraphClient:
    def __init__(self, builder):
        self.builder = builder

    def create_and_save_graph(self, csv_file_path, output_file_path):
        graph = self.builder.add_triples_from_csv(csv_file_path).build()
        graph.serialize(destination=output_file_path, format='turtle')

if __name__ == "__main__":
    
    csv_file_path = 'example.csv'
    builder = RDFGraphBuilder()
    client = RDFGraphClient(builder)
    client.create_and_save_graph(csv_file_path, 'output.ttl')


