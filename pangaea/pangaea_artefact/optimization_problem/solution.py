class Solution:

    def __init__(self, total_cost, communication_cost, coupling_cost, replication_cost, communication_weight, coupling_weight, num_microservices, used_microservices):
        self.total_cost = total_cost
        self.communication_cost = communication_cost
        self.coupling_cost = coupling_cost
        self.replication_cost = replication_cost
        self.communication_weight = communication_weight
        self.coupling_weight = coupling_weight
        self.num_microservices = num_microservices
        self.used_microservices = used_microservices
