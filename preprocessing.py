import json
import copy
<<<<<<< Updated upstream:main.py
import operator
=======
from Cromlech import abstractSolverFinalLinear
>>>>>>> Stashed changes:preprocessing.py
import yaml
from pyvis.network import Network
from apgl.graph import SparseGraph
import numpy as np
import random

# Graph is the starting graph of the architecture, keys are operations and values are entities
graph = {}
# Nodes_dict associates each number to an operation or entity
nodes_dict = {}
# This is the dict with the entities as keys and related operations as values
edges_from_e_to_o = {}
# Contains the edges as keys and the type of relationship as values
relationship_dict = {}
# Dictionary which contains the entities id as key and their required consistency as value
ent_consistencies = {}
# Number of replicas
num_replicas = 0
# Associations between operations and the columns they read
op_reads = {}
# Associations between operations and the columns they write
op_writes = {}
# Associations between replica identifiers and the indices of the microservices they can be found in
replica_locations = {}
# The location of the primary replica for each entity, to be assigned after the clustering. The location is represented by the id of an operation in the same microservices
# since operations uniquely identify microservices
primary_replicas_locations = {}

primary_replicas_microservices = {}
# The associations between secondary replicas (represented by their id and their microservice) and their indices in the chromosomes of the GA
secondary_replicas_indices = {}


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
        self.__required_consistency = ''

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_index(self):
        return self.__index


def parse_arch_json(json_filename):
    with open(json_filename) as f:
        data = json.load(f)
    ent = data['entities']
    op = data['operations']
    entities = []
    # Index of the last created node
    last_index = len(op)
    for e in ent:
        new_ent = Entity(e['name'], last_index)
        entities.append(new_ent)
        nodes_dict.update({last_index: new_ent})
        edges_from_e_to_o.update({new_ent.get_index(): []})
        last_index += 1
    last_index = 0
    for o in op:
        new_op = Operation(o['name'], last_index, int(o['frequency']), o['consistency'])
        last_index += 1
        nodes_dict.update({new_op.get_index(): new_op})
        graph.update({new_op.get_index(): []})
        op_reads.update({new_op.get_index(): []})
        op_writes.update({new_op.get_index(): []})
        for e in o['database_access']:
            try:
                if e['read_attributes']:
                    for entity in entities:
                        if entity.get_name() == e['entity_name']:
                            relationship_dict.update({(new_op.get_index(), entity.get_index()): 'R'})
                            graph.get(new_op.get_index()).append(entity.get_index())
                            if new_op.get_index() not in edges_from_e_to_o.get(entity.get_index()):
                                edges_from_e_to_o.get(entity.get_index()).append(new_op.get_index())
                    for a in e['read_attributes']:
                        op_reads.get(new_op.get_index()).append(e['entity_name'] + '.' + a)
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
                        op_writes.get(new_op.get_index()).append(e['entity_name'] + '.' + a)
            except KeyError:
                pass
        graph.update({new_op.get_index(): list(set(graph.get(new_op.get_index())))})
    compute_consistency_lists()


