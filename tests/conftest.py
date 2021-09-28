import pytest, json
from brain_atlas_toolkit.graph_tools import Graph

allen_ontology_file = 'static/allen.json'
with open(allen_ontology_file) as json_file:
    allen_ontology_dict = json.load(json_file)

pma_ontology_file = 'static/pma_ontology.json'
with open(pma_ontology_file) as json_file:
    pma_ontology_dict = json.load(json_file)

minimal_ontology_file = 'static/pma_ontology_minimal.json'
with open(minimal_ontology_file) as json_file:
    minimal_ontology_dict = json.load(json_file) 

@pytest.fixture(scope='session') 
def allen_ontology_graph():
	print('----------Setup ontology_graph() ----------')
	ontology_graph = Graph(allen_ontology_dict)
	return ontology_graph

@pytest.fixture(scope='session') 
def pma_ontology_graph():
	print('----------Setup ontology_graph() ----------')
	ontology_graph = Graph(pma_ontology_dict)
	return ontology_graph

@pytest.fixture(scope='session') 
def minimal_ontology_graph():
	print('----------Setup ontology_graph() ----------')
	ontology_graph = Graph(minimal_ontology_dict)
	return ontology_graph