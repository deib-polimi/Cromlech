import copy
from Cromlech import abstractSolverFinalLinear
import yaml
from pyvis.network import Network
from apgl.graph import SparseGraph
from difflib import SequenceMatcher

# Graph is the starting graph of the architecture, keys are operations and values are entities
graph = {}
# Nodes_dict associates each number to an operation or entity
nodes_dict = {}
# This is the dict with the entities as keys and related operations as values
edges_from_e_to_o = {}
# Contains the edges as keys and the type of relationship as values
relationship_dict = {}
# Number of replicas
num_replicas = 0
# Associations between operations and the columns they read
op_reads = {}
# Associations between operations and the columns they write
op_writes = {}
# Associations between forced operations
forced_operations = {}
# Associations between each attribute index and its name
attributes_iton = {}
# Associations between each attribute name and its index
attributes_ntoi = {}
# The location of the primary replica for each attribute, represented by the index of the microservice
primary_replicas_locations = {}
# Static attributes are attributes which are not written by any operation, and thus do not have a primary replica and do not count in the operative costs
# Association between the index of an attribute and a boolean saying if it is static
static_status = {}
# High consistency write attributes are attributes which are  written by high consistency operations
# Association between the index of an attribute and a boolean saying if it is hc write
hc_write_status = {}
# High consistency read-only attributes are attributes which are read but not written by high consistency operations
# Association between the index of an attribute and a boolean saying if it is hc readonly
hc_readonly_status = {}
# Number of operations
op_num = -1
# List of all attributes indexes
attributes = []
# Associates each attribute to the ops which read it
attr_read_by = {}
# Associates each attribute to the ops which write it
attr_written_by = {}
# Words which are not counted in the LCS algorithm
banned_words = ['get', 'put', 'delete', 'read', 'write', 'retrieve', 'create', 'remove', 'save', 'query',
                'add', 'all', 'upload', 'insert', 'update', 'change', 'modify', 'by', 'fetch', 'from', 'find']
# name of operations cleaned of banned_words
cleaned_names = {}

class Graph:
    def __init__(self):
        self.__graph = copy.deepcopy(graph)
        self.__nodes_dict = copy.deepcopy(nodes_dict)
        self.__edges_from_e_to_o = copy.deepcopy(edges_from_e_to_o)
        self.__relationshp_dict = copy.deepcopy(relationship_dict)

    def get_graph(self):
        return self.__graph

    def get_nodes_dict(self):
        return self.__nodes_dict

    def get_edges_from_e_to_o(self):
        return self.__edges_from_e_to_o

    def get_relationshp_dict(self):
        return self.__relationshp_dict


class Operation:
    def __init__(self, name, index, frequency, consistency):
        self.__name = name
        self.__index = index
        self.__frequency = frequency
        self.__consistency = consistency

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_index(self):
        return self.__index

    def get_frequency(self):
        return self.__frequency

    def set_frequency(self, frequency):
        self.__frequency = frequency

    def get_consistency(self):
        return self.__consistency

    def set_consistency(self, consistency):
        self.__consistency = consistency


class Entity:
    def __init__(self, name, index):
        self.__name = name
        self.__index = index

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_index(self):
        return self.__index


