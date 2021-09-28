import pytest, json
import graphviz
from brain_atlas_toolkit.graph_tools import Node, Graph

allen_ontology_file = 'static/allen.json'
with open(allen_ontology_file) as json_file:
    allen_ontology_dict = json.load(json_file)

pma_ontology_file = 'static/pma_ontology.json'
with open(pma_ontology_file) as json_file:
    pma_ontology_dict = json.load(json_file)

minimal_ontology_file = 'static/pma_ontology_minimal.json'
with open(minimal_ontology_file) as json_file:
    minimal_ontology_dict = json.load(json_file)    

def test_create_node():
	node = Node('Brain region')
	assert node.name == "Brain region"
	assert repr(node) == "Brain region"

def test_create_graph_allen():
	allen_ontology_graph = Graph(allen_ontology_dict)
	assert len(allen_ontology_graph.graph) > 0

def test_create_graph_pma():
	pma_ontology_graph = Graph(pma_ontology_dict)
	assert len(pma_ontology_graph.graph) > 0

def test_create_graph_miniaml():
	minimal_ontology_graph = Graph(minimal_ontology_dict)
	assert len(minimal_ontology_graph.graph) > 0

def test_get_progeny_allen(allen_ontology_graph):
	progeny_cbn = allen_ontology_graph.get_progeny('Cerebellar nuclei')
	assert progeny_cbn == \
		['Fastigial nucleus', 'Interposed nucleus',
		 'Dentate nucleus', 'Vestibulocerebellar nucleus']
	progeny_fpct = allen_ontology_graph.get_progeny('Frontal pole, cerebral cortex')
	assert progeny_fpct == \
		['Frontal pole, layer 1',
		 'Frontal pole, layer 2/3',
		 'Frontal pole, layer 5',
		 'Frontal pole, layer 6a',
		 'Frontal pole, layer 6b']
	progeny_MO_onelevel = allen_ontology_graph.get_progeny('Somatomotor areas',stoplevel=1)
	assert progeny_MO_onelevel == [
		'Somatomotor areas, Layer 1',
		'Somatomotor areas, Layer 2/3',
		'Somatomotor areas, Layer 5',
		'Somatomotor areas, Layer 6a',
		'Somatomotor areas, Layer 6b',
		'Primary motor area',
		'Secondary motor area']

def test_get_progeny_pma(pma_ontology_graph):
	progeny_cbn = pma_ontology_graph.get_progeny('Cerebellar nuclei')
	print(progeny_cbn)
	assert sorted(progeny_cbn) == \
		sorted(['Fastigial nucleus', 'Interposed nucleus',
		 'Dentate nucleus', 'Vestibulocerebellar nucleus'])
	progeny_fpct = pma_ontology_graph.get_progeny('Frontal pole, cerebral cortex')
	assert sorted(progeny_fpct) == \
		sorted(['Frontal pole, layer 1',
		 'Frontal pole, layer 2/3',
		 'Frontal pole, layer 5',
		 'Frontal pole, layer 6a',
		 'Frontal pole, layer 6b'])

def test_get_progeny_minimal(minimal_ontology_graph):
	progeny_cbn = minimal_ontology_graph.get_progeny('Cerebellar nuclei')
	print(progeny_cbn)
	assert sorted(progeny_cbn) == \
		sorted(['Fastigial nucleus', 'Interposed nucleus',
		 'Dentate nucleus', 'Vestibulocerebellar nucleus'])
	progeny_fpct = minimal_ontology_graph.get_progeny('Frontal pole, cerebral cortex')
	assert sorted(progeny_fpct) == \
		sorted(['Frontal pole, layer 1',
		 'Frontal pole, layer 2/3',
		 'Frontal pole, layer 5',
		 'Frontal pole, layer 6a',
		 'Frontal pole, layer 6b'])

def test_get_parent_allen(allen_ontology_graph):
	parent_cbn = allen_ontology_graph.get_parent('Cerebellar nuclei')
	assert parent_cbn == 'Cerebellum'
	parent_fpct = allen_ontology_graph.get_parent('Frontal pole, cerebral cortex')
	assert parent_fpct == 'Isocortex'
	parent_root = allen_ontology_graph.get_parent('root')
	assert parent_root == None