def parse_arch_yaml(yaml_filename):
    with open(yaml_filename, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            op_index = 0
            ent_index = len(data['operations'])
            entities = []
            for o in data['operations']:
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
                                op_reads.get(new_op.get_index()).append(e['entity_name'] + '.' + a)
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
                                op_writes.get(new_op.get_index()).append(e['entity_name'] + '.' + a)

                    except KeyError:
                        pass
                graph.update({op_index: list(set(graph.get(new_op.get_index())))})
                op_index += 1
        except yaml.YAMLError as exc:
            print(exc)
    compute_consistency_lists()


op_num = len(graph)


# Computes the dictionary which associates each entity to its required consistency
def compute_consistency_lists():
    for e in edges_from_e_to_o:
        relationships = edges_from_e_to_o.get(e)
        for r in relationships:
            operation = nodes_dict.get(r)
            if operation.get_consistency() == 'S':
                ent_consistencies.update({e: 'S'})
                break
            else:
                ent_consistencies.update({e: 'N'})


# Draws the graph with names instead of ids
def draw_graph_verbose(gr, html_filename):
    net = Network(height='1500px', width='100%', bgcolor="#dddddd")
    i = 0
    for n in gr.get_graph():
        net.add_node(gr.get_nodes_dict().get(n).get_name(), size=8, color='blue')
        for e in gr.get_graph().get(n):
            net.add_node(gr.get_nodes_dict().get(e).get_name(), size=8, color='red')
            net.add_edge(gr.get_nodes_dict().get(n).get_name(), gr.get_nodes_dict().get(e).get_name())
    net.show(html_filename)


<<<<<<< Updated upstream:main.py
=======
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


>>>>>>> Stashed changes:preprocessing.py
# Returns connected components of graph
def get_connected_components(gr):
    size = len(gr.get_nodes_dict())
    g = SparseGraph(size, frmt='lil')
    gra = gr.get_graph()
    for n in gra:
        for n2 in gra.get(n):
            g.addEdge(n, n2)
    return g.findConnectedComponents()


<<<<<<< Updated upstream:main.py
# Computes similarity between two microservices, by comparing each pair of operations from the two using their accessed
# columns as sets in a Jaccard similarity, and then getting the median between all couples
def compute_similarity(ms1, ms2):
    cols1 = []
    for m in ms1:
        cols1 += op_reads.get(m) + op_writes.get(m)
    cols2 = []
    for m in ms2:
        cols2 += op_reads.get(m) + op_writes.get(m)
    if len(list(set(cols1).intersection(cols2))) == 0:
        return 0
    ops = ms1 + ms2
    not_yet_computed = copy.deepcopy(ops)
    scores = []
    for o1 in ops:
        reads1 = op_reads.get(o1)
        writes1 = op_writes.get(o1)
        total1 = list(set(reads1 + writes1))
        for o2 in not_yet_computed:
            if o1 == o2:
                continue
            else:
                reads2 = op_reads.get(o2)
                writes2 = op_writes.get(o2)
                total2 = list(set(reads2 + writes2))
                intersection = len(list(set(total1).intersection(total2)))
                union = (len(total1) + len(total2)) - intersection
                scores.append(float(intersection) / union)
        not_yet_computed.remove(o1)
    return np.median(scores)


# Computes Jaccard similarity between two microservices, using as sets all the accessed columns by the microservices' operations
def compute_ms_similarity(ms1, ms2):
    total1 = []
    for o in ms1:
        reads = op_reads.get(o)
        writes = op_writes.get(o)
        total1 += reads + writes
    total2 = []
    for o in ms2:
        reads = op_reads.get(o)
        writes = op_writes.get(o)
        total2 += reads + writes
    total1 = list(set(total1))
    total2 = list(set(total2))
    intersection = len(list(set(total1).intersection(total2)))
    union = (len(total1) + len(total2)) - intersection
    return float(intersection) / union


# Computes intraservice cohesion as the mean of all Jaccard similaritys between each operation and the rest of the operations
# in the microservice
def compute_intraservice_cohesion(ms):
    final_scores = []
    for m in ms:
        if len(m) < 2:
            final_scores.append(1)
            continue
        scores = []
        for o in m:
            temp = copy.deepcopy(m)
            temp.remove(o)
            scores.append(compute_ms_similarity([o], temp))
        final_scores.append(np.mean(scores))
    return np.mean(final_scores)


# Computes coupling score as the mean of Jaccard similarities between each pair of microservices
def compute_coupling_score(ms):
    already_visited = copy.deepcopy(ms)
    scores = []
    for m in ms:
        for m2 in already_visited:
            if m != m2:
                scores.append(compute_ms_similarity(m, m2))
        already_visited.remove(m)
    return np.mean(scores)


# Turns the microservice architecure in a format drawable with pyvis (NEEDS REFACTORING)
def format_and_draw(microservices, op_num, html_filename, chr=None):
    names_ents = []
    name_ops = []
    indices_ops = []
    for l in microservices:
        names_ents.append([nodes_dict.get(x).get_name() for x in l if x >= op_num])
        name_ops.append([nodes_dict.get(x).get_name() for x in l if x < op_num])
        indices_ops.append([x for x in l if x < op_num])
    names_set = []
    for l in names_ents:
        for n in l:
            if n not in names_set:
                names_set.append(n)
    total_replicas = 0
    for n in names_set:
        count = 0
        for l in names_ents:
            i = 0
            for i in range(0, len(l)):
                if l[i] == n:
                    l[i] += '#R' + str(count)
                    count += 1
        total_replicas += count
    print("TOTAL REPLICAS " + str(total_replicas - len(ent_consistencies)))
    print("REPLICATION FACTOR " + str((total_replicas - len(ent_consistencies)) / len(ent_consistencies)))
    i = 0
    primary_replicas = []
    for p in primary_replicas_locations:
        op_index = primary_replicas_locations.get(p)
        m_index = -1
        for m in microservices:
            if op_index in m:
                m_index = microservices.index(m)
                break
        for e in names_ents[m_index]:
            if nodes_dict.get(p).get_name() == e.split('#')[0]:
                primary_replicas.append(e)
                break
    new_dict = {}
    for i in range(0, len(name_ops)):
        for j in range(0, len(name_ops[i])):
            edges = graph.get(indices_ops[i][j])
            new_dict.update({name_ops[i][j]: []})
            for e in edges:
                name = nodes_dict.get(e).get_name()
                names_in_microservices = names_ents[i]
                for n in names_in_microservices:
                    if n.split('#')[0] == name:
                        new_dict.get(name_ops[i][j]).append(n)
    net = Network(height='2500px', width='100%', bgcolor="#dddddd")
    absent = []
    if chr:
        for p in secondary_replicas_indices:
            if not chr[secondary_replicas_indices.get(p)]:
                ops_in_same_m = [o for o in microservices[p[1]] if o < op_num]
                for o in ops_in_same_m:
                    for e in new_dict.get(nodes_dict.get(o).get_name()):
                        if nodes_dict.get(p[0]).get_name() == e.split("#")[0]:
                            absent.append(e)
                            break
    for n in new_dict:
        for n2 in nodes_dict:
            if nodes_dict.get(n2).get_name() == n:
                if nodes_dict.get(n2).get_consistency() == 'S':
                    net.add_node(n, size=8, color='navy', mass=1.5)
                else:
                    net.add_node(n, size=8, color='royalblue', mass=1.5)
        for e in new_dict.get(n):
            if e in primary_replicas:
                net.add_node(e, size=8, color='red', shape='square', mass=1.5)
            elif e in absent:
                net.add_node(e, size=8, color='white', shape='diamond', mass=1.5)
            else:
                net.add_node(e, size=8, color='lightsalmon', shape='square', mass=1.5)
            net.add_edge(n, e)
    net.show(html_filename)
=======
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
    """
    print(op_scores)
    mpl.rcParams.update({'font.size': 7})
    x = dict(sorted(op_scores.items(), key=lambda item: item[1], reverse=True))
    mpl.bar(x.keys(), x.values())
    mpl.show()
    """
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
>>>>>>> Stashed changes:preprocessing.py

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
                    op_reads.get(op).remove(c)
                if c in op_writes.get(op):
                    op_writes.get(op).remove(c)
                if len(op_reads.get(op) + op_writes.get(op)) == 0:
                    to_remove.append(op)
    return to_remove


# Computes the first instance of similarity matrix between all the operations
def compute_initial_similarity_matrix():
    already_computed = [g for g in graph]
    similarity_matrix = {}
    service_indices = {}
    i = 0
    for o1 in graph:
        for o2 in already_computed:
            if o1 == o2:
                continue
            else:
                service_indices.update({i: ([o1], [o2])})
                similarity_matrix.update({i: compute_ms_similarity([o1], [o2])})
                i += 1
        already_computed.remove(o1)
    return similarity_matrix, service_indices


# Recomputes the similarity matrix after a cluster merging
def recompute_similarity_matrix(microservices):
    already_computed = copy.deepcopy(microservices)
    similarity_matrix = {}
    service_indices = {}
    i = 0
    for o1 in microservices:
        for o2 in already_computed:
            if o1 == o2:
                continue
            else:
                service_indices.update({i: (o1, o2)})
                similarity_matrix.update({i: compute_ms_similarity(o1, o2)})
                i += 1
        already_computed.remove(o1)
    return similarity_matrix, service_indices


# Elects the primary replicas as the replicas in the microservice where they're accessed the most frequently by high
# consistency operations, or simply accessed the most frequently if there are no high consistency operations accessing them
def elect_primary_replicas(microservices):
    for m in microservices:
        for n in m:
            if n >= op_num:
                replica_locations.update({n: []})
    for m in microservices:
        for n in m:
            if n >= op_num:
                replica_locations.get(n).append(microservices.index(m))
    for e in replica_locations:
        count = []
        i = 0
        for l in replica_locations.get(e):
            count.append(0)
            for n in microservices[l]:
                if n < op_num:
                    if n in edges_from_e_to_o.get(e) and nodes_dict.get(n).get_consistency() == 'S':
                        count[i] += nodes_dict.get(n).get_frequency()
            i += 1
        if max(count) != 0:
            index_of_primary = count.index(max(count))
            for n in microservices[replica_locations.get(e)[index_of_primary]]:
                if n <= op_num:
                    op_index = n
                    break
            primary_replicas_locations.update({e: op_index})
            primary_replicas_microservices.update({e: replica_locations.get(e)[index_of_primary]})
        else:
<<<<<<< Updated upstream:main.py
            total_count = []
            i = 0
            for l in replica_locations.get(e):
                total_count.append(0)
                for n in microservices[l]:
                    if n < op_num:
                        if n in edges_from_e_to_o.get(e):
                            total_count[i] += nodes_dict.get(n).get_frequency()
                i += 1
                index_of_primary = total_count.index(max(total_count))
                op_index = -1
                for n in microservices[replica_locations.get(e)[index_of_primary]]:
                    if n <= op_num:
                        op_index = n
                        break
                primary_replicas_locations.update({e: op_index})
                primary_replicas_microservices.update({e: replica_locations.get(e)[index_of_primary]})


# Creates the dictionary mapping each secondary replica to a position in a chromosome
def list_secondary_replicas(microservices):
    i = 0
=======
            elect_s(a, microservices)
    return

def elect_s(attribute, microservices):
>>>>>>> Stashed changes:preprocessing.py
    for m in microservices:
        m_index = microservices.index(m)
        for n in m:
            if n >= op_num:
                if primary_replicas_microservices.get(n) != m_index:
                    secondary_replicas_indices.update({(n, m_index): i})
                    i += 1


# If the replica is only read by low consistency ops in its microservice, then it's an unexpensive replica and can be
# replicated without cost, so it doesn't need to be considered in the genetic algorithm
def trim_unexpensive_replicas(microservices):
    to_remove = []
    for s in secondary_replicas_indices:
        expensive = False
        replica = s[0]
        ops = [x for x in microservices[s[1]] if x < op_num]
        for o in ops:
            if relationship_dict.get((o, replica)):
                if relationship_dict.get((o, replica)) == 'W' or nodes_dict.get(o).get_consistency == 'S':
                    expensive = True
                    break
        if not expensive:
            to_remove.append(s)
    for t in to_remove:
        secondary_replicas_indices.pop(t)
    i = 0
    for s in secondary_replicas_indices:
        secondary_replicas_indices.update({s: i})
        i += 1


# Computes the replication cost of a replica as 2 * write frequency in same microservice * num of microservices where such
# replica is present and accessed by high consistency operations. It essentially means the number of messages we would need
# to exchange in a synchronous protocol to keep all those replicas updated.
def compute_repl_costs(replica, microservices, chromosome):
    ops_in_same_m = [x for x in microservices[replica[1]] if x < op_num]
    write_frequency = 0
    for o in ops_in_same_m:
        if relationship_dict.get((o, replica[0])) == 'W':
            write_frequency += nodes_dict.get(o).get_frequency()
    if write_frequency == 0:
        return 0
<<<<<<< Updated upstream:main.py
    num_hc_microservices = 0
    for l in replica_locations.get(replica[0]):
        index_in_chromosome = secondary_replicas_indices.get((replica[0], l))
        if index_in_chromosome and not chromosome[index_in_chromosome]:
            continue
        if l != replica[1]:
            ops = [x for x in microservices[l] if x < op_num]
            for o in ops:
                if relationship_dict.get((o, replica[0])) and nodes_dict.get(o).get_consistency() == 'S':
                    num_hc_microservices += 1
                    break
    return num_hc_microservices * 2 * write_frequency


# Computes the communication costs of a replica (the costs which occur if the replica is eliminated), as
# 2 * access frequency in the same microservice * num of microservices where such replica is present and accessed
# by high consistency operations. Essentially we might have one less microservice to update (since we just eliminated
# the replica in such service) but we have to pay the access frequency to contact the primary replica in another
# service.
def compute_comm_cost(replica, microservices, chromosome):
    ops_in_same_m = [x for x in microservices[replica[1]] if x < op_num]
    access_frequency = 0
    write_frequency = 0
    for o in ops_in_same_m:
        if relationship_dict.get((o, replica[0])):
            access_frequency += nodes_dict.get(o).get_frequency()
            if relationship_dict.get((o, replica[0])) == 'W':
                write_frequency += nodes_dict.get(o).get_frequency()
    if write_frequency == 0:
        return access_frequency
    num_hc_microservices = 0
    for l in replica_locations.get(replica[0]):
        index_in_chromosome = secondary_replicas_indices.get((replica[0], l))
        if index_in_chromosome and chromosome[index_in_chromosome] == 0:
            continue
        if l != replica[1]:
            ops = [x for x in microservices[l] if x < op_num]
            for o in ops:
                if relationship_dict.get((o, replica[0])) and nodes_dict.get(o).get_consistency() == 'S':
                    num_hc_microservices += 1
                    break
    return 2 * access_frequency + num_hc_microservices * 2 * write_frequency


# Sum of replication (if replica is present) and communication (if it was eliminated) costs for all secondary replicas
def evaluate_fitness(microservices, chromosome):
    i = 0
    fitness = 0
    for s in secondary_replicas_indices:
        if chromosome[i]:
            cost = compute_repl_costs(s, microservices, chromosome)
=======
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
    print(sim)
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
        print(len(ops))
        suca += len(ops)
    print(sim)
    print(op_num)
    print(suca)
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
>>>>>>> Stashed changes:preprocessing.py
        else:
            cost = compute_comm_cost(s, microservices, chromosome)
        fitness += cost
        i += 1
    return fitness


# Roulette wheel selections with probabilities inversely proportional to fitness (since fitness must be minimized)
def roulette_wheel_selection(fitness_chr_tuples):
    fitnesses = []
    generation = []
    for f in fitness_chr_tuples:
        generation.append(f[0])
        fitnesses.append(f[1])
    max = sum(1 / f for f in fitnesses)
    probs = [(1 / f) / max for f in fitnesses]
    mother = generation[np.random.choice(len(generation), p=probs)]
    father = generation[np.random.choice(len(generation), p=probs)]
    while mother == father:
        mother = generation[np.random.choice(len(generation), p=probs)]
        father = generation[np.random.choice(len(generation), p=probs)]
    return mother, father


# Random crossover between chromosomes
def crossover(mother, father, mutchance):
    i = 0
    son = []
    for g in mother:
        if random.randint(0, 100) <= mutchance:
            son.append(random.choice([0, 1]))
        else:
            choice = [mother[i], father[i]]
            son.append(random.choice(choice))
        i += 1
    return son


if __name__ == '__main__':
<<<<<<< Updated upstream:main.py
    # parse_arch_json('pangaeaArch.json')
    parse_arch_yaml('pangeaArch2.yaml')
    op_num = len(graph)

    to_remove = noise_removal()
    graph_copy = Graph()
=======
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
    """
    sc = [
        ["createNewPriceConfig", "findPriceConfigById", "findByRouteIdAndTrainType", "findAllPriceConfig", "deletePriceConfig", "updatePriceConfig"],
        ["cancelOrderbyUser", "ticketExecute", "ticketCollect", "getSoldTickets", "createOrder", "cancelOrder", "deleteOrder", "updateOrder", "modifyOrderStatus", "getOrderPrice", "payOrder", "initOrder", "checkOrderValidity", "preserve", "rebook", "distributeSeat", "getLeftTicketOfInterval", "checkSecurityConfig", "getTickets"],
        ["queryForTravel", "getCheapestTravelResult", "getQuickestTravelResult", "getMinStopTravelResult", "createTrip", "getRouteByTripId", "getTrainTypeByTripId", "retrieveTrip", "updateTrip", "deleteTrip"],
        ["getAllAssuranceTypes", "getAllAssurances", "findAssuranceById", "findAssuranceByOrderId", "createAssurance", "deleteAssuranceById", "deleteAssuranceByOrderId", "modifyAssurance"],
        ["saveUser", "getAllUser", "findByUserId", "findByUsername", "updateUser"],
        ["deleteUserById"],
        ["createConfig", "updateConfig", "queryConfig", "deleteConfig", "queryAllConfigs"],
        ["findAllSecurityConfig", "addNewSecurityConfig", "deleteSecurityConfig"],
        ["modifySecurityConfig"],
        ["getPriceByWeightAndRegion", "queryConsignPrice", "createAndModifyPrice", "getConsignPrice", "insertConsignRecord", "updateConsignRecord", "queryConsignByAccountId", "queryConsignByOrderId", "queryConsignByConsignee"],
        ["addVoucher", "queryVoucher"],
        ["createFoodOrdersInBatch", "createFoodOrder", "deleteFoodOrder", "findFoodOrderByOrderId", "findAllFoodOrders", "updateFoodOrder"],
        ["getAllOffices", "getSpecificOffice", "addOffice", "deleteOffice", "updateOffice"],
        ["queryForStationId", "createStation", "existStation", "updateStation", "deleteStation", "queryStations", "queryStationById"] ,
        ["calculateRefund", "pay", "createPaymentAccount", "addMoney", "queryPaymentAccount", "queryPayments", "drawBack", "payDifference", "queryMoney", "payDifferenceRebook"],
        ["initPayment"],
        ["findContactsById", "findContactsByAccountId", "createContact", "deleteContact", "modifyContact", "getAllContacts"],
        ["createTrainFood", "listTrainFood", "listTrainFoodByTripIds"],
        ["createFoodStore", "listFoodStores", "listFoodStoredByStationId", "getAllFoods"],
        ["searchCheapestRouteResult", "searchMinStopRouteResult", "searchQuickestRouteResult", "createAndModifyRoute", "getRouteById", "getRouteByStartAndTerminal", "createTrain", "retrieveTrain", "queryTrains", "updateTrain", "deleteTrain", "getAllRoutes"],
        ["processDelivery"]
    ]
    for s in sc:
        print(str(s).replace("'", '').replace('[', '').replace(']', ';'))
    exit(-1)
    manual = []
    for s in sc:
        serv = []
        for o in s:
            found = False
            for n in nodes_dict:
                if nodes_dict.get(n).get_name() == o:
                    serv.append(n)
                    found = True
            if not found:
                print("Not found " + o)
        manual.append(serv)
        print(len(serv))

    for o in range(0, len(graph)):
        count = 0
        for s in manual:
            count += s.count(o)
        if count == 0:
            print(str(o) + " not found " + "(" + nodes_dict.get(o).get_name() + ")")
        if count > 1:
            print(str(o) + " duplicate " + "(" + nodes_dict.get(o).get_name() + ")")
    to_remove = []
    for n in manual:
        rem = []
        for y in n:
            if isinstance(y, str):
                rem.append(y)
        to_remove.append(rem)
    i = 0
    for n in manual:
        for t in to_remove[i]:
            n.remove(t)
>>>>>>> Stashed changes:preprocessing.py

    # Trims the useless operations from the architecture
    for t in to_remove:
        graph.pop(t)
        nodes_dict.pop(t)
        op_reads.pop(t)
        op_writes.pop(t)

<<<<<<< Updated upstream:main.py
    model = 2
    if model == 2:
        # Lists the high consistency write operations
        hc_writes = []
        for o in op_writes:
            if nodes_dict.get(o).get_consistency() == 'S':
                hc_writes.append(o)
        # Lists the columns which are written
        written_columns = []
        for o in hc_writes:
                for x in op_writes.get(o):
                    written_columns.append(x)
        written_columns = list(set(written_columns))

        # Creates the "writing" services
        starting_services = []
        for c in written_columns:
            this_col = []
            for o in hc_writes:
                if c in op_writes.get(o):
                    this_col.append(o)
            already_added = False
            for s in starting_services:
                if this_col == s:
                    already_added = True
            if not already_added:
                starting_services.append(this_col)
        for o in hc_writes:
            indices = []
            for s in starting_services:
                if o in s:
                    indices.append(starting_services.index(s))
            new_s = []
            indices = list(set(indices))
            for i in indices:
                new_s += starting_services[i]
            new_s = list(set(new_s))
            list.sort(indices, reverse=True)
            for i in indices:
                starting_services.remove(starting_services[i])
            starting_services.append(new_s)
        to_remove = []
        writing_services = []
        for s in starting_services:
            if s:
                writing_services.append(starting_services[starting_services.index(s)])

        # Associates each written column with its writing service
        col_ws = {}
        for w in written_columns:
            for s in writing_services:
                for s2 in s:
                    if w in op_writes.get(s2):
                        col_ws.update({w: writing_services.index(s)})
                        break
        print(col_ws)
        print(writing_services)
        services = []
        for m in writing_services:
            new_s = []
            for o in m:
                new_s += [o] + graph.get(o)
            new_s = list(set(new_s))
            services.append(new_s)

        elect_primary_replicas(services)
        list_secondary_replicas(services)
        format_and_draw(services, op_num, 'suga.html')
        exit(-1)




    if model == 0:
        similarity_matrix, service_indices = compute_initial_similarity_matrix()
        microservices = [[g] for g in graph]
        while len(microservices) > 15:
            candidate_index = max(similarity_matrix, key=similarity_matrix.get)
            if similarity_matrix.get(candidate_index) <= 0:
                break
            candidate = service_indices.get(candidate_index)
            print(str(candidate) + " are the candidates to be joined, with score " + str(
                similarity_matrix.get(candidate_index)))
            new_m = []
            for c in candidate:
                for c2 in c:
                    new_m.append(c2)
                microservices.remove(c)
            microservices.append(new_m)
            similarity_matrix, service_indices = recompute_similarity_matrix(microservices)
            print(similarity_matrix)
            print(len(microservices))
            print(microservices)
            print("COUPLING SCORE " + str(compute_coupling_score(microservices)))
            print("INTRA-SERVICE COHESION SCORE " + str(compute_intraservice_cohesion(microservices)))
            print("CC RATIO " + str(compute_coupling_score(microservices) / compute_intraservice_cohesion(microservices)))


        cc_ratio = compute_coupling_score(microservices) / compute_intraservice_cohesion(microservices)

        services = []
        for m in microservices:
            new_s = []
            for o in m:
                new_s += [o] + graph.get(o)
            new_s = list(set(new_s))
            services.append(new_s)

        elect_primary_replicas(services)
        list_secondary_replicas(services)
        trim_unexpensive_replicas(services)

        generation = []
        for i in range(0, 20):
            chromosome = []
            for s in secondary_replicas_indices:
                choice = random.choice([0, 1])
                chromosome.append(choice)
            generation.append(chromosome)

        for i in range(0, 100):
            fitness_chr_tuples = []
            for g in generation:
                fitness_chr_tuples.append((g, evaluate_fitness(microservices, g)))
            fitness_chr_tuples.sort(key=operator.itemgetter(1))
            print(fitness_chr_tuples)
            new_gen = []
            new_gen.append(fitness_chr_tuples[0][0])
            new_gen.append(fitness_chr_tuples[1][0])
            for i in range(0, 18):
                m, f = roulette_wheel_selection(fitness_chr_tuples)
                new_gen.append(crossover(m, f, 5))
            generation = new_gen

        print("FINAL SCORE = ", end='')
        print(evaluate_fitness(microservices, new_gen[0]) * cc_ratio)

        for x in secondary_replicas_indices:
            if secondary_replicas_indices.get(x) == 7:
                print(nodes_dict.get(x[0]).get_name())
                print([x for x in services[x[1]]])

        format_and_draw(services, op_num, "res.html", chr=new_gen[0])

    if model == 3:
        similarity_matrix, service_indices = compute_initial_similarity_matrix()
        microservices = [[g] for g in graph]
        while True:
            candidate_index = max(similarity_matrix, key=similarity_matrix.get)
            if similarity_matrix.get(candidate_index) != 1:
                break
            candidate = service_indices.get(candidate_index)
            print(str(candidate) + " are the candidates to be joined, with score " + str(
                similarity_matrix.get(candidate_index)))
            new_m = []
            for c in candidate:
                for c2 in c:
                    new_m.append(c2)
                microservices.remove(c)
            microservices.append(new_m)
            similarity_matrix, service_indices = recompute_similarity_matrix(microservices)
            print(similarity_matrix)
            print(len(microservices))
            print(microservices)
            print("COUPLING SCORE " + str(compute_coupling_score(microservices)))
            print("INTRA-SERVICE COHESION SCORE " + str(compute_intraservice_cohesion(microservices)))
            print(
                "CC RATIO " + str(compute_coupling_score(microservices) / compute_intraservice_cohesion(microservices)))

        cc_ratio = compute_coupling_score(microservices) / compute_intraservice_cohesion(microservices)

        services = []
        for m in microservices:
            new_s = []
            for o in m:
                new_s += [o] + graph.get(o)
            new_s = list(set(new_s))
            services.append(new_s)

        elect_primary_replicas(services)
        list_secondary_replicas(services)
        trim_unexpensive_replicas(services)

        generation = []
        for i in range(0, 20):
            chromosome = []
            for s in secondary_replicas_indices:
                choice = random.choice([0, 1])
                chromosome.append(choice)
            generation.append(chromosome)

        for i in range(0, 100):
            fitness_chr_tuples = []
            for g in generation:
                fitness_chr_tuples.append((g, evaluate_fitness(microservices, g)))
            fitness_chr_tuples.sort(key=operator.itemgetter(1))
            print(fitness_chr_tuples)
            new_gen = []
            new_gen.append(fitness_chr_tuples[0][0])
            new_gen.append(fitness_chr_tuples[1][0])
            for i in range(0, 18):
                m, f = roulette_wheel_selection(fitness_chr_tuples)
                new_gen.append(crossover(m, f, 5))
            generation = new_gen

        print("FINAL SCORE = ", end='')
        print(evaluate_fitness(microservices, new_gen[0]) * cc_ratio)

        for x in secondary_replicas_indices:
            if secondary_replicas_indices.get(x) == 7:
                print(nodes_dict.get(x[0]).get_name())
                print([x for x in services[x[1]]])

        format_and_draw(services, op_num, "res.html", chr=new_gen[0])
        print(len(services))
=======
    manual_final = []
    for micro in manual:
        accesses = []
        for n in micro:
            accesses_temp = []
            accesses_temp += op_reads.get(n) + op_writes.get(n)
            for a in accesses_temp:
                accesses.append(attributes_ntoi.get(a))
        manual_final.append(micro + list(set(accesses)))
    elect_primary_replicas(manual_final)
    cached_a = {}
    uncached_a = {}
    tot_rop = 0
    for a in attributes:
        c_a = []
        u_a = []
        for micro in manual_final:
            if a in micro and primary_replicas_locations.get(a) != manual_final.index(micro):
                read_in_same = 0
                write_in_others = 0
                for o in micro:
                    if o < 10000 and attributes_iton.get(a) in op_reads.get(o):
                        read_in_same += nodes_dict.get(o).get_frequency()
                for micro2 in manual_final:
                    for o in micro2:
                        if o < 10000 and attributes_iton.get(a) in op_writes.get(o):
                            write_in_others += nodes_dict.get(o).get_frequency()
                if read_in_same <= write_in_others:
                    tot_rop += read_in_same
                    u_a.append(manual_final.index(micro))
                else:
                    tot_rop += write_in_others
                    c_a.append(manual_final.index(micro))
        cached_a.update({a: c_a})
        uncached_a.update({a: u_a})
    right_format = []
    for micro in manual:
        new_serv = [] + micro
        for a in attributes:
            if manual.index(micro) in cached_a.get(a):
                new_serv.append(str(a) + 'R')
            if manual.index(micro) in uncached_a.get(a):
                new_serv.append(str(a) + 'N')
            if manual.index(micro) == primary_replicas_locations.get(a):
                new_serv.append(str(a) + 'P')
        right_format.append(new_serv)
    print(right_format)
    print(manual)
    format_and_draw_final(right_format, "formatted_manual.html")
    print(compute_total_coupling(manual))
    print(compute_communication_cost(manual_final)/max_com_cost)
    exit(-1)
    """
    print(len(attributes))
    write_dat_file(4)

    """
    manual = [[67, 52, 41, 24, 48, 68, 8, 46, 36, 7, 26, 25, 34, 35, 51, 47, 64], [29, 21, 32, 3, 4, 9, 55, 61, 0, 5, 1, 2, 6, 63],
              [45, 53, 33, 54, 38, 10, 17, 65, 28, 17, 27, 20], [15, 16, 60, 49, 66, 39, 37, 31, 62, 12, 18, 13, 59, 42, 40, 14, 19, 57, 43, 44, 56, 30, 50, 11, 22, 23, 58]]
    manual_final = []
    for m in manual:
        accesses = []
        for n in m:
            accesses_temp = []
            accesses_temp += op_reads.get(n) + op_writes.get(n)
            for a in accesses_temp:
                accesses.append(attributes_ntoi.get(a))
        manual_final.append(m + list(set(accesses)))
    format_and_draw_complete(manual_final, "manual.html")
    elect_primary_replicas(manual_final)
    print(compute_communication_cost(manual_final))
    print(compute_total_coupling(manual_final))
    """
    """

    print(max_com_cost)

    op = 0.2
    coup = 0.8
    while coup < 1.001:
        opt_result = abstractSolver.optimizer(op_num, max_com_cost, min_decoupling_bound, max_decoupling_bound,
                                          op, coup)
        op -= 0.05
        coup += 0.05
    """
    alpha = 0.0
    while alpha <= 1:
        opt_result = abstractSolverFinalLinear.optimizer(op_num, max_com_cost, alpha)
        alpha += 0.1

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
>>>>>>> Stashed changes:preprocessing.py
