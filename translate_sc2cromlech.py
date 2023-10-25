import cromlech as cr
import sys

def setup(yaml_file):
    cr.parse_arch_yaml(yaml_file)
    to_remove = cr.noise_removal()
    cr.graph_copy = cr.Graph()
    cr.op_num = len(cr.graph)
    cr.trim_operations(to_remove)
    cr.op_num = len(cr.graph)
    cr.attributes = cr.build_attr_relationships()
    cr.build_hcw_relationships()
    cr.clean_names()
    services = cr.force_operations()
    bound_ops = {}
    for s in services:
        for o1 in s:
            for o2 in cr.graph:
                if o2 in s:
                    #######
                    bound_ops.update({(o1, o2): 1})
                else:
                    bound_ops.update({(o1, o2): 0})

    for l in services:
        attrs = []
        for s in l:
            attrs += cr.op_writes.get(s) + cr.op_reads.get(s)
        attrs = list(set(attrs))
        for a in attrs:
            services[services.index(l)].append(cr.attributes_ntoi.get(a))
    cr.identify_static_attributes()
    cr.identify_hc_readonly_attributes()
    cr.elect_primary_replicas(services)


def produce_opcode_services(services):
    with_op_codes = []
    for s in services:
        serv = []
        for o in s:
            found = False
            for n in cr.nodes_dict:
                if cr.nodes_dict.get(n).get_name() == o:
                    serv.append(n)
                    found = True
            if not found:
                print("Not found " + o)
                raise Exception('Operation with name ' + o + ' was not found in nodes dictionary.')
        with_op_codes.append(serv)
    print("OP CODES ONLY: " + str(with_op_codes))
    return with_op_codes


def validate(services):
    for o in range(0, len(cr.graph)):
        count = 0
        for s in services:
            count += s.count(o)
        if count == 0:
            raise Exception("Operation " + str(o) + " was not found " + "(" + cr.nodes_dict.get(o).get_name() + ")")
        if count > 1:
            raise Exception("Operation " + str(o) + " is a duplicate " + "(" + cr.nodes_dict.get(o).get_name() + ")")

def produce_ops_and_attrs_services(services):
    ops_attrs = []
    for s in services:
        accesses = []
        for n in s:
            accesses_temp = []
            accesses_temp += cr.op_reads.get(n) + cr.op_writes.get(n)
            for a in accesses_temp:
                accesses.append(cr.attributes_ntoi.get(a))
        ops_attrs.append(s + list(set(accesses)))
    print("OPS AND ATTRS: " + str(ops_attrs))
    cr.elect_primary_replicas(ops_attrs)
    return ops_attrs


def annotate_replicas(services, only_ops):
    cached_a = {}
    uncached_a = {}
    tot_rop = 0
    for a in cr.attributes:
        c_a = []
        u_a = []
        for s in services:
            if a in s and cr.primary_replicas_locations.get(a) != services.index(s):
                read_in_same = 0
                write_in_others = 0
                for o in s:
                    if o < 10000 and cr.attributes_iton.get(a) in cr.op_reads.get(o):
                        read_in_same += cr.nodes_dict.get(o).get_frequency()
                for s2 in services:
                    for o in s2:
                        if o < 10000 and cr.attributes_iton.get(a) in cr.op_writes.get(o):
                            write_in_others += cr.nodes_dict.get(o).get_frequency()
                if read_in_same <= write_in_others:
                    tot_rop += read_in_same
                    u_a.append(services.index(s))
                else:
                    tot_rop += write_in_others
                    c_a.append(services.index(s))
        cached_a.update({a: c_a})
        uncached_a.update({a: u_a})
    final = []
    for s in only_ops:
        new_serv = [] + s
        for a in cr.attributes:
            if only_ops.index(s) in cached_a.get(a):
                new_serv.append(str(a) + 'R')
            if only_ops.index(s) in uncached_a.get(a):
                new_serv.append(str(a) + 'N')
            if only_ops.index(s) == cr.primary_replicas_locations.get(a):
                new_serv.append(str(a) + 'P')
        final.append(new_serv)
    print("FINAL FORMAT: " + str(final))
    return final