def parse_arch_yaml(yaml_filename):
    with open(yaml_filename, 'r') as stream:
        try:
            op_names = []
            data = yaml.safe_load(stream)
            op_index = 0
            ent_index = len(data['operations'])
            entities = []
            for o in data['operations']:
                if o['name'] in op_names:
                    raise Exception("There are two operations named " + o['name'])
                op_names.append(o['name'])
                new_op = Operation(o['name'], op_index, int(o['frequency']), o['consistency'])
                nodes_dict.update({op_index: new_op})
                graph.update({op_index: []})
                op_reads.update({op_index: []})
                op_writes.update({op_index: []})
                for e in o['database_access']:
                    new_ent = Entity(e['entity_name'], ent_index)
                    already_listed = False
                    for e2 in entities:
                        if e2.get_name() == new_ent.get_name():
                            already_listed = True
                    if not already_listed:
                        entities.append(new_ent)
                        edges_from_e_to_o.update({ent_index: []})
                        nodes_dict.update({ent_index: new_ent})
                        ent_index += 1
                    try:
                        if e['read_attributes']:
                            for entity in entities:
                                if entity.get_name() == e['entity_name']:
                                    relationship_dict.update({(new_op.get_index(), entity.get_index()): 'R'})
                                    graph.get(new_op.get_index()).append(entity.get_index())
                                    if new_op.get_index() not in edges_from_e_to_o.get(entity.get_index()):
                                        edges_from_e_to_o.get(entity.get_index()).append(new_op.get_index())
                            for a in e['read_attributes']:
                                if e['entity_name'] + '.' + a not in op_writes.get(new_op.get_index()):
                                    op_reads.get(new_op.get_index()).append(e['entity_name'] + '.' + a)
                                else:
                                    raise Exception("Attribute " + e['entity_name'] + '.' + a + " of operation " + new_op.get_name() +
                                                    " is both read and written. This is not allowed.")
                    except KeyError:
                        pass
                    try:
                        if e['write_attributes']:
                            for entity in entities:
                                if entity.get_name() == e['entity_name']:
                                    relationship_dict.update({(new_op.get_index(), entity.get_index()): 'W'})
                                    graph.get(new_op.get_index()).append(entity.get_index())
                                    if new_op.get_index() not in edges_from_e_to_o.get(entity.get_index()):
                                        edges_from_e_to_o.get(entity.get_index()).append(new_op.get_index())
                            for a in e['write_attributes']:
                                if e['entity_name'] + '.' + a not in op_reads.get(new_op.get_index()):
                                    op_writes.get(new_op.get_index()).append(e['entity_name'] + '.' + a)
                                else:
                                    raise Exception("Attribute " + e['entity_name'] + '.' + a + " of operation " + new_op.get_name() +
                                                    " is both read and written. This is not allowed.")
                    except KeyError:
                        pass
                graph.update({op_index: list(set(graph.get(new_op.get_index())))})
                op_index += 1
            for o in data['operations']:
                fops = []
                for f in o['forced_operations']:
                    association = False
                    for n in nodes_dict:
                        if nodes_dict.get(n).get_name() == o['name'] and n < ent_index:
                            break
                    for n2 in nodes_dict:
                        if nodes_dict.get(n2).get_name() == f and n2 < ent_index:
                            fops.append(n2)
                            association = True
                    if not association and f:
                        raise Exception("No operation named " + f + ' exists, it cannot be forced along ' + o['name'])
                    forced_operations.update({n: fops})
            print([e.get_name() for e in entities])
        except yaml.YAMLError as exc:
            print(exc)


# Draws the graph with names instead of ids
def draw_graph_verbose(gr, html_filename):
    net = Network(height='1500px', width='100%', bgcolor="#dddddd")
    i = 0
    for n in gr.get_graph():
        net.add_node(gr.get_nodes_dict().get(n).get_name(), size=8, color='blue')
        for e in gr.get_graph().get(n):
            net.add_node(gr.get_nodes_dict().get(e).get_name(), size=8, color='seagreen')
            net.add_edge(gr.get_nodes_dict().get(n).get_name(), gr.get_nodes_dict().get(e).get_name())
    net.show(html_filename)


# Draws the graph showing the forced operations relationships
def draw_forcedops(html_filename):
    net = Network(height='2500px', width='100%', bgcolor="#dddddd")
    for g in graph:
        net.add_node(nodes_dict.get(g).get_name(), size=8, color='royalblue', mass=1.5)
    for f in forced_operations:
        for o in forced_operations.get(f):
            net.add_edge(nodes_dict.get(f).get_name(), nodes_dict.get(o).get_name())
    net.show(html_filename)


# Turns the microservice architecure in a format drawable with pyvis
def format_and_draw(microservices, html_filename):
    net = Network(height='2500px', width='100%', bgcolor="#dddddd")
    i = 0
    for m in microservices:
        ops = [x for x in m if x < op_num]
        attrs = [x for x in m if x >= op_num]
        for o in ops:
            if nodes_dict.get(o).get_consistency() == 'H':
                if op_writes.get(o):
                    net.add_node(nodes_dict.get(o).get_name(), size=8, color='black', mass=1.5)
                else:
                    net.add_node(nodes_dict.get(o).get_name(), size=8, color='navy', mass=1.5)
            else:
                net.add_node(nodes_dict.get(o).get_name(), size=8, color='royalblue', mass=1.5)
        for a in attrs:
            net.add_node(attributes_iton.get(a) + '@' + str(i), size=8, color='seagreen', shape='square', mass=1.5)
        for o in ops:
            accesses = op_reads.get(o) + op_writes.get(o)
            accesses_i = []
            for a in accesses:
                accesses_i.append(attributes_ntoi.get(a))
            for a in accesses_i:
                if a in attrs:
                    net.add_edge(nodes_dict.get(o).get_name(), attributes_iton.get(a) + '@' + str(i))
        i += 1
    net.show(html_filename)

