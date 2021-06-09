import json
import copy
import operator
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


# Returns connected components of graph
def get_connected_components(gr):
    size = len(gr.get_nodes_dict())
    g = SparseGraph(size, frmt='lil')
    gra = gr.get_graph()
    for n in gra:
        for n2 in gra.get(n):
            g.addEdge(n, n2)
    return g.findConnectedComponents()


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
    # parse_arch_json('pangaeaArch.json')
    parse_arch_yaml('pangeaArch2.yaml')
    op_num = len(graph)

    to_remove = noise_removal()
    graph_copy = Graph()

    # Trims the useless operations from the architecture
    for t in to_remove:
        graph.pop(t)
        nodes_dict.pop(t)
        op_reads.pop(t)
        op_writes.pop(t)

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