import pyomo.environ as pyo
from pyomo.util.infeasible import log_infeasible_constraints
from itertools import product


def optimizer(op_num, max_com_cost, alpha):
    model = pyo.AbstractModel()
    opt = pyo.SolverFactory('gurobi', solver_io="lp")
    M = 10000

    ######################
    # INPUT VARIABLES #
    ######################

    # set of ENTITIES
    model.ENTITIES = pyo.Set()

    # set of operations
    model.OPERATIONS = pyo.Set()

    # num of available microservices
    model.MICROSERVICES = pyo.Set()

    # operation frequencies
    model.frequencies = pyo.Param({'F'}, model.OPERATIONS, within=pyo.Integers)

    # matrix of dependencies between operations and ENTITIES
    model.acc = pyo.Param(model.OPERATIONS, model.ENTITIES, within=pyo.Binary)

    # matrix of dependencies between operations and ENTITIES
    model.accr = pyo.Param(model.OPERATIONS, model.ENTITIES, within=pyo.Binary)

    # matrix of dependencies between operations and ENTITIES
    model.accrw = pyo.Param(model.OPERATIONS, model.ENTITIES, within=pyo.Binary)

    # matrix of dependencies between operations and operations
    model.coloc = pyo.Param(model.OPERATIONS, model.OPERATIONS, within=pyo.Binary)

    # vector representing if an operation has transactional requirements
    model.tr = pyo.Param({'T'}, model.OPERATIONS, within=pyo.Binary)

    # matrix representing similarity between pairs of operations
    model.similarity = pyo.Param(model.OPERATIONS, model.OPERATIONS, within=pyo.Reals)

    ######################
    # DECISION VARIABLES #
    ######################

    # True iff operation o is in microservice m
    model.x = pyo.Var(model.OPERATIONS, model.MICROSERVICES, within=pyo.Binary)

    # True iff attribute a is in microservice m
    model.y = pyo.Var(model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    # True iff attribute a has primary location in service m
    model.l = pyo.Var(model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    ########################
    #  AUXILIARY VARIABLES #
    ########################

    # Variable which is true when two operations are in the same service (needed by colocated operations and cohm constraints)
    model.same_location = pyo.Var(model.OPERATIONS, model.OPERATIONS, model.MICROSERVICES, within=pyo.Binary)

    # Variable to linearize product of x and acc
    model.accesses_e_in_m = pyo.Var(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    # Variable to linearize product of booleans in transactional constraint
    model.transactional = pyo.Var(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    # Variable to linearize product between same_location and similarity (used by cohm constraint)
    model.similarity_if_in_same_location = pyo.Var(model.OPERATIONS, model.OPERATIONS, model.MICROSERVICES, bounds=(0, 1), within=pyo.Reals)

    # Variable to replace division in cohm computation
    model.cohesion_temp = pyo.Var(model.MICROSERVICES, bounds=(0, 1), within=pyo.Reals)

    # Variable to compute boolean and for ROP computation (to determine if an entity is read remotely) (needed by rop computation)
    model.reads_from_remote = pyo.Var(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    # Variable to store frequency of operations if it reads from remote (needed by rop computation)
    model.read_frequency_from_remote = pyo.Var(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, within=pyo.Integers)

    # Variable to compute boolean and for WOP computation (to determine if a leader is written remotely) (needed by wop computation)
    model.writes_from_remote = pyo.Var(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    # Variable to store frequency of operations if it writes a leader from remote (needed by wop computation)
    model.write_frequency_from_remote = pyo.Var(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, within=pyo.Integers)

    # Variable to store frequency of operation if it writes entity e (needed by repl computation)
    model.write_frequency = pyo.Var(model.OPERATIONS, model.ENTITIES, within=pyo.Integers)

    # Cohesion metric of a single microservice
    model.cohm = pyo.Var(model.MICROSERVICES, bounds=(0, 1), within=pyo.Reals)

    # Read operational cost of a operation-entity pair
    model.rop = pyo.Var(model.OPERATIONS, model.ENTITIES, within=pyo.Integers)

    # Write operational cost of a operation-entity pair
    model.wop = pyo.Var(model.OPERATIONS, model.ENTITIES, within=pyo.Integers)

    # Replication cost for an entity
    model.repl = pyo.Var(model.ENTITIES, within=pyo.Integers)

    ########################
    #     CONSTRAINTS      #
    ########################

    # Each operation is deployed on exactly one microservice

    def lone_operation_constraint(mod, o):
        return sum(mod.x[o, m] for m in mod.MICROSERVICES) == 1

    model.LoneOperationConstraint = pyo.Constraint(model.OPERATIONS, rule=lone_operation_constraint)

    # Each entity is deployed on at least one microservice

    def at_least_one_replica_constraint(mod, e):
        return sum(mod.y[e, m] for m in mod.MICROSERVICES) >= 1

    model.AtLeastOneReplicaConstraint = pyo.Constraint(model.ENTITIES, rule=at_least_one_replica_constraint)

    # Each entity has exactly one leader replica

    def lone_leader_constraint(mod, e):
        return sum(mod.l[e, m] for m in mod.MICROSERVICES) == 1

    model.LoneLeaderConstraint = pyo.Constraint(model.ENTITIES, rule=lone_leader_constraint)

    # Leader replica is a replica

    def leader_is_replica_constraint(mod, e, m):
        return mod.y[e, m] >= mod.l[e, m]

    model.LeaderIsReplicaConstraint = pyo.Constraint(model.ENTITIES, model.MICROSERVICES,
                                                     rule=leader_is_replica_constraint)

    # Replica can be present only if it is accessed by at least one operation in that microservice

    def and1_accessed_in_microservice_constraint(mod, o, e, m):
        return mod.accesses_e_in_m[o, e, m] >= mod.x[o, m] + mod.acc[o, e] - 1

    model.And1AccessedInMConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                      rule=and1_accessed_in_microservice_constraint)

    def and2_accessed_in_microservice_constraint(mod, o, e, m):
        return mod.accesses_e_in_m[o, e, m] <= mod.x[o, m]

    model.And2AccessedInMConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                      rule=and2_accessed_in_microservice_constraint)

    def and3_accessed_in_microservice_constraint(mod, o, e, m):
        return mod.accesses_e_in_m[o, e, m] <= mod.acc[o, e]

    model.And3AccessedInMConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                      rule=and3_accessed_in_microservice_constraint)

    def accessed_in_microservice_constraint1(mod, e, m):
        return mod.y[e, m] <= sum(mod.accesses_e_in_m[o, e, m] for o in mod.OPERATIONS)

    model.AccessedInMicroservice1 = pyo.Constraint(model.ENTITIES, model.MICROSERVICES,
                                              rule=accessed_in_microservice_constraint1)


    # And linearization to represent operation couple in same service (used for colocated operation and cohm constraints)

    def and1_same_location_constraint(mod, o1, o2, m):
        return mod.same_location[o1, o2, m] >= mod.x[o1, m] + mod.x[o2, m] - 1

    model.And1SameLocationConstraint = pyo.Constraint(model.OPERATIONS, model.OPERATIONS, model.MICROSERVICES, rule=and1_same_location_constraint)

    def and2_same_location_constraint(mod, o1, o2, m):
        return mod.same_location[o1, o2, m] <= mod.x[o1, m]

    model.And2SameLocationConstraint = pyo.Constraint(model.OPERATIONS, model.OPERATIONS, model.MICROSERVICES, rule=and2_same_location_constraint)

    def and3_same_location_constraint(mod, o1, o2, m):
        return mod.same_location[o1, o2, m] <= mod.x[o2, m]

    model.And3SameLocationConstraint = pyo.Constraint(model.OPERATIONS, model.OPERATIONS, model.MICROSERVICES, rule=and3_same_location_constraint)

    # Colocated operations need to be in the same service

    def colocated_operations_constraint(mod, o1, o2):
        return sum(mod.same_location[o1, o2, m] for m in mod.MICROSERVICES) >= mod.coloc[o1, o2]

    model.ColocatedOperationsConstraint = pyo.Constraint(model.OPERATIONS, model.OPERATIONS,
                                                         rule=colocated_operations_constraint)

    # And linearization for transactional constraint

    def and1_transactional_constraint(mod, o, e, m):
        return mod.transactional[o, e, m] >= mod.tr['T', o] + mod.acc[o, e] + mod.l[e, m] - 2

    model.And1TransactionalConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                            rule=and1_transactional_constraint)

    def and2_transactional_constraint(mod, o, e, m):
        return mod.transactional[o, e, m] <= mod.tr['T', o]

    model.And2TransactionalConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                            rule=and2_transactional_constraint)

    def and3_transactional_constraint(mod, o, e, m):
        return mod.transactional[o, e, m] <= mod.acc[o, e]

    model.And3TransactionalConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                            rule=and3_transactional_constraint)

    def and4_transactional_constraint(mod, o, e, m):
        return mod.transactional[o, e, m] <= mod.l[e, m]

    model.And4TransactionalConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                            rule=and4_transactional_constraint)

    # Transactional operations need to be where leader is located

    def transactional_constraint(mod, o, e, m):
        return mod.x[o, m] >= mod.transactional[o, e, m]

    model.TransactionalConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                   rule=transactional_constraint)

    # Constraints needed to linearize product of similarity and same_location (for cohm constraint)

    def similarity_if_in_same_location_constraint1(mod, o1, o2, m):
        return mod.similarity_if_in_same_location[o1, o2, m] - mod.similarity[o1, o2] <= (1 - mod.same_location[o1, o2, m]) * M

    model.SimilarityIfInSameLocationConstraint1 = pyo.Constraint(model.OPERATIONS, model.OPERATIONS, model.MICROSERVICES,
                                       rule=similarity_if_in_same_location_constraint1)

    def similarity_if_in_same_location_constraint2(mod, o1, o2, m):
        return - mod.similarity_if_in_same_location[o1, o2, m] + mod.similarity[o1, o2] <= (1 - mod.same_location[o1, o2, m]) * M

    model.SimilarityIfInSameLocationConstraint2 = pyo.Constraint(model.OPERATIONS, model.OPERATIONS,
                                                                 model.MICROSERVICES,
                                                                 rule=similarity_if_in_same_location_constraint2)
   
    def similarity_if_in_same_location_constraint3(mod, o1, o2, m):
        return mod.similarity_if_in_same_location[o1, o2, m] <= mod.same_location[o1, o2, m] * M


    model.SimilarityIfInSameLocationConstraint3 = pyo.Constraint(model.OPERATIONS, model.OPERATIONS, model.MICROSERVICES,
                                                       rule=similarity_if_in_same_location_constraint3)
    
    def similarity_if_in_same_location_constraint4(mod, o1, o2, m):
        return - mod.similarity_if_in_same_location[o1, o2, m] <= mod.same_location[o1, o2, m]

    model.SimilarityIfInSameLocationConstraint4 = pyo.Constraint(model.OPERATIONS, model.OPERATIONS,
                                                                 model.MICROSERVICES,
                                                                 rule=similarity_if_in_same_location_constraint4)

    # Constraint needed to compute cohm by replacing the division

    def cohesion_linearization_constraint(mod, m):
        return mod.cohesion_temp[m] * sum(mod.same_location[o1, o2, m] for o1, o2 in product(mod.OPERATIONS, mod.OPERATIONS)) == sum(mod.similarity_if_in_same_location[o1, o2, m]
                                              for o1, o2 in product(mod.OPERATIONS, mod.OPERATIONS))

    model.CohesionLinearizationConstraint = pyo.Constraint(model.MICROSERVICES, rule=cohesion_linearization_constraint)

    def cohm(mod, m):
        return mod.cohm[m] == mod.cohesion_temp[m] * sum(mod.x[o, m] for o in mod.OPERATIONS)/op_num

    model.Cohm= pyo.Constraint(model.MICROSERVICES, rule=cohm)


    # And constraints to linearize boolean products in Read operational cost computation

    def and_rop_constraint1(mod, o, e, m):
        return mod.reads_from_remote[o, e, m] >= mod.accr[o, e] + mod.x[o, m] + (1 - mod.y[e, m]) - 2

    model.AndRopConstraint1 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, rule=and_rop_constraint1)

    def and_rop_constraint2(mod, o, e, m):
        return mod.reads_from_remote[o, e, m] <= mod.accr[o, e]

    model.AndRopConstraint2 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                             rule=and_rop_constraint2)

    def and_rop_constraint3(mod, o, e, m):
        return mod.reads_from_remote[o, e, m] <= mod.x[o, m]

    model.AndRopConstraint3 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                             rule=and_rop_constraint3)

    def and_rop_constraint4(mod, o, e, m):
        return mod.reads_from_remote[o, e, m] <= (1 - mod.y[e, m])

    model.AndRopConstraint4 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                             rule=and_rop_constraint4)

    # Constraint needed to save into a variable the frequency if the operation o reads entity e from remote location

    def read_frequency_from_remote_constraint1(mod, o, e, m):
        return mod.read_frequency_from_remote[o, e, m] - mod.frequencies['F', o] <= (
                    1 - mod.reads_from_remote[o, e, m]) * M

    model.ReadFrequencyFromRemoteConstraint1 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                                 model.MICROSERVICES,
                                                                 rule=read_frequency_from_remote_constraint1)

    def read_frequency_from_remote_constraint2(mod, o, e, m):
        return - mod.read_frequency_from_remote[o, e, m] + mod.frequencies['F', o] <= (
                1 - mod.reads_from_remote[o, e, m]) * M

    model.ReadFrequencyFromRemoteConstraint2 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                              model.MICROSERVICES,
                                                              rule=read_frequency_from_remote_constraint2)

    def read_frequency_from_remote_constraint3(mod, o, e, m):
        return mod.read_frequency_from_remote[o, e, m] <= mod.reads_from_remote[o, e, m] * M

    model.ReadFrequencyFromRemoteConstraint3 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                              model.MICROSERVICES,
                                                              rule=read_frequency_from_remote_constraint3)

    def read_frequency_from_remote_constraint4(mod, o, e, m):
        return - mod.read_frequency_from_remote[o, e, m] <= mod.reads_from_remote[o, e, m]

    model.ReadFrequencyFromRemoteConstraint4 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                              model.MICROSERVICES,
                                                              rule=read_frequency_from_remote_constraint4)

    # Read operational costs

    def rop_comp(mod, o, e):
        return mod.rop[o, e] == sum(mod.read_frequency_from_remote[o, e, m] for m in mod.MICROSERVICES)

    model.RopComp = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=rop_comp)

    # And constraints to linearize boolean products in Write operational cost computation

    def and_wop_constraint1(mod, o, e, m):
        return mod.writes_from_remote[o, e, m] >= mod.accrw[o, e] + mod.x[o, m] + (1 - mod.l[e, m]) - 2

    model.AndWopConstraint1 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, rule=and_wop_constraint1)

    def and_wop_constraint2(mod, o, e, m):
        return mod.writes_from_remote[o, e, m] <= mod.accrw[o, e]

    model.AndWopConstraint2 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                             rule=and_wop_constraint2)

    def and_wop_constraint3(mod, o, e, m):
        return mod.writes_from_remote[o, e, m] <= mod.x[o, m]

    model.AndWopConstraint3 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                             rule=and_wop_constraint3)

    def and_wop_constraint4(mod, o, e, m):
        return mod.writes_from_remote[o, e, m] <= (1 - mod.l[e, m])

    model.AndWopConstraint4 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                             rule=and_wop_constraint4)

    # Constraint needed to save into a variable the frequency if the operation o writes leader of entity e from remote location

    def write_frequency_from_remote_constraint1(mod, o, e, m):
        return mod.write_frequency_from_remote[o, e, m] - mod.frequencies['F', o] <= (
                    1 - mod.writes_from_remote[o, e, m]) * M

    model.WriteFrequencyFromRemoteConstraint1 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                                 model.MICROSERVICES,
                                                                 rule=write_frequency_from_remote_constraint1)

    def write_frequency_from_remote_constraint2(mod, o, e, m):
        return - mod.write_frequency_from_remote[o, e, m] + mod.frequencies['F', o] <= (
                1 - mod.writes_from_remote[o, e, m]) * M

    model.WriteFrequencyFromRemoteConstraint2 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                              model.MICROSERVICES,
                                                              rule=write_frequency_from_remote_constraint2)

    def write_frequency_from_remote_constraint3(mod, o, e, m):
        return mod.write_frequency_from_remote[o, e, m] <= mod.writes_from_remote[o, e, m] * M

    model.WriteFrequencyFromRemoteConstraint3 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                              model.MICROSERVICES,
                                                              rule=write_frequency_from_remote_constraint3)

    def write_frequency_from_remote_constraint4(mod, o, e, m):
        return - mod.write_frequency_from_remote[o, e, m] <= mod.writes_from_remote[o, e, m]

    model.WriteFrequencyFromRemoteConstraint4 = pyo.Constraint(model.OPERATIONS, model.ENTITIES,
                                                              model.MICROSERVICES,
                                                              rule=write_frequency_from_remote_constraint4)

    # Write operational costs

    def wop_comp(mod, o, e):
        return mod.wop[o, e] == sum(mod.write_frequency_from_remote[o, e, m] for m in mod.MICROSERVICES)

    model.Wop = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=wop_comp)

    # Constraint needed to save into a variable the frequency if the operation o writes entity e (from any location)

    def write_frequency_constraint1(mod, o, e):
        return mod.write_frequency[o, e] - mod.frequencies['F', o] <= (1 - mod.accrw[o, e]) * M
    model.WriteFrequencyConstraint1 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=write_frequency_constraint1)

    def write_frequency_constraint2(mod, o, e):
        return - mod.write_frequency[o, e] + mod.frequencies['F', o] <= (1 - mod.accrw[o, e]) * M

    model.WriteFrequencyConstraint2 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=write_frequency_constraint2)

    def write_frequency_constraint3(mod, o, e):
        return mod.write_frequency[o, e] <= mod.accrw[o, e] * M

    model.WriteFrequencyConstraint3 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=write_frequency_constraint3)

    def write_frequency_constraint4(mod, o, e):
        return - mod.write_frequency[o, e] <= mod.accrw[o, e]

    model.WriteFrequencyConstraint4 = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=write_frequency_constraint4)

    # Replication costs

    def repl(mod, e):
        return mod.repl[e] == sum(
            mod.write_frequency[o, e] * (sum(mod.y[e, m] for m in mod.MICROSERVICES) - 1) for o in
            mod.OPERATIONS)

    model.Repl = pyo.Constraint(model.ENTITIES, rule=repl)

    ####    AUXILIARY STUFF FOR DEBUGGING PURPOSES    #####

    model.com = pyo.Var(within=pyo.Integers)

    model.coh = pyo.Var(within=pyo.Reals)

    model.total_rop = pyo.Var(within=pyo.Integers)

    model.total_repl = pyo.Var(within=pyo.Integers)

    model.total_wop = pyo.Var(within=pyo.Integers)

    def com_rule(mod):
        return mod.com == ((sum(mod.repl[e] for e in mod.ENTITIES)) + (sum(mod.wop[o, e] + mod.rop[o, e] for o, e in product(mod.OPERATIONS, mod.ENTITIES))))

    model.COM = pyo.Constraint(rule=com_rule)

    def coh_rule(mod):
        return mod.coh == sum(mod.cohm[m] for m in mod.MICROSERVICES)

    model.COH = pyo.Constraint(rule=coh_rule)

    def rop_rule(mod):
        return mod.total_rop == sum(mod.rop[o, e] for o, e in product(mod.OPERATIONS, mod.ENTITIES))

    model.total_rop_constr = pyo.Constraint(rule=rop_rule)

    def wop_rule(mod):
        return mod.total_wop == sum(mod.wop[o, e] for o, e in product(mod.OPERATIONS, mod.ENTITIES))

    model.total_wop_constr = pyo.Constraint(rule=wop_rule)

    def repl_rule(mod):
        return mod.total_repl == sum(mod.repl[e] for e in mod.ENTITIES)

    model.total_repl_constr = pyo.Constraint(rule=repl_rule)

    # Objective function

    def total_score(mod):
        return alpha * sum(mod.cohm[m] for m in mod.MICROSERVICES) - (1 - alpha) * ((sum(mod.repl[e] for e in mod.ENTITIES)) + (sum(mod.wop[o, e] + mod.rop[o, e] for o, e in product(mod.OPERATIONS, mod.ENTITIES)))) / max_com_cost

    model.obj = pyo.Objective(rule=total_score, sense=pyo.maximize)
    model.name = 'Microservices Decomposition'
    instance = model.create_instance('data.dat')
    # opt.options["mipgap"] = 10
    # opt.options['mipfocus'] = 1
    # opt.options['presolve'] = 2
    # opt.options['numericfocus'] = 1
    opt.options['timelimit'] = 604800
    # opt.options['method'] = 3
    result = opt.solve(instance, tee=True)
    log_infeasible_constraints(instance, log_expression=True)

    """
    instance.com.display()
    instance.coh.display()
    instance.total_rop.display()
    instance.total_wop.display()
    instance.total_repl.display()
    instance.similarity_if_in_same_location.display()
    instance.write_frequency.display()
    """
    arch = [[] for m in instance.MICROSERVICES]
    for o in instance.OPERATIONS:
        for m in instance.MICROSERVICES:
            if pyo.value(instance.x[o, m]) > 0:
                arch[int(m[1:])].append(int(o[1:]))
    for e in instance.ENTITIES:
        for m in instance.MICROSERVICES:
            s = str(int(e[1:]) + 100000)
            if pyo.value(instance.y[e, m]) > 0:
                if pyo.value(instance.l[e, m]) > 0:
                    arch[int(m[1:])].append(s + "P")
                else:
                    arch[int(m[1:])].append(s + "R")
            else:
                for o in instance.OPERATIONS:
                    if pyo.value(instance.acc[o, e]) > 0 and pyo.value(instance.x[o, m]) > 0:
                        arch[int(m[1:])].append(s + "N")
                        break

    result = []
    for a in arch:
        if a:
            result.append(a)
    print(result)

    f = open("results_new.txt", 'a')
    f.write(str(alpha))
    f.write("\n")
    f.write(str(1 - alpha))
    f.write("\n")
    f.write(str(instance.coh.value))
    f.write("\n")
    f.write(str(instance.com.value))
    f.write("\n")
    f.write(str(instance.coh.value * alpha - (1 - alpha) * instance.com.value / max_com_cost))
    f.write("\n")
    f.write(str(result))
    f.write("\n\n")
    f.close()

    return result