# Turns the microservice architecure in a format drawable with pyvis
def format_and_draw_complete(microservices, html_filename):
    net = Network(height='2500px', width='100%', bgcolor="#dddddd")
    i = 0
    for m in microservices:
        net_single = Network(height='2500px', width='100%', bgcolor="#dddddd")
        ops = [x for x in m if x < op_num]
        attrs = [x for x in m if x >= op_num]
        for o in ops:
            if nodes_dict.get(o).get_consistency() == 'H':
                if op_writes.get(o):
                    net.add_node(nodes_dict.get(o).get_name(), size=8, color='black', mass=1.5)
                    net_single.add_node(nodes_dict.get(o).get_name(), size=8, color='black', mass=1.5)
                else:
                    net.add_node(nodes_dict.get(o).get_name(), size=8, color='navy', mass=1.5)
                    net_single.add_node(nodes_dict.get(o).get_name(), size=8, color='navy', mass=1.5)
            else:
                net.add_node(nodes_dict.get(o).get_name(), size=8, color='royalblue', mass=1.5)
                net_single.add_node(nodes_dict.get(o).get_name(), size=8, color='royalblue', mass=1.5)
        for a in attrs:
            net.add_node(attributes_iton.get(a) + '@' + str(i), size=8, color='darkgreen', shape='square', mass=1.5)
            net_single.add_node(attributes_iton.get(a) + '@' + str(i), size=8, color='darkgreen', shape='square', mass=1.5)
        for o in ops:
            accesses = op_reads.get(o) + op_writes.get(o)
            accesses_i = []
            for a in accesses:
                accesses_i.append(attributes_ntoi.get(a))
            for a in accesses_i:
                if a in attrs:
                    net.add_edge(nodes_dict.get(o).get_name(), attributes_iton.get(a) + '@' + str(i))
                    net_single.add_edge(nodes_dict.get(o).get_name(), attributes_iton.get(a) + '@' + str(i))
        net_single.show("Service " + str(i) + ".html")
        i += 1
    net.show(html_filename)

def format_and_draw_final(microservices, html_filename):
    net = Network(height='2500px', width='100%', bgcolor="#dddddd")
    i = 0
    for m in microservices:
        net_single = Network(height='2500px', width='100%', bgcolor="#dddddd")
        ops = [x for x in m if isinstance(x, int)]
        attrs = [x for x in m if isinstance(x, str)]
        for o in ops:
            if nodes_dict.get(o).get_consistency() == 'H':
                if op_writes.get(o):
                    net.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency()*1.2, color='navy', mass=1.5, group=i)
                    net_single.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency()*1.2, color='navy', mass=1.5, group=i)
                else:
                    net.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency() * 1.2,
                                 color='mediumseagreen', mass=1.5, group=i)
                    net_single.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency() * 1.2,
                                        color='mediumseagreen', mass=1.5, group=i)
            else:
                if op_writes.get(o):
                    net.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency()*1.2, color='dodgerblue', mass=1.5, group=i)
                    net_single.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency()*1.2, color='dodgerblue', mass=1.5, group=i)
                else:
                    net.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency()*1.2,
                                 color='mediumseagreen', mass=1.5, group=i)
                    net_single.add_node(nodes_dict.get(o).get_name(), size=8 + nodes_dict.get(o).get_frequency()*1.2,
                                        color='mediumseagreen', mass=1.5, group=i)
        attr_count = {}
        for a in attrs:
            attr_id = attributes_iton.get(int(a[:len(a) - 1]))
            count = 0
            for m2 in microservices:
                attr_int = [int(x[:len(x)-1]) for x in m2 if isinstance(x, str)]
                if attributes_ntoi.get(attr_id) in attr_int:
                    count += 1
            attr_count.update({int(a[:len(a) - 1]): count })
            repl_status = a[len(a) - 1]
            if repl_status == 'N':
                net.add_node(attr_id + '@' + str(i) + '/'   + str(count), size=8, color='yellow', shape='square', mass=1.5, group=i)
                net_single.add_node(attr_id + '@' + str(i)  + '/' + str(count), size=8, color='yellow', shape='square', mass=1.5, group=i)
            if repl_status == 'R':
                net.add_node(attr_id + '@' + str(i) + '/'   + str(count) , size=8, color='orange', shape='square', mass=1.5, group=i)
                net_single.add_node(attr_id + '@' + str(i)  + '/' + str(count), size=8, color='orange', shape='square', mass=1.5, group=i)
            if repl_status == 'P':
                net.add_node(attr_id + '@' + str(i) + '/'   + str(count), size=8, color='red', shape='square', mass=1.5, group=i)
                net_single.add_node(attr_id + '@' + str(i)  + '/' + str(count), size=8, color='red', shape='square', mass=1.5, group=i)
        for o in ops:
            accesses = op_reads.get(o) + op_writes.get(o)
            accesses_i = []
            attrs_num = []
            for a in accesses:
                accesses_i.append(attributes_ntoi.get(a))
            for a in attrs:
                attrs_num.append(int(a[:len(a) - 1]))
            for a in accesses_i:
                if a in attrs_num:
                    net.add_edge(nodes_dict.get(o).get_name(), attributes_iton.get(a) + '@' + str(i) + '/' + str(attr_count.get(a)) )
                    net_single.add_edge(nodes_dict.get(o).get_name(), attributes_iton.get(a) + '@' + str(i) + '/' + str(attr_count.get(a)) )
        net_single.show("Service " + str(i) + ".html")
        i += 1

    net.show(html_filename)