def test_get_parent_pma(pma_ontology_graph):
	parent_cbn = pma_ontology_graph.get_parent('Cerebellar nuclei')
	assert parent_cbn == 'Cerebellum'
	parent_fpct = pma_ontology_graph.get_parent('Frontal pole, cerebral cortex')
	assert parent_fpct == 'Isocortex'
	parent_root = pma_ontology_graph.get_parent('root')
	assert parent_root == None

def test_get_parent_minimal(minimal_ontology_graph):
	parent_cbn = minimal_ontology_graph.get_parent('Cerebellar nuclei')
	assert parent_cbn == 'Cerebellum'
	parent_fpct = minimal_ontology_graph.get_parent('Frontal pole, cerebral cortex')
	assert parent_fpct == 'Isocortex'
	parent_root = minimal_ontology_graph.get_parent('root')
	assert parent_root == None

def test_get_progenitors_allen(allen_ontology_graph):
	progenitors_cbn = allen_ontology_graph.get_progenitors('Cerebellar nuclei')
	assert progenitors_cbn == ['Cerebellum', 'Basic cell groups and regions', 'root']
	progenitors_fpct = allen_ontology_graph.get_progenitors('Frontal pole, cerebral cortex')
	assert progenitors_fpct == ['Isocortex',
	 'Cortical plate',
	 'Cerebral cortex',
	 'Cerebrum',
	 'Basic cell groups and regions',
	 'root']
	progenitors_root = allen_ontology_graph.get_progenitors('root')
	assert progenitors_root == []

def test_get_progenitors_pma(pma_ontology_graph):
	progenitors_cbn = pma_ontology_graph.get_progenitors('Cerebellar nuclei')
	assert progenitors_cbn == ['Cerebellum', 'Basic cell groups and regions', 'root']
	progenitors_fpct = pma_ontology_graph.get_progenitors('Frontal pole, cerebral cortex')
	assert progenitors_fpct == ['Isocortex',
	 'Cortical plate',
	 'Cerebral cortex',
	 'Cerebrum',
	 'Basic cell groups and regions',
	 'root']
	progenitors_root = pma_ontology_graph.get_progenitors('root')
	assert progenitors_root == []

def test_get_progenitors_minimal(minimal_ontology_graph):
	progenitors_cbn = minimal_ontology_graph.get_progenitors('Cerebellar nuclei')
	assert progenitors_cbn == ['Cerebellum', 'Basic cell groups and regions', 'root']
	progenitors_fpct = minimal_ontology_graph.get_progenitors('Frontal pole, cerebral cortex')
	assert progenitors_fpct == ['Isocortex',
	 'Cortical plate',
	 'Cerebral cortex',
	 'Cerebrum',
	 'Basic cell groups and regions',
	 'root']
	progenitors_root = minimal_ontology_graph.get_progenitors('root')
	assert progenitors_root == []

def test_get_id_allen(allen_ontology_graph):
	id_cbn = allen_ontology_graph.get_id('Cerebellar nuclei')
	assert id_cbn == 519
	id_fpct = allen_ontology_graph.get_id('Frontal pole, cerebral cortex')
	assert id_fpct == 184

def test_get_id_pma(pma_ontology_graph):
	id_cbn = pma_ontology_graph.get_id('Cerebellar nuclei')
	assert id_cbn == 519
	id_fpct = pma_ontology_graph.get_id('Frontal pole, cerebral cortex')
	assert id_fpct == 184

def test_get_id_minimal(minimal_ontology_graph):
	id_cbn = minimal_ontology_graph.get_id('Cerebellar nuclei')
	assert id_cbn == 519
	id_fpct = minimal_ontology_graph.get_id('Frontal pole, cerebral cortex')
	assert id_fpct == 184

def test_get_acronym_allen(allen_ontology_graph):
	acronym_cbn = allen_ontology_graph.get_acronym('Cerebellar nuclei')
	assert acronym_cbn == 'CBN'
	acronym_fpct = allen_ontology_graph.get_acronym('Frontal pole, cerebral cortex')
	assert acronym_fpct == 'FRP'

def test_get_acronym_pma(pma_ontology_graph):
	acronym_cbn = pma_ontology_graph.get_acronym('Cerebellar nuclei')
	assert acronym_cbn == 'CBN'
	acronym_fpct = pma_ontology_graph.get_acronym('Frontal pole, cerebral cortex')
	assert acronym_fpct == 'FRP'

