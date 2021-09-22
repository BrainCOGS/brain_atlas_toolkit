import pytest, json
import graphviz
from brain_atlas_toolkit.graph_tools import Node, Graph

ontology_file = 'static/allen.json'
with open(ontology_file) as json_file:
    ontology_dict = json.load(json_file)

def test_create_node():
	node = Node('Brain region')
	assert node.name == "Brain region"
	assert repr(node) == "Brain region"

def test_create_graph():
	ontology_graph = Graph(ontology_dict)
	assert len(ontology_graph.graph) > 0

def test_get_progeny(ontology_graph):
	progeny_cbn = ontology_graph.get_progeny('Cerebellar nuclei')
	assert progeny_cbn == \
		['Fastigial nucleus', 'Interposed nucleus',
		 'Dentate nucleus', 'Vestibulocerebellar nucleus']
	progeny_fpct = ontology_graph.get_progeny('Frontal pole, cerebral cortex')
	assert progeny_fpct == \
		['Frontal pole, layer 1',
		 'Frontal pole, layer 2/3',
		 'Frontal pole, layer 5',
		 'Frontal pole, layer 6a',
		 'Frontal pole, layer 6b']

def test_get_parent(ontology_graph):
	parent_cbn = ontology_graph.get_parent('Cerebellar nuclei')
	assert parent_cbn == 'Cerebellum'
	parent_fpct = ontology_graph.get_parent('Frontal pole, cerebral cortex')
	assert parent_fpct == 'Isocortex'
	parent_root = ontology_graph.get_parent('root')
	assert parent_root == None

def test_get_id(ontology_graph):
	id_cbn = ontology_graph.get_id('Cerebellar nuclei')
	assert id_cbn == 519
	id_fpct = ontology_graph.get_id('Frontal pole, cerebral cortex')
	assert id_fpct == 184

def test_get_acronym(ontology_graph):
	acronym_cbn = ontology_graph.get_acronym('Cerebellar nuclei')
	assert acronym_cbn == 'CBN'
	acronym_fpct = ontology_graph.get_acronym('Frontal pole, cerebral cortex')
	assert acronym_fpct == 'FRP'

def test_lookup_region_name_by_id(ontology_graph,capfd):
	name_cbn = ontology_graph.lookup_region_name_by_id(519)
	assert name_cbn == 'Cerebellar nuclei'
	name_fpct = ontology_graph.lookup_region_name_by_id(184)
	assert name_fpct == 'Frontal pole, cerebral cortex'
	name_garbage = ontology_graph.lookup_region_name_by_id(-99)
	out,err = capfd.readouterr()
	assert out == "No region name found with id: -99\n"
	assert name_garbage == None

def test_print_branch(ontology_graph,capfd):
	branch_cbn = ontology_graph.print_branch('Cerebellar nuclei',stoplevel=-1)
	out,err = capfd.readouterr()
	assert out == (
		' 0 Cerebellar nuclei\n\t 1 Fastigial nucleus\n\t'
		' 1 Interposed nucleus\n\t 1 Dentate nucleus\n\t 1'
		' Vestibulocerebellar nucleus\n'
		)
	branch_cbn_nostoplevel = ontology_graph.print_branch('Cerebellar nuclei')
	out,err = capfd.readouterr()
	assert out == (
		' 0 Cerebellar nuclei\n\t 1 Fastigial nucleus\n\t'
		' 1 Interposed nucleus\n\t 1 Dentate nucleus\n\t'
 		' 1 Vestibulocerebellar nucleus\n'
 		)
	branch_root_1level = ontology_graph.print_branch('root',stoplevel=1)
	out,err = capfd.readouterr()
	assert out == (
		' 0 root\n\t 1 Basic cell groups and regions\n\t'
		' 1 fiber tracts\n\t 1 ventricular systems\n\t'
		' 1 grooves\n\t 1 retina\n'
		)

def test_visualize_graph(ontology_graph):
	digraph_cbn = ontology_graph.visualize_graph('Cerebellar nuclei',stoplevel=-1)
	assert '\t"Cerebellar nuclei" -> "Fastigial nucleus"' in digraph_cbn.source
	assert type(digraph_cbn) == graphviz.dot.Digraph
	digraph_root_1level = ontology_graph.visualize_graph('root',stoplevel=1)
	assert digraph_root_1level.source == (
		'digraph {\n\troot\n\troot -> "Basic cell groups and regions"\n\t'
		'root -> "fiber tracts"\n\troot -> "ventricular systems"\n\t'
		'root -> grooves\n\troot -> retina\n}'
		)

def test_make_html_ontology(ontology_graph):
	html_str_ontology = ontology_graph.make_html_ontology()
	assert len(html_str_ontology) == 69573
	assert "<li>0 root </li>" in html_str_ontology
	assert "<li>1 Basic cell groups and regions </li>" in html_str_ontology
	assert "<li>2 Cerebrum </li>" in html_str_ontology
	assert "<li>5 Hypothalamic medial zone </li>" in html_str_ontology