# Returns connected components of graph
def get_connected_components(gr):
    size = len(gr.get_nodes_dict())
    g = SparseGraph(size, frmt='lil')
    gra = gr.get_graph()
    for n in gra:
        for n2 in gra.get(n):
            g.addEdge(n, n2)
    return g.findConnectedComponents()


def compute_communication_cost(microservices):
    w_op = 0
    location_dict = {}
    op_scores = {}
    for g in graph:
        for m in microservices:
            if g in m:
                location_dict.update({g: microservices.index(m)})
    for a in primary_replicas_locations:
        if not static_status.get(a):
            m_index = 0
            for m in microservices:
                if m_index == primary_replicas_locations.get(a):
                    m_index += 1
                    continue
                for o in m:
                    if o in attr_written_by.get(a):
                        w_op += nodes_dict.get(o).get_frequency()
                        ent_name = attributes_iton.get(a).split('.')[0]
                        if op_scores.get(ent_name):
                            op_scores.update({ent_name: op_scores.get(ent_name) + nodes_dict.get(o).get_frequency()})
                        else:
                            op_scores.update({ent_name: nodes_dict.get(o).get_frequency()})
                m_index += 1
    r_op = 0
    repl = 0
    caches = {}
    for a in attributes:
        ent_name = attributes_iton.get(a).split('.')[0]
        m_index = -1
        for m in microservices:
            m_index += 1
            if a in m and not primary_replicas_locations.get(a) == m_index:
                read_in_same = 0
                total_write = 0
                for o in m:
                    if o < 10000 and attributes_iton.get(a) in op_reads.get(o):
                        read_in_same += nodes_dict.get(o).get_frequency()
                for m2 in microservices:
                    for o in m2:
                        if o < 10000 and attributes_iton.get(a) in op_writes.get(o):
                            total_write += nodes_dict.get(o).get_frequency()
                if read_in_same >= total_write:
                    repl += total_write
                    caches.update({(a, m_index): True})
                    if op_scores.get(ent_name):
                        op_scores.update(
                            {ent_name: op_scores.get(ent_name) + total_write})
                    else:
                        op_scores.update({ent_name: total_write})
                else:
                    r_op += read_in_same
                    caches.update({(a, m_index): False})
                    if op_scores.get(ent_name):
                        op_scores.update(
                            {ent_name: op_scores.get(ent_name) + read_in_same})
                    else:
                        op_scores.update({ent_name: read_in_same})
            else:
                continue

    repl2 = 0
    for a in attributes:
        replica_num = 1
        total_write = 0
        m_index = -1
        for m in microservices:
            m_index += 1
            if a in m and caches.get((a, m_index)):
                replica_num += 1
            for o in m:
                if o < 10000 and attributes_iton.get(a) in op_writes.get(o):
                    total_write += nodes_dict.get(o).get_frequency()
        if replica_num > 1:
            repl2 += total_write * (replica_num - 1)
            ent_name = attributes_iton.get(a).split('.')[0]
            if op_scores.get(ent_name):
                op_scores.update({ent_name: op_scores.get(ent_name) + total_write * (replica_num - 1)})
            else:
                op_scores.update({ent_name: total_write * (replica_num - 1)})
    print("ROP " + str(r_op))
    print("REPL " + str(repl) + " - " + str(repl2))
    print("WOP " + str(w_op))
    return w_op + r_op + repl