def translate(ch_architecture, sc_services):
    setup(ch_architecture)
    op_codes = produce_opcode_services(sc_services)
    validate(op_codes)
    ops_and_attrs = produce_ops_and_attrs_services(op_codes)
    complete_format = annotate_replicas(ops_and_attrs, op_codes)
    return complete_format


if __name__ == '__main__':
    yaml_file = sys.argv[1]
    

    sc = [
        ["createNewPriceConfig", "findPriceConfigById", "findByRouteIdAndTrainType", "findAllPriceConfig",
         "deletePriceConfig", "updatePriceConfig"],
        ["cancelOrderbyUser", "ticketExecute", "ticketCollect", "getSoldTickets", "createOrder", "cancelOrder",
         "deleteOrder", "updateOrder", "modifyOrderStatus", "getOrderPrice", "payOrder", "initOrder",
         "checkOrderValidity", "preserve", "rebook", "distributeSeat", "getLeftTicketOfInterval", "checkSecurityConfig",
         "getTickets"],
        ["queryForTravel", "getCheapestTravelResult", "getQuickestTravelResult", "getMinStopTravelResult", "createTrip",
         "getRouteByTripId", "getTrainTypeByTripId", "retrieveTrip", "updateTrip", "deleteTrip"],
        ["getAllAssuranceTypes", "getAllAssurances", "findAssuranceById", "findAssuranceByOrderId", "createAssurance",
         "deleteAssuranceById", "deleteAssuranceByOrderId", "modifyAssurance"],
        ["saveUser", "getAllUser", "findByUserId", "findByUsername", "updateUser"],
        ["deleteUserById"],
        ["createConfig", "updateConfig", "queryConfig", "deleteConfig", "queryAllConfigs"],
        ["findAllSecurityConfig", "addNewSecurityConfig", "deleteSecurityConfig"],
        ["modifySecurityConfig"],
        ["getPriceByWeightAndRegion", "queryConsignPrice", "createAndModifyPrice", "getConsignPrice",
         "insertConsignRecord", "updateConsignRecord", "queryConsignByAccountId", "queryConsignByOrderId",
         "queryConsignByConsignee"],
        ["addVoucher", "queryVoucher"],
        ["createFoodOrdersInBatch", "createFoodOrder", "deleteFoodOrder", "findFoodOrderByOrderId", "findAllFoodOrders",
         "updateFoodOrder"],
        ["getAllOffices", "getSpecificOffice", "addOffice", "deleteOffice", "updateOffice"],
        ["queryForStationId", "createStation", "existStation", "updateStation", "deleteStation", "queryStations",
         "queryStationById"],
        ["calculateRefund", "pay", "createPaymentAccount", "addMoney", "queryPaymentAccount", "queryPayments",
         "drawBack", "payDifference", "queryMoney", "payDifferenceRebook"],
        ["initPayment"],
        ["findContactsById", "findContactsByAccountId", "createContact", "deleteContact", "modifyContact",
         "getAllContacts"],
        ["createTrainFood", "listTrainFood", "listTrainFoodByTripIds"],
        ["createFoodStore", "listFoodStores", "listFoodStoredByStationId", "getAllFoods"],
        ["searchCheapestRouteResult", "searchMinStopRouteResult", "searchQuickestRouteResult", "createAndModifyRoute",
         "getRouteById", "getRouteByStartAndTerminal", "createTrain", "retrieveTrain", "queryTrains", "updateTrain",
         "deleteTrain", "getAllRoutes"],
        ["processDelivery"]
    ]

    output = translate(yaml_file, sc)
    print("FINAL FORMAT: " + str(output))

