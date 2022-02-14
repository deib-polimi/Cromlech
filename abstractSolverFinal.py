import pyomo.environ as pyo
from pyomo.util.infeasible import log_infeasible_constraints
from itertools import product

def optimizer(op_num, max_com_cost, alpha):
    model = pyo.AbstractModel()
    opt = pyo.SolverFactory('gurobi', solver_io="lp")

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

    # Cohesion metric of a single microservice
    model.cohm = pyo.Var(model.MICROSERVICES, bounds=(0, 1), within=pyo.Reals)

    # Cohesion metric of the whole architecture
    model.coh = pyo.Var(bounds=(0, 1), within=pyo.Reals)

    # Communication cost of the whole architecture
    model.com = pyo.Var(bounds=(0, 1), within=pyo.Reals)

    # Cohesion metric of a single microservice
    model.rop = pyo.Var(model.OPERATIONS, model.ENTITIES, within=pyo.Integers)

    # Cohesion metric of a single microservice
    model.wop = pyo.Var(model.OPERATIONS, model.ENTITIES, within=pyo.Integers)

    # Cohesion metric of a single microservice
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
        return mod.l[e, m] >= mod.y[e, m]

    model.LeaderIsReplicaConstraint = pyo.Constraint(model.ENTITIES, model.MICROSERVICES, rule=leader_is_replica_constraint)

    # Colocated operations need to be in the same service

    def colocated_operations_constraint(mod, o1, o2):
        return sum(mod.x[o1, m] * mod.x[o2,m] for m in mod.MICROSERVICES) == mod.coloc[o1, o2]

    model.ColocatedOperationsConstraint = pyo.Constraint(model.OPERATIONS, model.OPERATIONS,
                                                   rule=colocated_operations_constraint)

    # Transactional operations need to be where leader is located

    def transactional_constraint(mod, o, e, m):
        return mod.x[o, m] >= mod.tr['T', o] * mod.acc[o, e] * mod.l[e, m]

    model.TransactionalConstraint = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES,
                                                     rule=transactional_constraint)
    
    # Cohesion score for a single microservice
    
    def cohm(mod, m):
        return mod.cohm[m] == (sum(mod.similarity[o1, o2] * mod.x[o1, m] * mod.x[o2, m] for o1, o2 in product(mod.OPERATIONS, mod.OPERATIONS)) / sum(mod.x[o, m] for o in mod.OPERATIONS))

    model.Cohm = pyo.Constraint(model.MICROSERVICES, rule=cohm)

    # Cohesion score for the whole architecture

    def total_coh(mod):
        return mod.coh == sum(mod.cohm[m] for m in mod.MICROSERVICES) / op_num

    model.TotalCoh = pyo.Constraint(rule=total_coh)
    
    # Read operational costs

    def rop_comp(mod, o, e):
        return mod.rop[o, e] == sum(mod.accr[o, e] * mod.frequencies['F', o] * mod.x[o, m] * (1 - mod.y[e, m]) for m in mod.MICROSERVICES)

    model.Rop = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=rop_comp)

    # Write operational costs

    def wop_comp(mod, o, e):
        return mod.wop[o, e] == sum(mod.accrw[o, e] * mod.frequencies['F', o] * mod.x[o, m] * (1 - mod.l[e, m]) for m in mod.MICROSERVICES)

    model.Wop = pyo.Constraint(model.OPERATIONS, model.ENTITIES, rule=wop_comp)

    # Replication costs

    def repl_comp(mod, e):
        return mod.repl[e] == sum(mod.frequencies['F', o] * mod.accrw[o, e] * (sum(mod.y[e,m] for m in mod.MICROSERVICES) - 1) for o in mod.OPERATIONS)

    model.Repl = pyo.Constraint(model.ENTITIES, rule=repl_comp)

    # Total communication costs

    def total_com(mod):
        return mod.com == sum(mod.rop[o, e] + mod.wop[o, e] for o, e in product(mod.OPERATIONS, mod.ENTITIES)) + sum(mod.repl[e] for e in mod.ENTITIES)

    model.TotalCom = pyo.Constraint(rule=total_com)

    # Objective function

    def total_score(mod):
        return alpha * mod.coh - (1 - alpha) * mod.com/max_com_cost

    model.obj = pyo.Objective(rule=total_score, sense=pyo.maximize)
    model.name = 'Microservices Decomposition'
    instance = model.create_instance('data.dat')
    # opt.options["mipgap"] = 10
    # opt.options['mipfocus'] = 1
    # opt.options['presolve'] = 2
    # opt.options['numericfocus'] = 1
    opt.options['timelimit'] = 18000
    opt.options['method'] = 3
    result = opt.solve(instance, tee=False)
    log_infeasible_constraints(instance, log_expression=True)
    """
    instance.sum_similarities.display()
    instance.cohesion.display()
    instance.cohesion_temp.display()
    instance.decoupling.display()
    instance.m_op_num.display()
    instance.operational_cost.display()
    instance.decoupling.display()
    instance.l.display()
    instance.y.display()
    """

    arch = [[] for m in instance.MICROSERVICES]
    for o in instance.OPERATIONS:
        for m in instance.MICROSERVICES:
            if pyo.value(instance.x[o, m]) > 0:
                arch[int(m[1:])].append(int(o[1:]))
    for a in instance.ENTITIES:
        for m in instance.MICROSERVICES:
            if pyo.value(instance.y[a, m]) > 0:
                s = str(int(a[1:]) + 100000)
                if pyo.value(instance.l[a, m]) > 0:
                    arch[int(m[1:])].append(s + "P")
                else:
                    if pyo.value(instance.norep[a, m]) > 0:
                        arch[int(m[1:])].append(s + "N")
                    else:
                        arch[int(m[1:])].append(s + "R")
    result = []
    for a in arch:
        if a:
            result.append(a)
    print(result)
    """
    f = open("results_new.txt", 'a')
    f.write(str(alpha))
    f.write("\n")
    f.write(str(1 - alpha))
    f.write("\n")
    f.write(str(instance.decoupling.value))
    f.write("\n")
    f.write(str(instance.operational_cost.value))
    f.write("\n")
    #f.write(str(instance.operational_cost.value * alpha - t * instance.decoupling.value))
    f.write("\n")
    f.write(str(result))
    f.write("\n\n")
    f.close()
    """
    return result