def post_processing_communication_cost(result):
    repl = 0
    for a in attributes:
        repl_num = 0
        total_write = 0
        for m in result:
            attr_int = [int(x[:len(x)-1]) for x in m if isinstance(x, str)]
            if a in attr_int and (str(a) + 'R') in m:
                repl_num += 1
        for o in graph:
            if o < op_num:
                if attributes_iton.get(a) in op_writes.get(o):
                    total_write += nodes_dict.get(o).get_frequency()
        repl += total_write * repl_num

    rop = 0
    for a in attributes:
        for m in result:
            attr_int = [int(x[:len(x)-1]) for x in m if isinstance(x, str)]
            ops = [x for x in m if isinstance(x, int)]
            if a in attr_int and (str(a) + 'N') in m:
                for o in ops:
                    if attributes_iton.get(a) in op_reads.get(o):
                        rop += nodes_dict.get(o).get_frequency()

    wop = 0
    for a in attributes:
        for m in result:
            attr_int = [int(x[:len(x)-1]) for x in m if isinstance(x, str)]
            ops = [x for x in m if isinstance(x, int)]
            if a in attr_int and (str(a) + 'P') not in m:
                for o in ops:
                    if attributes_iton.get(a) in op_writes.get(o):
                        wop += nodes_dict.get(o).get_frequency()
    print("POST PROCESSING:")
    print("WOP " + str(wop))
    print("ROP " + str(rop))
    print("REPL " + str(repl))

# Removes all columns which only create noise (as they are only accessed by a single operation) and returns
# the list of operations which have no accessed columns, which can then be trimmed from the architecture
def noise_removal():
    all_columns = []
    to_remove = []
    for op in graph:
        all_columns += list(set(op_reads.get(op) + op_writes.get(op)))
    for op in graph:
        related_columns = op_reads.get(op) + op_writes.get(op)
        for c in related_columns:
            if all_columns.count(c) == 1:
                if c in op_reads.get(op):
                    print("Removed " + c)
                    op_reads.get(op).remove(c)
                if c in op_writes.get(op):
                    op_writes.get(op).remove(c)
                if len(op_reads.get(op) + op_writes.get(op)) == 0:
                    to_remove.append(op)
    return to_remove


# Finds the static attributes and populates the static_status dict
def identify_static_attributes():
    written = []
    for o in op_writes:
        for a in op_writes.get(o):
            written.append(attributes_ntoi.get(a))
    written = list(set(written))
    read = []
    for o in op_reads:
        for a in op_reads.get(o):
            read.append(attributes_ntoi.get(a))
    read = list(set(read))
    all_attrs = list(set(written + read))
    for a in all_attrs:
        static_status.update({a: False})
        if a not in written:
            static_status.update({a: True})


# Finds the hc read only attributes and populates the hc_readonly_status dictionary
def identify_hc_readonly_attributes():
    written = []
    for o in op_writes:
        if nodes_dict.get(o).get_consistency() == 'H':
            for a in op_writes.get(o):
                written.append(attributes_ntoi.get(a))
    written = list(set(written))
    read = []
    for o in op_reads:
        if nodes_dict.get(o).get_consistency() == 'H':
            for a in op_reads.get(o):
                read.append(attributes_ntoi.get(a))
    read = list(set(read))
    all_attrs = list(set(written + read))
    for a in all_attrs:
        if a not in written:
            hc_readonly_status.update({a: True})


def elect_primary_replicas(microservices):
    for a in attributes:
        if not static_status.get(a):
            if hc_write_status.get(a):
                elect_hcw(a, microservices)
            else:
                elect_w(a, microservices)
        else:
            elect_s(a, microservices)
    return

def elect_s(attribute, microservices):
    for m in microservices:
        if attribute in m:
            primary_replicas_locations.update({attribute: microservices.index(m)})
            return

def elect_hcw(attribute, microservices):
    for m in microservices:
        if attribute in m:
            ops = [n for n in m if n < op_num and nodes_dict.get(n).get_consistency() == 'H']
            for o2 in ops:
                if attributes_iton.get(attribute) in op_writes.get(o2) + op_reads.get(o2) and op_writes.get(o2):
                    primary_replicas_locations.update({attribute: microservices.index(m)})
                    return
    raise Exception("Attribute " + attributes_iton.get(attribute) + " was wrongly categorized as hc write.")


def elect_w(attribute, microservices):
    frequencies = []
    for m in microservices:
        if attribute in m:
            ops = [n for n in m if n < op_num]
            frequency = 0
            for o2 in ops:
                if attributes_iton.get(attribute) in op_writes.get(o2):
                    frequency += nodes_dict.get(o2).get_frequency()
            frequencies.append(frequency)
        else:
            frequencies.append(0)
    if max(frequencies) == 0:
        raise Exception("Attribute " + attributes_iton.get(attribute) + " was wrongly categorized as lc write.")
    primary_replicas_locations.update({attribute: frequencies.index(max(frequencies))})
    return