def test_get_acronym_minimal(minimal_ontology_graph):
	acronym_cbn = minimal_ontology_graph.get_acronym('Cerebellar nuclei')
	assert acronym_cbn == None
	acronym_fpct = minimal_ontology_graph.get_acronym('Frontal pole, cerebral cortex')
	assert acronym_fpct == None

def test_lookup_region_name_by_id_allen(allen_ontology_graph,capfd):
	name_cbn = allen_ontology_graph.lookup_region_name_by_id(519)
	assert name_cbn == 'Cerebellar nuclei'
	name_fpct = allen_ontology_graph.lookup_region_name_by_id(184)
	assert name_fpct == 'Frontal pole, cerebral cortex'
	name_garbage = allen_ontology_graph.lookup_region_name_by_id(-99)
	out,err = capfd.readouterr()
	assert out == "No region name found with id: -99\n"
	assert name_garbage == None

def test_lookup_region_name_by_id_pma(pma_ontology_graph,capfd):
	name_cbn = pma_ontology_graph.lookup_region_name_by_id(519)
	assert name_cbn == 'Cerebellar nuclei'
	name_fpct = pma_ontology_graph.lookup_region_name_by_id(184)
	assert name_fpct == 'Frontal pole, cerebral cortex'
	name_garbage = pma_ontology_graph.lookup_region_name_by_id(-99)
	out,err = capfd.readouterr()
	assert out == "No region name found with id: -99\n"
	assert name_garbage == None

def test_lookup_region_name_by_id_minimal(minimal_ontology_graph,capfd):
	name_cbn = minimal_ontology_graph.lookup_region_name_by_id(519)
	assert name_cbn == 'Cerebellar nuclei'
	name_fpct = minimal_ontology_graph.lookup_region_name_by_id(184)
	assert name_fpct == 'Frontal pole, cerebral cortex'
	name_garbage = minimal_ontology_graph.lookup_region_name_by_id(-99)
	out,err = capfd.readouterr()
	assert out == "No region name found with id: -99\n"
	assert name_garbage == None

def test_print_branch_allen(allen_ontology_graph,capfd):
	branch_cbn = allen_ontology_graph.print_branch('Cerebellar nuclei',stoplevel=-1)
	out,err = capfd.readouterr()
	assert out == (
		' 0 Cerebellar nuclei\n\t 1 Fastigial nucleus\n\t'
		' 1 Interposed nucleus\n\t 1 Dentate nucleus\n\t 1'
		' Vestibulocerebellar nucleus\n'
		)
	branch_cbn_nostoplevel = allen_ontology_graph.print_branch('Cerebellar nuclei')
	out,err = capfd.readouterr()
	assert out == (
		' 0 Cerebellar nuclei\n\t 1 Fastigial nucleus\n\t'
		' 1 Interposed nucleus\n\t 1 Dentate nucleus\n\t'
 		' 1 Vestibulocerebellar nucleus\n'
 		)
	branch_root_1level = allen_ontology_graph.print_branch('root',stoplevel=1)
	out,err = capfd.readouterr()
	assert out == (
		' 0 root\n\t 1 Basic cell groups and regions\n\t'
		' 1 fiber tracts\n\t 1 ventricular systems\n\t'
		' 1 grooves\n\t 1 retina\n'
		)

def test_visualize_graph_allen(allen_ontology_graph):
	digraph_cbn = allen_ontology_graph.visualize_graph('Cerebellar nuclei',stoplevel=-1)
	assert '\t"Cerebellar nuclei" -> "Fastigial nucleus"' in digraph_cbn.source
	assert type(digraph_cbn) == graphviz.dot.Digraph
	digraph_root_1level = allen_ontology_graph.visualize_graph('root',stoplevel=1)
	assert digraph_root_1level.source == (
		'digraph {\n\troot\n\troot -> "Basic cell groups and regions"\n\t'
		'root -> "fiber tracts"\n\troot -> "ventricular systems"\n\t'
		'root -> grooves\n\troot -> retina\n}'
		)

def test_make_html_ontology_allen(allen_ontology_graph):
	html_str_ontology = allen_ontology_graph.make_html_ontology()
	assert len(html_str_ontology) == 69573
	assert "<li>0 root </li>" in html_str_ontology
	assert "<li>1 Basic cell groups and regions </li>" in html_str_ontology
	assert "<li>2 Cerebrum </li>" in html_str_ontology
	assert "<li>5 Hypothalamic medial zone </li>" in html_str_ontology
