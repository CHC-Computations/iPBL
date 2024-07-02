import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, SKOS

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
        subject = URIRef(subject.strip())  # Strip potential whitespace from subject
        predicate = URIRef(predicate.strip())  # Strip potential whitespace from predicate
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