# Joins the forced operations
def force_operations():
    services_temp = []
    services = []
    for o in op_reads:
        for o2 in op_reads:
            if o2 != o and nodes_dict.get(o).get_consistency() == 'H' and nodes_dict.get(o2).get_consistency() == 'H' and op_writes.get(o) and op_writes.get(o2):
                if compute_op_similarity(o, o2) > 0 and o2 not in forced_operations.get(o):
                    forced_operations.get(o).append(o2)
        services_temp.append([o] + forced_operations.get(o))
    for o in op_reads:
        indices = []
        for s in services_temp:
            if o in s:
                indices.append(services_temp.index(s))
        new_serv = []
        for i in indices:
            new_serv += services_temp[i]
        services_temp.append(new_serv)
        for i in indices:
            services_temp.remove(services_temp[i])
            for i2 in indices:
                if i2 > i:
                    indices[indices.index(i2)] -= 1
    for s in services_temp:
        if s:
            services.append(list(set(s)))
    return services

def clean_names():
    for g in graph:
        clean = nodes_dict.get(g).get_name().lower()
        for w in banned_words:
            if w in clean:
                clean = clean.replace(w, '')
        cleaned_names.update({g: clean})

def set_overlap(o1, o2):
    accesses1 = set(op_writes.get(o1) + op_reads.get(o1))
    accesses2 = set(op_writes.get(o2) + op_reads.get(o2))
    return float(len(accesses1.intersection(accesses2)) / min(len(accesses1), len(accesses2)))

def semantic_overlap(o1, o2):
    name1 = cleaned_names.get(o1)
    name2 = cleaned_names.get(o2)
    seqMatch = SequenceMatcher(None, name1, name2)
    match = seqMatch.find_longest_match(0, len(name1), 0, len(name2))
    if match.size < 4:
        return 0
    else:
        return match.size / min(len(name1), len(name2))

def compute_semantic_score(services):
    sim = []
    for s in services:
        ops = [x for x in s if x < op_num]
        similarities = []
        for o in ops:
            for o2 in ops:
                similarities.append(semantic_overlap(o, o2))
        sim.append(round((sum(similarities) * len(ops)) / (op_num * len(similarities)), 4))
    return sum(sim)

def compute_op_similarity(o1, o2):
    if o1 == o2:
        return 1
    set_o = set_overlap(o1, o2)
    if set_o == 1:
        semantic_penalty = 1
        name1 = cleaned_names.get(o1)
        name2 = cleaned_names.get(o2)
        seqMatch = SequenceMatcher(None, name1, name2)
        match = seqMatch.find_longest_match(0, len(name1), 0, len(name2))
        if match.size < 4:
            semantic_penalty = 0.9 #OCCHIO
        return set_o * semantic_penalty
    return set_o


def compute_total_coupling(services):
    sim = []
    suca = 0
    for s in services:
        ops = [x for x in s if x < op_num]
        similarities = []
        for o in ops:
            for o2 in ops:
                similarities.append(compute_op_similarity(o, o2))
        sim.append(round((sum(similarities) * len(ops)) / (op_num * len(similarities)), 4))
        suca += len(ops)
    return sum(sim)

