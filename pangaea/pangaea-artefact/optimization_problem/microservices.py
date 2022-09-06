import pyomo.environ as pyo
from pyomo.util.infeasible import log_infeasible_constraints
import csv
import solution


def optimizer(debug=False, writeCsv=True, communication_weight=0, coupling_weight=0, num_microservices=0, executionTime=3600, file_name='result.csv'):
    model = pyo.AbstractModel()

    # opt = pyo.SolverFactory('glpk', executable="C:\\w64\\glpsol")
    opt = pyo.SolverFactory('gurobi', solver_io="lp")
    
    ######################
    # INPUT VARIABLES #
    ######################

    # set of entities
    model.ENTITIES = pyo.Set()

    # set of operations
    model.OPERATIONS = pyo.Set()

    # num of available microservices
    if num_microservices == 0:
        model.num_microservices = pyo.Param(within=pyo.PositiveIntegers)
        # set of available microservices
        model.MICROSERVICES = pyo.Set()
    else:
        model.num_microservices = pyo.Param(within=pyo.PositiveIntegers, initialize=num_microservices)
        services_list = []
        for i in range(1, num_microservices+1):
            services_list.append("M"+str(i))
        model.MICROSERVICES = pyo.Set(initialize=services_list)

    # weight coefficient for coupling
    if coupling_weight == 0:
        model.coupling_weight = pyo.Param(within=pyo.Integers, mutable=True)
    else:
        model.coupling_weight = pyo.Param(within=pyo.Integers, initialize=coupling_weight, mutable=True)

    # weight coefficient for communication
    if communication_weight == 0:
        model.communication_weight = pyo.Param(within=pyo.Integers, mutable=True)
    else:
        model.communication_weight = pyo.Param(within=pyo.Integers, initialize=communication_weight, mutable=True)

    # weight coefficient for entities' replication
    model.replication_overhead = pyo.Param({'C'}, model.ENTITIES, within=pyo.Integers, initialize=1)

    # matrix of dependencies between operations and entities
    model.dependencies = pyo.Param(model.OPERATIONS, model.ENTITIES, within=pyo.Integers)

    # matrix of coupling constraints between entities
    model.entities_coupling = pyo.Param(model.ENTITIES, model.ENTITIES, within=pyo.Integers)

    ######################
    # DECISION VARIABLES #
    ######################

    # matrix of indicating operations positions (in contexts) -> 0 present, 1 not present
    model.pos_operations = pyo.Var(model.OPERATIONS, model.MICROSERVICES, within=pyo.Binary)

    # matrix of indicating entities positions (in contexts) -> 1 present, 0 not present
    model.pos_entities = pyo.Var(model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    # additional variables needed to linearize product of binary variables
    model.z = pyo.Var(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)
    model.w = pyo.Var(model.ENTITIES, model.ENTITIES, model.MICROSERVICES, within=pyo.Binary)

    # array of communication overhead of each microservice
    model.communication_cost = pyo.Var(model.MICROSERVICES, within=pyo.Integers)

    # array of coupling cost of each microservice
    model.coupling_cost = pyo.Var(model.MICROSERVICES, within=pyo.Integers)

    # array of cost (coupling + communication) of each microservice
    model.cost = pyo.Var(model.MICROSERVICES, within=pyo.Integers)

    # array of replication cost of each entity
    model.replication_cost = pyo.Var(model.ENTITIES, within=pyo.Integers)

    ########################
    # OPTIMIZATION PROBLEM #
    ########################

    def communication_cost_constraint(mod, i):
        comm_cost_summation = 0
        for op in mod.OPERATIONS:
            for e in mod.ENTITIES:
                comm_cost_summation += mod.dependencies[op, e] * mod.communication_weight * (
                        mod.pos_operations[op, i] - mod.z[op, e, i])
        return mod.communication_cost[i] >= comm_cost_summation

    model.CommunicationCostConst = pyo.Constraint(model.MICROSERVICES, rule=communication_cost_constraint)

    def z_check_1(mod, op, e, m):
        return mod.z[op, e, m] <= mod.pos_entities[e, m]

    def z_check_2(mod, op, e, m):
        return mod.z[op, e, m] <= mod.pos_operations[op, m]

    def z_check_3(mod, op, e, m):
        return mod.z[op, e, m] >= mod.pos_operations[op, m] + mod.pos_entities[e, m] - 1

    model.ZCheck1Const = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, rule=z_check_1)
    model.ZCheck2Const = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, rule=z_check_2)
    model.ZCheck3Const = pyo.Constraint(model.OPERATIONS, model.ENTITIES, model.MICROSERVICES, rule=z_check_3)

    def coupling_cost_constraint(mod, i):
        coup_cost_summation = 0
        for e1 in mod.ENTITIES:
            for e2 in mod.ENTITIES:
                if e1 != e2:
                    coup_cost_summation += mod.w[e1, e2, i] * mod.entities_coupling[e1, e2] * mod.coupling_weight

        return mod.coupling_cost[i] >= coup_cost_summation

    model.CouplingCostConst = pyo.Constraint(model.MICROSERVICES, rule=coupling_cost_constraint)

    def w_check_1(mod, e1, e2, m):
        return mod.w[e1, e2, m] <= mod.pos_entities[e1, m]

    def w_check_2(mod, e1, e2, m):
        return mod.w[e1, e2, m] <= mod.pos_entities[e2, m]

    def w_check_3(mod, e1, e2, m):
        return mod.w[e1, e2, m] >= mod.pos_entities[e1, m] + mod.pos_entities[e2, m] - 1

    model.WCheck1Const = pyo.Constraint(model.ENTITIES, model.ENTITIES, model.MICROSERVICES, rule=w_check_1)
    model.WCheck2Const = pyo.Constraint(model.ENTITIES, model.ENTITIES, model.MICROSERVICES, rule=w_check_2)
    model.WCheck3Const = pyo.Constraint(model.ENTITIES, model.ENTITIES, model.MICROSERVICES, rule=w_check_3)

    def cost_constraint(mod, i):
        return mod.cost[i] >= mod.communication_cost[i] + mod.coupling_cost[i]

    model.CostConst = pyo.Constraint(model.MICROSERVICES, rule=cost_constraint)

    def replication_cost_constraint(mod, i):
        replication_sum = 0
        for j in mod.MICROSERVICES:
            replication_sum += mod.pos_entities[i, j]
        return mod.replication_cost[i] >= mod.replication_overhead['C', i] * replication_sum * mod.communication_weight

    model.ReplicationCostConst = pyo.Constraint(model.ENTITIES, rule=replication_cost_constraint)

    def entities_check(mod, i):
        entity_sum = 0
        for j in mod.MICROSERVICES:
            entity_sum += mod.pos_entities[i, j]
        return entity_sum >= 1

    model.EntitiesCheckConst = pyo.Constraint(model.ENTITIES, rule=entities_check)

    def operations_check(mod, i):
        return sum(mod.pos_operations[i, j] for j in mod.MICROSERVICES) == 1

    model.OperationsCheckConst = pyo.Constraint(model.OPERATIONS, rule=operations_check)

    def total_cost(mod):
        return pyo.summation(mod.cost) + pyo.summation(mod.replication_cost)

    model.obj = pyo.Objective(rule=total_cost, sense=pyo.minimize)
    model.name = 'Microservices Decomposition'
    instance = model.create_instance('microservices.dat')
    instance.coupling_weight.value = coupling_weight
    instance.communication_weight.value = communication_weight
    
    #opt.options["mipgap"] = 0.05
    opt.options['mipfocus'] = 1
    opt.options['presolve'] = 2
    opt.options['timelimit'] = executionTime
    result = opt.solve(instance, tee=debug)
    log_infeasible_constraints(instance, log_expression=True)
    instance.OPERATIONS.display()
    #
    # Print values for each variable explicitly
    #

    if debug:
        print("###### COMMUNICATION COSTS ######")
        for i in instance.MICROSERVICES:
            print(instance.communication_cost[i], instance.communication_cost[i].value)
        print("\n###### COUPLING WEIGHT ######")
        print(instance.communication_weight, instance.communication_weight.value)
        print("\n###### COUPLING COSTS ######")
        for i in instance.MICROSERVICES:
            print(instance.coupling_cost[i], instance.coupling_cost[i].value)
        print("\n###### COUPLING WEIGHT ######")
        print(instance.coupling_weight, instance.coupling_weight.value)
        print("\n###### ENTITIES ######")
        for i in instance.pos_entities:
            print(instance.pos_entities[i], instance.pos_entities[i].value)
        print("\n###### OPERATIONS ######")
        for i in instance.pos_operations:
            print(instance.pos_operations[i], instance.pos_operations[i].value)
        print("\n###### REPLICATION COST ######")
        for i in instance.replication_cost:
            print(instance.replication_cost[i], instance.replication_cost[i].value)

    if writeCsv:
        with open(file_name, mode='w') as result_file:
            csv_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            csv_writer.writerow([])
            csv_writer.writerow(['COMMUNICATION WEIGHT', int(instance.communication_weight.value)])

            csv_writer.writerow([])
            csv_writer.writerow(['COUPLING WEIGHT', int(instance.coupling_weight.value)])

            csv_writer.writerow([])
            row = ["MICROSERVICES"]
            for m in instance.MICROSERVICES:
                row.append(m)
            csv_writer.writerow(row)

            csv_writer.writerow([])
            row = ['COMMUNICATION COST']
            communication_cost = 0
            for m in instance.MICROSERVICES:
                row.append(int(instance.communication_cost[m].value))
                communication_cost += int(instance.communication_cost[m].value)
            csv_writer.writerow(row)

            csv_writer.writerow([])
            row = ['COUPLING COST']
            coupling_cost = 0
            for m in instance.MICROSERVICES:
                row.append(int(instance.coupling_cost[m].value))
                coupling_cost += int(instance.coupling_cost[m].value)
            csv_writer.writerow(row)

            csv_writer.writerow([])
            row = ['REPLICATION COST']
            replication_cost = 0
            for m in instance.ENTITIES:
                replication_cost += int(instance.replication_cost[m].value)
            row.append(replication_cost)
            csv_writer.writerow(row)

            total_cost = replication_cost + coupling_cost + communication_cost
            csv_writer.writerow([])
            row = ['TOTAL COST', total_cost]
            csv_writer.writerow(row)

            csv_writer.writerow([])
            csv_writer.writerow(['POS ENTITIES'])
            for e in instance.ENTITIES:
                row = [e]
                for m in instance.MICROSERVICES:
                    row.append(int(instance.pos_entities[e, m].value))
                csv_writer.writerow(row)
            csv_writer.writerow([])
            csv_writer.writerow(['POS OPERATIONS'])
            for op in instance.OPERATIONS:
                row = [op]
                for m in instance.MICROSERVICES:
                    row.append(int(instance.pos_operations[op, m].value))
                csv_writer.writerow(row)
    else:
        replication_cost = 0
        coupling_cost = 0
        communication_cost = 0
        for e in instance.ENTITIES:
            replication_cost += int(instance.replication_cost[e].value)
        for m in instance.MICROSERVICES:
            communication_cost += int(instance.communication_cost[m].value)
            coupling_cost += int(instance.coupling_cost[m].value)
        total_cost = replication_cost + coupling_cost + communication_cost
        n = set()
        for e in instance.ENTITIES:
            for m in instance.MICROSERVICES:
                if instance.pos_entities[e, m] == 1:
                    n.add(m)
        used_microservices = len(n)
        return solution.Solution(
            communication_weight=instance.communication_weight.value,
            coupling_weight=instance.coupling_weight.value,
            communication_cost=communication_cost,
            coupling_cost=coupling_cost,
            replication_cost=replication_cost,
            num_microservices=instance.num_microservices.value,
            used_microservices=used_microservices,
            total_cost=total_cost
        )

# optimizer(debug=True)
