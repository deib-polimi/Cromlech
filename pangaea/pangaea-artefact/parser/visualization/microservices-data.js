let result = {
  "communication_weight": "1",
  "coupling_weight": "10",
  "microservices": [
    {
      "id": "m1",
      "label": "M1",
      "entities": [
        {
          "id": "e1",
          "label": "Assurance"
        },
        {
          "id": "e2",
          "label": "AssuranceType"
        }
      ],
      "operations": [
        {
          "id": "op12",
          "label": "createAssurance"
        },
        {
          "id": "op25",
          "label": "deleteAssuranceById"
        },
        {
          "id": "op26",
          "label": "deleteAssuranceByOrderId"
        },
        {
          "id": "op45",
          "label": "findAssuranceById"
        },
        {
          "id": "op46",
          "label": "findAssuranceByOrderId"
        },
        {
          "id": "op54",
          "label": "getAllAssuranceTypes"
        },
        {
          "id": "op55",
          "label": "getAllAssurances"
        },
        {
          "id": "op82",
          "label": "modifyAssurance"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m2",
      "label": "M2",
      "entities": [
        {
          "id": "e23",
          "label": "Trip"
        }
      ],
      "operations": [
        {
          "id": "op24",
          "label": "createTrip"
        },
        {
          "id": "op37",
          "label": "deleteTrip"
        },
        {
          "id": "op61",
          "label": "getCheapestTravelResult"
        },
        {
          "id": "op64",
          "label": "getMinStopTravelResult"
        },
        {
          "id": "op99",
          "label": "queryForTravel"
        },
        {
          "id": "op109",
          "label": "retrieveTrip"
        },
        {
          "id": "op124",
          "label": "updateTrip"
        }
      ],
      "dependencies": [
        {
          "id": "m14",
          "weight": 1
        },
        {
          "id": "m22",
          "weight": 1
        },
        {
          "id": "m13",
          "weight": 2
        },
        {
          "id": "m23",
          "weight": 1
        },
        {
          "id": "m14",
          "weight": 1
        },
        {
          "id": "m13",
          "weight": 2
        },
        {
          "id": "m23",
          "weight": 1
        },
        {
          "id": "m22",
          "weight": 1
        },
        {
          "id": "m13",
          "weight": 1
        },
        {
          "id": "m26",
          "weight": 1
        },
        {
          "id": "m23",
          "weight": 1
        },
        {
          "id": "m4",
          "weight": 1
        }
      ],
      "communication_cost": 14
    },
    {
      "id": "m3",
      "label": "M3",
      "entities": [
        {
          "id": "e7",
          "label": "Contacts"
        }
      ],
      "operations": [
        {
          "id": "op14",
          "label": "createContact"
        },
        {
          "id": "op28",
          "label": "deleteContact"
        },
        {
          "id": "op50",
          "label": "findContactsByAccountId"
        },
        {
          "id": "op51",
          "label": "findContactsById"
        },
        {
          "id": "op56",
          "label": "getAllContacts"
        },
        {
          "id": "op83",
          "label": "modifyContact"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m4",
      "label": "M4",
      "entities": [
        {
          "id": "e21",
          "label": "Travel"
        }
      ],
      "operations": [],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m5",
      "label": "M5",
      "entities": [
        {
          "id": "e19",
          "label": "TrainFood"
        }
      ],
      "operations": [
        {
          "id": "op23",
          "label": "createTrainFood"
        },
        {
          "id": "op57",
          "label": "getAllFoods"
        },
        {
          "id": "op80",
          "label": "listTrainFood"
        },
        {
          "id": "op81",
          "label": "listTrainFoodByTripIds"
        }
      ],
      "dependencies": [
        {
          "id": "m17",
          "weight": 1
        },
        {
          "id": "m13",
          "weight": 1
        }
      ],
      "communication_cost": 2
    },
    {
      "id": "m6",
      "label": "M6",
      "entities": [],
      "operations": [],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m7",
      "label": "M7",
      "entities": [
        {
          "id": "e5",
          "label": "ConsignPrice"
        }
      ],
      "operations": [
        {
          "id": "op10",
          "label": "createAndModifyPrice"
        },
        {
          "id": "op62",
          "label": "getConsignPrice"
        },
        {
          "id": "op66",
          "label": "getPriceByWeightAndRegion"
        },
        {
          "id": "op97",
          "label": "queryConsignPrice"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m8",
      "label": "M8",
      "entities": [
        {
          "id": "e25",
          "label": "Voucher"
        }
      ],
      "operations": [
        {
          "id": "op4",
          "label": "addVoucher"
        },
        {
          "id": "op106",
          "label": "queryVoucher"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m9",
      "label": "M9",
      "entities": [
        {
          "id": "e11",
          "label": "Money"
        }
      ],
      "operations": [
        {
          "id": "op1",
          "label": "addMoney"
        },
        {
          "id": "op5",
          "label": "calculateRefund"
        },
        {
          "id": "op20",
          "label": "createPaymentAccount"
        },
        {
          "id": "op40",
          "label": "drawBack"
        },
        {
          "id": "op86",
          "label": "pay"
        },
        {
          "id": "op100",
          "label": "queryMoney"
        }
      ],
      "dependencies": [
        {
          "id": "m14",
          "weight": 1
        },
        {
          "id": "m25",
          "weight": 1
        },
        {
          "id": "m14",
          "weight": 1
        },
        {
          "id": "m18",
          "weight": 2
        }
      ],
      "communication_cost": 5
    },
    {
      "id": "m10",
      "label": "M10",
      "entities": [
        {
          "id": "e4",
          "label": "Config"
        }
      ],
      "operations": [
        {
          "id": "op13",
          "label": "createConfig"
        },
        {
          "id": "op27",
          "label": "deleteConfig"
        },
        {
          "id": "op92",
          "label": "queryAllConfigs"
        },
        {
          "id": "op93",
          "label": "queryConfig"
        },
        {
          "id": "op116",
          "label": "updateConfig"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m11",
      "label": "M11",
      "entities": [
        {
          "id": "e8",
          "label": "Delivery"
        }
      ],
      "operations": [
        {
          "id": "op91",
          "label": "processDelivery"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m12",
      "label": "M12",
      "entities": [
        {
          "id": "e17",
          "label": "SecurityConfig"
        }
      ],
      "operations": [
        {
          "id": "op2",
          "label": "addNewSecurityConfig"
        },
        {
          "id": "op9",
          "label": "checkSecurityConfig"
        },
        {
          "id": "op34",
          "label": "deleteSecurityConfig"
        },
        {
          "id": "op44",
          "label": "findAllSecurityConfig"
        },
        {
          "id": "op85",
          "label": "modifySecurityConfig"
        }
      ],
      "dependencies": [
        {
          "id": "m14",
          "weight": 1
        }
      ],
      "communication_cost": 1
    },
    {
      "id": "m13",
      "label": "M13",
      "entities": [
        {
          "id": "e16",
          "label": "Route"
        }
      ],
      "operations": [
        {
          "id": "op11",
          "label": "createAndModifyRoute"
        },
        {
          "id": "op33",
          "label": "deleteRoute"
        },
        {
          "id": "op59",
          "label": "getAllRoutes"
        },
        {
          "id": "op63",
          "label": "getLeftTicketOfInterval"
        },
        {
          "id": "op67",
          "label": "getQuickestTravelResult"
        },
        {
          "id": "op68",
          "label": "getRouteById"
        },
        {
          "id": "op69",
          "label": "getRouteByStartAndTerminal"
        },
        {
          "id": "op70",
          "label": "getRouteByTripId"
        },
        {
          "id": "op111",
          "label": "searchCheapestRouteResult"
        },
        {
          "id": "op112",
          "label": "searchMinStopRouteResult"
        },
        {
          "id": "op113",
          "label": "searchQuickestRouteResult"
        }
      ],
      "dependencies": [
        {
          "id": "m10",
          "weight": 1
        },
        {
          "id": "m14",
          "weight": 1
        },
        {
          "id": "m23",
          "weight": 1
        },
        {
          "id": "m14",
          "weight": 1
        },
        {
          "id": "m23",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 2
        },
        {
          "id": "m2",
          "weight": 1
        },
        {
          "id": "m22",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 1
        }
      ],
      "communication_cost": 12
    },
    {
      "id": "m14",
      "label": "M14",
      "entities": [
        {
          "id": "e13",
          "label": "Order"
        }
      ],
      "operations": [
        {
          "id": "op6",
          "label": "cancelOrder"
        },
        {
          "id": "op7",
          "label": "cancelOrderbyUser"
        },
        {
          "id": "op8",
          "label": "checkOrderValidity"
        },
        {
          "id": "op19",
          "label": "createOrder"
        },
        {
          "id": "op31",
          "label": "deleteOrder"
        },
        {
          "id": "op39",
          "label": "distributeSeat"
        },
        {
          "id": "op65",
          "label": "getOrderPrice"
        },
        {
          "id": "op71",
          "label": "getSoldTickets"
        },
        {
          "id": "op73",
          "label": "getTickets"
        },
        {
          "id": "op75",
          "label": "initOrder"
        },
        {
          "id": "op84",
          "label": "modifyOrderStatus"
        },
        {
          "id": "op89",
          "label": "payOrder"
        },
        {
          "id": "op90",
          "label": "preserve"
        },
        {
          "id": "op107",
          "label": "rebook"
        },
        {
          "id": "op114",
          "label": "ticketCollect"
        },
        {
          "id": "op115",
          "label": "ticketExecute"
        },
        {
          "id": "op120",
          "label": "updateOrder"
        }
      ],
      "dependencies": [
        {
          "id": "m25",
          "weight": 1
        },
        {
          "id": "m13",
          "weight": 1
        },
        {
          "id": "m23",
          "weight": 2
        },
        {
          "id": "m22",
          "weight": 1
        },
        {
          "id": "m13",
          "weight": 1
        },
        {
          "id": "m26",
          "weight": 1
        },
        {
          "id": "m23",
          "weight": 1
        },
        {
          "id": "m4",
          "weight": 1
        },
        {
          "id": "m19",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 1
        },
        {
          "id": "m3",
          "weight": 1
        },
        {
          "id": "m22",
          "weight": 1
        },
        {
          "id": "m13",
          "weight": 1
        },
        {
          "id": "m26",
          "weight": 1
        },
        {
          "id": "m23",
          "weight": 1
        },
        {
          "id": "m4",
          "weight": 1
        },
        {
          "id": "m19",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 1
        }
      ],
      "communication_cost": 20
    },
    {
      "id": "m15",
      "label": "M15",
      "entities": [
        {
          "id": "e6",
          "label": "ConsignRecord"
        }
      ],
      "operations": [
        {
          "id": "op77",
          "label": "insertConsignRecord"
        },
        {
          "id": "op94",
          "label": "queryConsignByAccountId"
        },
        {
          "id": "op95",
          "label": "queryConsignByConsignee"
        },
        {
          "id": "op96",
          "label": "queryConsignByOrderId"
        },
        {
          "id": "op117",
          "label": "updateConsignRecord"
        }
      ],
      "dependencies": [
        {
          "id": "m7",
          "weight": 1
        },
        {
          "id": "m7",
          "weight": 1
        }
      ],
      "communication_cost": 2
    },
    {
      "id": "m16",
      "label": "M16",
      "entities": [
        {
          "id": "e9",
          "label": "FoodOrder"
        }
      ],
      "operations": [
        {
          "id": "op15",
          "label": "createFoodOrder"
        },
        {
          "id": "op16",
          "label": "createFoodOrdersInBatch"
        },
        {
          "id": "op29",
          "label": "deleteFoodOrder"
        },
        {
          "id": "op42",
          "label": "findAllFoodOrders"
        },
        {
          "id": "op52",
          "label": "findFoodOrderByOrderId"
        },
        {
          "id": "op118",
          "label": "updateFoodOrder"
        }
      ],
      "dependencies": [
        {
          "id": "m11",
          "weight": 2
        },
        {
          "id": "m11",
          "weight": 2
        }
      ],
      "communication_cost": 4
    },
    {
      "id": "m17",
      "label": "M17",
      "entities": [
        {
          "id": "e10",
          "label": "FoodStore"
        }
      ],
      "operations": [
        {
          "id": "op17",
          "label": "createFoodStore"
        },
        {
          "id": "op78",
          "label": "listFoodStoredByStationId"
        },
        {
          "id": "op79",
          "label": "listFoodStores"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m18",
      "label": "M18",
      "entities": [
        {
          "id": "e14",
          "label": "Payment"
        }
      ],
      "operations": [
        {
          "id": "op76",
          "label": "initPayment"
        },
        {
          "id": "op87",
          "label": "payDifference"
        },
        {
          "id": "op88",
          "label": "payDifferenceRebook"
        },
        {
          "id": "op102",
          "label": "queryPayments"
        }
      ],
      "dependencies": [
        {
          "id": "m9",
          "weight": 1
        },
        {
          "id": "m9",
          "weight": 1
        },
        {
          "id": "m2",
          "weight": 1
        }
      ],
      "communication_cost": 3
    },
    {
      "id": "m19",
      "label": "M19",
      "entities": [
        {
          "id": "e22",
          "label": "TravelResult"
        }
      ],
      "operations": [],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m20",
      "label": "M20",
      "entities": [
        {
          "id": "e12",
          "label": "Office"
        }
      ],
      "operations": [
        {
          "id": "op3",
          "label": "addOffice"
        },
        {
          "id": "op30",
          "label": "deleteOffice"
        },
        {
          "id": "op58",
          "label": "getAllOffices"
        },
        {
          "id": "op72",
          "label": "getSpecificOffice"
        },
        {
          "id": "op119",
          "label": "updateOffice"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m21",
      "label": "M21",
      "entities": [],
      "operations": [],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m22",
      "label": "M22",
      "entities": [
        {
          "id": "e15",
          "label": "PriceConfig"
        }
      ],
      "operations": [
        {
          "id": "op18",
          "label": "createNewPriceConfig"
        },
        {
          "id": "op32",
          "label": "deletePriceConfig"
        },
        {
          "id": "op43",
          "label": "findAllPriceConfig"
        },
        {
          "id": "op47",
          "label": "findByRouteIdAndTrainType"
        },
        {
          "id": "op53",
          "label": "findPriceConfigById"
        },
        {
          "id": "op121",
          "label": "updatePriceConfig"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m23",
      "label": "M23",
      "entities": [
        {
          "id": "e20",
          "label": "TrainType"
        }
      ],
      "operations": [
        {
          "id": "op22",
          "label": "createTrain"
        },
        {
          "id": "op36",
          "label": "deleteTrain"
        },
        {
          "id": "op74",
          "label": "getTrainTypeByTripId"
        },
        {
          "id": "op105",
          "label": "queryTrains"
        },
        {
          "id": "op108",
          "label": "retrieveTrain"
        },
        {
          "id": "op123",
          "label": "updateTrain"
        }
      ],
      "dependencies": [
        {
          "id": "m2",
          "weight": 1
        }
      ],
      "communication_cost": 1
    },
    {
      "id": "m24",
      "label": "M24",
      "entities": [
        {
          "id": "e3",
          "label": "Balance"
        }
      ],
      "operations": [
        {
          "id": "op101",
          "label": "queryPaymentAccount"
        }
      ],
      "dependencies": [
        {
          "id": "m9",
          "weight": 1
        },
        {
          "id": "m18",
          "weight": 1
        },
        {
          "id": "m25",
          "weight": 1
        }
      ],
      "communication_cost": 3
    },
    {
      "id": "m25",
      "label": "M25",
      "entities": [
        {
          "id": "e24",
          "label": "User"
        }
      ],
      "operations": [
        {
          "id": "op38",
          "label": "deleteUserById"
        },
        {
          "id": "op48",
          "label": "findByUserId"
        },
        {
          "id": "op49",
          "label": "findByUsername"
        },
        {
          "id": "op60",
          "label": "getAllUser"
        },
        {
          "id": "op110",
          "label": "saveUser"
        },
        {
          "id": "op125",
          "label": "updateUser"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m26",
      "label": "M26",
      "entities": [
        {
          "id": "e18",
          "label": "Station"
        }
      ],
      "operations": [
        {
          "id": "op21",
          "label": "createStation"
        },
        {
          "id": "op35",
          "label": "deleteStation"
        },
        {
          "id": "op41",
          "label": "existStation"
        },
        {
          "id": "op98",
          "label": "queryForStationId"
        },
        {
          "id": "op103",
          "label": "queryStationById"
        },
        {
          "id": "op104",
          "label": "queryStations"
        },
        {
          "id": "op122",
          "label": "updateStation"
        }
      ],
      "dependencies": [],
      "communication_cost": 0
    },
    {
      "id": "m27",
      "label": "M27",
      "entities": [],
      "operations": [],
      "dependencies": [],
      "communication_cost": 0
    }
  ]
}

let entities_coupling = {
  "E1": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 0
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E2": [
    {
      "entity_name": "E1",
      "coupling": 0
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E3": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E4": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E5": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E6": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E7": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 1
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E8": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 1
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E9": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 1
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E10": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E11": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E12": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 0
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E13": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 1
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 1
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 1
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 1
    }
  ],
  "E14": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 1
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E15": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E16": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 1
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 1
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E17": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E18": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 0
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E19": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 1
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E20": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 1
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E21": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 1
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 1
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 1
    }
  ],
  "E22": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E23": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 1
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 1
    },
    {
      "entity_name": "E21",
      "coupling": 1
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E24": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 1
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 2
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 2
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ],
  "E25": [
    {
      "entity_name": "E1",
      "coupling": 2
    },
    {
      "entity_name": "E2",
      "coupling": 2
    },
    {
      "entity_name": "E3",
      "coupling": 2
    },
    {
      "entity_name": "E4",
      "coupling": 2
    },
    {
      "entity_name": "E5",
      "coupling": 2
    },
    {
      "entity_name": "E6",
      "coupling": 2
    },
    {
      "entity_name": "E7",
      "coupling": 2
    },
    {
      "entity_name": "E8",
      "coupling": 2
    },
    {
      "entity_name": "E9",
      "coupling": 2
    },
    {
      "entity_name": "E10",
      "coupling": 2
    },
    {
      "entity_name": "E11",
      "coupling": 2
    },
    {
      "entity_name": "E12",
      "coupling": 2
    },
    {
      "entity_name": "E13",
      "coupling": 1
    },
    {
      "entity_name": "E14",
      "coupling": 2
    },
    {
      "entity_name": "E15",
      "coupling": 2
    },
    {
      "entity_name": "E16",
      "coupling": 2
    },
    {
      "entity_name": "E17",
      "coupling": 2
    },
    {
      "entity_name": "E18",
      "coupling": 2
    },
    {
      "entity_name": "E19",
      "coupling": 2
    },
    {
      "entity_name": "E20",
      "coupling": 2
    },
    {
      "entity_name": "E21",
      "coupling": 1
    },
    {
      "entity_name": "E22",
      "coupling": 2
    },
    {
      "entity_name": "E23",
      "coupling": 2
    },
    {
      "entity_name": "E24",
      "coupling": 2
    },
    {
      "entity_name": "E25",
      "coupling": 2
    }
  ]
}

let entity_replication_cost = {
  "E1": 1,
  "E2": 1,
  "E3": 1,
  "E4": 1,
  "E5": 1,
  "E6": 1,
  "E7": 1,
  "E8": 1,
  "E9": 1,
  "E10": 1,
  "E11": 1,
  "E12": 1,
  "E13": 1,
  "E14": 1,
  "E15": 1,
  "E16": 1,
  "E17": 1,
  "E18": 1,
  "E19": 1,
  "E20": 1,
  "E21": 1,
  "E22": 1,
  "E23": 1,
  "E24": 1,
  "E25": 1
}

let total_coupling_cost = 0;
let total_communication_cost = 0;
let total_replication_cost = 0;
let total_cost = 0;

let elements = [];

let microservices = result.microservices;
microservices.map(m => {
    elements.push({
        data: {
            id: m.id,
            label: m.label,
            type: 'microservice'
        }
    })
    if (m.entities) {
        m.entities.map(e => {
            elements.push(
                {data: {id: e.id, label: e.label, type: 'entity'}},
                {data: {source: m.id, target: e.id, type: 'entity'}}
            )
            // replication_cost
            total_replication_cost += parseInt(entity_replication_cost[e.id.toUpperCase()]);
            total_cost += parseInt(entity_replication_cost[e.id.toUpperCase()]);
        })
    }
    if (m.operations) {
        m.operations.map(op => {
            elements.push(
                {data: {id: op.id, label: op.label, type: 'operation'}},
                {data: {source: m.id, target: op.id, type: 'operation'}}
            )
        })
    }
    if (m.dependencies) {
        m.dependencies.map(dep => {
            elements.push(
                {data: {source: m.id, target: dep.id, label: dep.weight, type: 'microservice', arrow: 'triangle'}},
            )
        })
        // communication cost
        total_communication_cost += m.dependencies.map(d => d.weight).reduce((a, b) => a + b, 0)
        total_cost += m.dependencies.map(d => d.weight).reduce((a, b) => a + b, 0)
    }
    let coupled_entities = 0;
    let coupling_cost = 0;
    // cycle over entities in that microservice
    m.entities.map(e1 => {
        let coupling = entities_coupling[e1.id.toUpperCase()].filter(a => a.coupling > 0).map(a => a.entity_name.toLowerCase());
        m.entities.map(e2 => {
            if (e2.id !== e1.id && coupling.indexOf(e2.id) !== -1) {
                let c = entities_coupling[e1.id.toUpperCase()][parseInt(e2.id.substring(1))-1].coupling;
                coupled_entities += c
            }
        })
    })
    coupling_cost = coupled_entities * result.coupling_weight;
    total_coupling_cost += coupling_cost;
    total_cost += coupling_cost;
})
let coupling_factor = total_coupling_cost / result.coupling_weight;
console.log('COUPLING:', total_coupling_cost)
console.log('COMMUNICATION:', total_communication_cost)
console.log('REPLICATION:', total_replication_cost)
console.log('TOTAL', total_cost)