def write_dat_file(num_services):
    read_dependencies = {}
    write_dependencies = {}
    access_dependencies = {}
    for g in graph:
        reads = [attributes_ntoi.get(a) for a in op_reads.get(g)]
        writes = [attributes_ntoi.get(a) for a in op_writes.get(g)]
        for a in attributes:
            access_dependencies.update({(g, a - 100000): 1})
            if a in reads:
                read_dependencies.update({(g, a - 100000): 1})
            else:
                read_dependencies.update({(g, a - 100000): 0})
            if a in writes:
                write_dependencies.update({(g, a - 100000): 1})
            else:
                write_dependencies.update({(g, a - 100000): 0})
            if a not in reads and a not in writes:
                access_dependencies.update({(g, a - 100000): 0})

    print("Producing .dat file with " +str(num_services) + " services...")
    data = open('data.dat', 'w')
    data.write("data;\n\n")
    data.write("set MICROSERVICES := ")
    for n in range(0, num_services):
        data.write("M" + str(n) + " ")
    data.write(";\n\n")
    data.write("set OPERATIONS := ")
    for n in range(0, op_num):
        data.write("O" + str(n) + " ")
    data.write(";\n\n")
    data.write("set ENTITIES := ")
    for n in range(0, len(attributes)):
        data.write("E" + str(n) + " ")
    data.write(";\n\n")
    data.write("param frequencies:\n    ")
    for n in range(0, op_num):
        data.write("O" + str(n) + " ")
    data.write(":=")
    data.write("\nF   ")
    for n in range(0, op_num):
        spaces = " "
        for l in range(0, len(str(n)) + 1 - len(str(nodes_dict.get(n).get_frequency()))):
            spaces += " "
        data.write(str(nodes_dict.get(n).get_frequency()) + spaces)
    data.write(";\n\n")
    data.write("param acc:\n    ")
    for n in range(0, len(attributes)):
        data.write("E" + str(n) + " ")
    data.write(":=")
    for n in range(0, op_num):
        spaces = " "
        for l in range(0, 2 - len(str(n))):
            spaces += " "
        data.write("\nO" + str(n) + spaces)
        for a in range(0, len(attributes)):
            spaces = " "
            for l in range(0, len(str(a))):
                spaces += " "
            if access_dependencies.get((n, a)) == 1:
                data.write(str(1) + spaces)
            else:
                data.write(str(0) + spaces)
    data.write(";\n\n")
    data.write("param accr:\n    ")
    for n in range(0, len(attributes)):
        data.write("E" + str(n) + " ")
    data.write(":=")
    for n in range(0, op_num):
        spaces = " "
        for l in range(0, 2 - len(str(n))):
            spaces += " "
        data.write("\nO" + str(n) + spaces)
        for a in range(0, len(attributes)):
            spaces = " "
            for l in range(0, len(str(a))):
                spaces += " "
            if read_dependencies.get((n, a)) == 1:
                data.write(str(1) + spaces)
            else:
                data.write(str(0) + spaces)
    data.write(";\n\n")
    data.write("param accrw:\n    ")
    for n in range(0, len(attributes)):
        data.write("E" + str(n) + " ")
    data.write(":=")
    for n in range(0, op_num):
        spaces = " "
        for l in range(0, 2 - len(str(n))):
            spaces += " "
        data.write("\nO" + str(n) + spaces)
        for a in range(0, len(attributes)):
            spaces = " "
            for l in range(0, len(str(a))):
                spaces += " "
            if write_dependencies.get((n, a)) == 1:
                data.write(str(1) + spaces)
            else:
                data.write(str(0) + spaces)
    data.write(";\n\n")
    data.write("param coloc:\n    ")
    for n in range(0, op_num):
        data.write("O" + str(n) + " ")
    data.write(":=")
    for n in range(0, op_num):
        spaces = " "
        for l in range(0, 2 - len(str(n))):
            spaces += " "
        data.write("\nO" + str(n) + spaces)
        for a in range(0, op_num):
            spaces = " "
            for l in range(0, len(str(a))):
                spaces += " "
            if bound_ops.get((n, a)) == 1:
                data.write(str(1) + spaces)
            else:
                data.write(str(0) + spaces)
    data.write(";\n\n")
    data.write("param tr:\n    ")
    for o in range(0, op_num):
        data.write("O" + str(o) + " ")
    data.write(":=")
    data.write("\nT   ")
    for o in range(0, op_num):
        spaces = " "
        for l in range(0, len(str(o))):
            spaces += " "
        if nodes_dict.get(o).get_consistency() == 'H':
            data.write(str(1) + spaces)
        else:
            data.write(str(0) + spaces)
    data.write(";\n\n")
    data.write("param similarity:\n    ")
    for n in range(0, op_num):
        data.write("O" + str(n) + " ")
    data.write(":=")
    for n in range(0, op_num):
        spaces = " "
        for l in range(0, 2 - len(str(n))):
            spaces += " "
        data.write("\nO" + str(n) + spaces)
        for n2 in range(0, op_num):
            spaces = " "
            for l in range(0, len(str(n2))):
                spaces += " "
            data.write(str(compute_op_similarity(n, n2)) + spaces)
    data.write(";")
    data.close()

