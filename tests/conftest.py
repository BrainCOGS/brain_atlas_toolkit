import pytest, json
from brain_atlas_toolkit.graph_tools import Graph

ontology_file = 'static/allen.json'
with open(ontology_file) as json_file:
    ontology_dict = json.load(json_file)

@pytest.fixture(scope='session') 
def ontology_graph():
	print('----------Setup ontology_graph() ----------')
	ontology_graph = Graph(ontology_dict)
	return ontology_graph

