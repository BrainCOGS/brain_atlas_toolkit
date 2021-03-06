import graphviz

class Node():
    """ The elements in the graph """
    def __init__(self,name):
        self.name = name
        self.parent = None
        self.id = None
        self.acronym = None
        self.children = [] # list of Node objects
        self.level = None
    def __repr__(self):
        return str(self.name)
    
class Graph():
    """ The ontology graph """
    def __init__(self,ontology_dict):
        self.html_str = ''
        self.level = 0
        self.last_checked_nodename = None
        self.ontology_dict = ontology_dict 
        self.graph = {}
        self._make_graph(self.ontology_dict) # fills out self.graph which contains the Node relationships
        
    def _make_graph(self,dic):
        name = dic.get('name')
        if name not in self.graph:
            node = Node(name)
            node.id = dic.get('id')
            node.acronym = dic.get('acronym')
            self.graph[name] = node
        else:
            node = self.graph[name]
        if name == 'root':
            node.level = 0
        children = dic.get('children')
        self.level += 1
        for child in children: # child is a dict
            child_name = child.get('name')
            child_node = Node(child_name)
            child_node.parent = node
            child_node.id = child.get('id')
            child_node.acronym = child.get('acronym')
            child_node.level = self.level 
            self.graph[child_name] = child_node
            node.children.append(child_node)
            self._make_graph(child)
        self.level -= 1
    
    def get_progeny(self,nodename,stoplevel=-1):
        """ 
        ---PURPOSE---
        Return a list of all progeny (aka descendents) of the the given nodename
        ---INPUT---
        nodename     The parent node whose descendents to retrieve
        """
        level = 0
        progeny_list = []
        self.get_progeny_helper(nodename,progeny_list,stoplevel,level=level)
        return progeny_list

    def get_progeny_helper(self,nodename,progeny_list,stoplevel,level):
        if stoplevel == -1:
            pass
        elif level == stoplevel:
            return 
        
        for child in self.graph[nodename].children:
            progeny_list.append(child.name)
            self.get_progeny_helper(child.name,progeny_list,stoplevel=stoplevel,level=level+1)
        level-=1
        return
    
    def get_parent(self,nodename):
        """ 
        ---PURPOSE---
        Return the parent of the given nodename
        ---INPUT---
        nodename     The node whose parent you want to retrieve
        """
        node = self.graph[nodename]
        if node.parent:
            return node.parent.name
        else:
            # root does not have a parent
            return None

    def get_progenitors(self,nodename):
        """ 
        ---PURPOSE---
        Return the line of progentiors [parent, grandparent, ..., root] of the given nodename in a list
        ---INPUT---
        nodename     The node whose parent you want to retrieve
        """
        node = self.graph[nodename]
        progenitors_list = []
        self.get_progenitors_helper(node,progenitors_list)
        return progenitors_list

    def get_progenitors_helper(self,node,progenitors_list):
        """ 
        ---PURPOSE---
        Return the line of progentiors [parent, grandparent, ..., root] of the given nodename in a list
        ---INPUT---
        nodename     The node whose parent you want to retrieve
        """

        if node.parent:
            progenitors_list.append(node.parent.name)
            self.get_progenitors_helper(node.parent,progenitors_list)
        else:
            # root does not have a parent
            return 

    def get_id(self,nodename):
        """ 
        ---PURPOSE---
        Return the id of the given nodename
        ---INPUT---
        nodename     The node whose id you want to retrieve
        """
        node = self.graph[nodename]
        return node.id

    def get_acronym(self,nodename):
        """ 
        ---PURPOSE---
        Return the acronym of the given nodename
        ---INPUT---
        nodename     The node whose acronym you want to retrieve
        """
        node = self.graph[nodename]
        return node.acronym

    def lookup_region_name_by_id(self,ID):
        """ 
        ---PURPOSE---
        Return the region name corresponding to an id, if one exists
        ---INPUT---
        ID     The id whose region name you want to look up
        """
        for node in self.graph.values():
            if node.id == ID:
                return node.name
        else:
            print(f"No region name found with id: {ID}")
            return None

    
    def print_branch(self,nodename,stoplevel=-1):
        """ 
        ---PURPOSE---
        Print out the branch of the ontology, 
        starting with a parent nodename
        ---INPUT---
        nodename     The parent node you want to start at
        stoplevel    The number of levels down from the parent 
                     node that you want to print. 
                     Use -1 to print the entire branch out
        """
        level = 0
        self.printstr = ""
        self._print_branch_helper(nodename,stoplevel=stoplevel,level=level)
        return self.printstr
    
    def _print_branch_helper(self,nodename,stoplevel=2,level=0):
        """ 
        ---PURPOSE---
        Helper function for printing out the ontology branch
        ---INPUT---
        nodename     The parent node you want to start at
        stoplevel    The number of levels down from the parent 
                     node that you want to print. 
                     Use -1 to print the entire branch out
        level        A variable used internally by the function. Do not modify.
        """
        if stoplevel == -1:
            pass
        elif level > stoplevel:
            return 
        this_str =" ".join(["\t"*level,str(level),str(nodename)])
        print(this_str)
        self.printstr+=this_str + "\n"
        for child in self.graph[nodename].children:
            self._print_branch_helper(child.name,stoplevel=stoplevel,level=level+1)
        level-=1
    
    def visualize_graph(self,nodename,stoplevel=-1):
        """ 
        ---PURPOSE---
        Visualize a graph using graphviz starting at a given node
        and stopping at a certain number of levels down 
        the ontology.
        ---INPUT---
        nodename     The parent node you want to start at
        stoplevel    The number of levels down from the parent 
                     node that you want to print. -1 shows all
        ---OUTPUT--- 
        graph        
        """
        digraph = graphviz.Digraph()
        self.visualize_graph_helper(nodename=nodename,graph=digraph,level=0,stoplevel=stoplevel)
        return digraph
    
    def visualize_graph_helper(self,nodename,graph,level,stoplevel):
        if stoplevel == -1:
            pass
        elif level >= stoplevel:
            return
        graph.node(nodename)
        for child in self.graph[nodename].children:
            graph.edge(nodename,child.name)
            self.visualize_graph_helper(child.name,graph=graph,level=level+1,stoplevel=stoplevel)
        level-=1
        return
    
    def make_html_ontology(self):
        """ 
        ---PURPOSE---
        Print out the entire ontology
        in html format with regions
        that are included in the dataframe in bold
        ---INPUT---
        """
        self.html_str = ''
        self.html_helper(nodename='root')
        return self.html_str

    def html_helper(self,nodename):
        node = self.graph[nodename]
        level = node.level
        
        if nodename == 'root':
            previous_level = -1
        else:
            previous_node = self.graph[self.last_checked_nodename]
            previous_level = previous_node.level
        
        if level > previous_level:
            self.html_str += '<ul style="list-style-type: none;">'
        elif level == previous_level:
            # dont need to do anything
            pass
        elif level < previous_level:
            # then we need to end unordered lists
            # the number of which we need to end depends on the difference between
            # current and previous level
            level_diff = previous_level-level
            self.html_str += '</ul>'*level_diff
        # Add the actual text to the html string        
        self.html_str += '<li>' + ' '.join([str(level),nodename,'</li>'])
        self.last_checked_nodename = nodename
        for child in self.graph[nodename].children:
            self.html_helper(child.name,)
        return