def trim_operations(to_remove):
    op_num = len(graph)
    for t in to_remove:
        print("Removed op. " + nodes_dict.get(t).get_name())
        graph.pop(t)
        nodes_dict.pop(t)
        op_reads.pop(t)
        op_writes.pop(t)
        forced_operations.pop(t)
        for i in range(t, op_num):
            graph.update({i: graph.get(i + 1)})
            nodes_dict.update({i: nodes_dict.get(i + 1)})
            op_reads.update({i: op_reads.get(i + 1)})
            op_writes.update({i: op_writes.get(i + 1)})
            forced_operations.update({i: forced_operations.get(i + 1)})
        graph.pop(op_num - 1)
        nodes_dict.pop(op_num - 1)
        op_reads.pop(op_num - 1)
        op_writes.pop(op_num - 1)
        forced_operations.pop(op_num - 1)
        for f in forced_operations:
            if t in forced_operations.get(f):
                forced_operations.get(f).remove(t)
            for f2 in forced_operations.get(f):
                if f2 > t:
                    forced_operations.get(f)[forced_operations.get(f).index(f2)] -= 1
        op_num = len(graph)
        for t2 in range(0, len(to_remove)):
            if to_remove[t2] > t:
                to_remove[t2] -= 1

def build_attr_relationships():
    attrs = []
    for g in graph:
        for a in op_writes.get(g):
            attrs.append(a)
        for a in op_reads.get(g):
            attrs.append(a)
    all_attrs = list(set(attrs))
    all_attrs.sort()
    index = 100000
    for a in all_attrs:
        attributes_iton.update({index: a})
        attributes_ntoi.update({a: index})
        index += 1
        read_by = []
        written_by = []
        for o in graph:
            if a in op_reads.get(o):
                read_by.append(o)
            if a in op_writes.get(o):
                written_by.append(o)
        attr_read_by.update({attributes_ntoi.get(a): read_by})
        attr_written_by.update({attributes_ntoi.get(a): written_by})
    res = [attributes_ntoi.get(x) for x in all_attrs]
    return res

def build_hcw_relationships():
    # Lists the high consistency write operations
    hc_writes = []
    for o in graph:
        if nodes_dict.get(o).get_consistency() == 'H' and op_writes.get(o) != []:
            hc_writes.append(o)

    hcwassociations = {}
    # Lists the columns which are written
    hc_written_columns = []
    for o in hc_writes:
        for x in op_writes.get(o) + op_reads.get(o):
            hc_written_columns.append(x)
            hcwassociations.update({attributes_ntoi.get(x) - 100000: o})
    hc_written_columns = list(set(hc_written_columns))

    for a in attributes:
        if not hcwassociations.get(a - 100000):
            hcwassociations.update({a - 100000: -1})
    for a in attributes:
        if attributes_iton.get(a) in hc_written_columns:
            hc_write_status.update({a: True})
        else:
            hc_write_status.update(({a: False}))


if __name__ == '__main__':
    parse_arch_yaml('trainticket.yaml')
    print("Preprocessing...")
    to_remove = noise_removal()
    graph_copy = Graph()
    op_num = len(graph)
    trim_operations(to_remove)
    op_num = len(graph)
    attributes = build_attr_relationships()
    build_hcw_relationships()
    clean_names()
    services = force_operations()
    bound_ops = {}
    for s in services:
        for o1 in s:
            for o2 in graph:
                if o2 in s:
                    #######
                    bound_ops.update({(o1, o2): 1})
                else:
                    bound_ops.update({(o1, o2): 0})

    for l in services:
        attrs = []
        for s in l:
            attrs += op_writes.get(s) + op_reads.get(s)
        attrs = list(set(attrs))
        for a in attrs:
            services[services.index(l)].append(attributes_ntoi.get(a))

    identify_static_attributes()
    identify_hc_readonly_attributes()
    elect_primary_replicas(services)

    for g in graph:
        if g < op_num:
            print(str(g) + " " + nodes_dict.get(g).get_name())
    min_decoupling_bound = compute_total_coupling([[o for o in graph]])
    max_decoupling_bound = compute_total_coupling(services)
    max_com_cost = compute_communication_cost(services)

    # Specify number of services HERE
    write_dat_file(4)
    # Specify alpha parameter HERE
    alpha = 0.5
    opt_result = abstractSolverFinalLinear.optimizer(op_num, max_com_cost, alpha)

    opt_result_only_nums = []
    for m in opt_result:
        ops = [x for x in m if isinstance(x, int)]
        attrs = [x for x in m if isinstance(x, str)]
        attrs_num = [int(x[:len(x) - 1]) for x in attrs]
        opt_result_only_nums.append(ops + attrs_num)

    print(opt_result_only_nums)
    print(compute_total_coupling(opt_result_only_nums))
    elect_primary_replicas(opt_result_only_nums)
    print(compute_communication_cost(opt_result_only_nums))
    print(compute_communication_cost(opt_result_only_nums) / max_com_cost)
    print(post_processing_communication_cost(opt_result))
    format_and_draw_final(opt_result, "test.html")
