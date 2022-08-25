/**
 * @Entity
 * name: AssuranceType
 * implementation: AssuranceType
 * replication_overhead: 1
 * columns:
 *   - index
 *   - price
 *   - name
 */

/**
 * @Entity
 * name: Assurance
 * implementation: Assurance
 * replication_overhead: 1
 * columns:
 *   - index
 *   - orderId
 *   - price
 *   - name
 *   - id
 * relations:
 *   - entity_name: AssuranceType
 *     type: COMPOSITION
 */

/**
 * @Entity
 * name: User
 * implementation: User
 * replication_overhead: 1
 * columns:
 *   - userName
 *   - userId
 *   - email
 *   - roles
 *   - password
 *   - id
 */

/**
 * @Entity
 * name: Station
 * implementation: Station
 * replication_overhead: 1
 * columns:
 *   - stayTime
 *   - id
 *   - name
 * relations:
 *   - entity_name: Office
 *     type: COMPOSITION
 */

/**
 * @Entity
 * name: TrainType
 * implementation: TrainType
 * replication_overhead: 1
 * columns:
 *   - economyClass
 *   - confortClass
 *   - id
 *   - averageSpeed
 */

/**
 * @Entity
 * name: Route
 * implementation: Route
 * replication_overhead: 1
 * columns:
 *   - startingStationId
 *   - startStationId
 *   - id
 *   - routeId
 *   - stations
 *   - distances
 *   - terminalStationId
 */

/**
 * @Entity
 * name: PriceConfig
 * implementation: PriceConfig
 * replication_overhead: 1
 * columns:
 *   - trainType
 *   - firstClassPriceRate
 *   - routeId
 *   - basicPriceRate
 *   - id
 */

/**
 * @Entity
 * name: Trip
 * implementation: Trip
 * replication_overhead: 1
 * columns:
 *   - startingStationId
 *   - startingTime
 *   - tripId
 *   - endTime
 *   - trainTypeId
 *   - stationsId
 *   - routeId
 *   - terminalStationId
 * relations:
 *   - entity_name: Travel
 *     type: AGGREGATION
 *   - entity_name: Route
 *     type: AGGREGATION
 *   - entity_name: TrainType
 *     type: AGGREGATION
 */

/**
 * @Entity
 * name: Travel
 * implementation: Travel
 * replication_overhead: 1
 * columns:
 *   - endPlace
 *   - tripId
 *   - departureTime
 *   - startingPlace
 */

/**
 * @Entity
 * name: Order
 * implementation: Order
 * replication_overhead: 1
 * columns:
 *   - seatClass
 *   - seatNumber
 *   - orderId
 *   - from
 *   - travelDate
 *   - travelTime
 *   - trainNumber
 *   - accountId
 *   - price
 *   - contactsDocumentNumber
 *   - to
 *   - status
 *   - boughtDate
 *   - documentType
 *   - id
 *   - coachNumber
 *   - contactsName
 * relations:
 *   - entity_name: Travel
 *     type: AGGREGATION
 *   - entity_name: Route
 *     type: AGGREGATION
 *   - entity_name: Payment
 *     type: AGGREGATION
 */

/**
 * @Entity
 * name: Money
 * implementation: Money
 * replication_overhead: 1
 * columns:
 *   - userId
 *   - type
 *   - id
 *   - money
 */

/**
 * @Entity
 * name: Config
 * implementation: Config
 * replication_overhead: 1
 * columns:
 *   - value
 *   - description
 *   - name
 */

/**
 * @Entity
 * name: ConsignPrice
 * implementation: ConsignPrice
 * replication_overhead: 1
 * columns:
 *   - initialPrice
 *   - index
 *   - beyondPrice
 *   - id
 *   - initialWeight
 *   - withinPrice
 */

/**
 * @Entity
 * name: ConsignRecord
 * implementation: ConsignRecord
 * replication_overhead: 1
 * columns:
 *   - orderId
 *   - from
 *   - weight
 *   - consignee
 *   - handleDate
 *   - targetDate
 *   - accountId
 *   - price
 *   - to
 *   - phone
 *   - id
 */

/**
 * @Entity
 * name: Contacts
 * implementation: Contacts
 * replication_overhead: 1
 * columns:
 *   - phoneNumber
 *   - accountId
 *   - name
 *   - documentType
 *   - id
 *   - documentName
 * relations:
 *   - entity_name: User
 *     type: AGGREGATION
 */

/**
 * @Entity
 * name: Delivery
 * implementation: Delivery
 * replication_overhead: 1
 * columns:
 *   - stationName
 *   - orderId
 *   - storeName
 *   - id
 *   - foodName
 * relations:
 *   - entity_name: FoodOrder
 *     type: AGGREGATION
 */

/**
 * @Entity
 * name: FoodStore
 * implementation: FoodStore
 * replication_overhead: 1
 * columns:
 *   - deliveryFee
 *   - telephone
 *   - storeName
 *   - businessTime
 *   - stationId
 *   - id
 *   - foodList
 */

/**
 * @Entity
 * name: TrainFood
 * implementation: TrainFood
 * replication_overhead: 1
 * columns:
 *   - id
 *   - foodList
 *   - tripId
 */

/**
 * @Entity
 * name: FoodOrder
 * implementation: FoodOrder
 * replication_overhead: 1
 * columns:
 *   - stationName
 *   - orderId
 *   - storeName
 *   - foodType
 *   - id
 *   - foodName
 * relations:
 *   - entity_name: TrainFood
 *     type: AGGREGATION
 */

/**
 * @Entity
 * name: Payment
 * implementation: Payment
 * replication_overhead: 1
 * columns:
 *   - userId
 *   - orderId
 *   - price
 *   - id
 */

/**
 * @Entity
 * name: Balance
 * implementation: Balance
 * replication_overhead: 1
 * columns:
 *   - balance
 *   - userId
 *   - id
 */

/**
 * @Entity
 * name: TravelResult
 * implementation: TravelResult
 * replication_overhead: 1
 * columns:
 *   - percent
 *   - trainType
 *   - status
 */

/**
 * @Entity
 * name: SecurityConfig
 * implementation: SecurityConfig
 * replication_overhead: 1
 * columns:
 *   - value
 *   - description
 *   - name
 *   - id
 * relations:
 *   - entity_name: Config
 *     type: INHERITANCE
 */

/**
 * @Entity
 * name: Office
 * implementation: Office
 * replication_overhead: 1
 * columns:
 *   - officeName
 *   - workTime
 *   - windowNum
 *   - region
 *   - province
 *   - address
 *   - city
 */

/**
 * @Entity
 * name: Voucher
 * implementation: Voucher
 * replication_overhead: 1
 * columns:
 *   - seatClass
 *   - seatNumber
 *   - destStation
 *   - orderId
 *   - travelDate
 *   - startStation
 *   - travelTime
 *   - trainNumber
 *   - contactName
 *   - voucherId
 *   - price
 * relations:
 *   - entity_name: Order
 *     type: AGGREGATION
 *   - entity_name: Travel
 *     type: AGGREGATION
 */

/**
 * @Operation
 * name: getAllAssuranceTypes
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: AssuranceType
 *     access_mode: read
 */

/**
 * @Operation
 * name: getAllAssurances
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: AssuranceType
 *     access_mode: read
 *   - entity_name: Assurance
 *     access_mode: read
 */

/**
 * @Operation
 * name: findAssuranceById
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Assurance
 *     access_mode: read
 */

/**
 * @Operation
 * name: findAssuranceByOrderId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Assurance
 *     access_mode: read
 */

/**
 * @Operation
 * name: createAssurance
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Assurance
 *     access_mode: write
 *   - entity_name: AssuranceType
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteAssuranceById
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Assurance
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteAssuranceByOrderId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Assurance
 *     access_mode: write
 */

/**
 * @Operation
 * name: modifyAssurance
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Assurance
 *     access_mode: write
 *   - entity_name: AssuranceType
 *     access_mode: write
 */

/**
 * @Operation
 * name: saveUser
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: getAllUser
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: findByUserId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: findByUsername
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: deleteUserById
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateUser
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryForTravel
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: read
 *   - entity_name: PriceConfig
 *     access_mode: read
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: Travel
 *     access_mode: read
 */

/**
 * @Operation
 * name: queryForStationId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: read
 */

/**
 * @Operation
 * name: cancelOrderbyUser
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 *   - entity_name: User
 *     access_mode: read
 */

/**
 * @Operation
 * name: calculateRefund
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: read
 *   - entity_name: Money
 *     access_mode: write
 */

/**
 * @Operation
 * name: createConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Config
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Config
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Config
 *     access_mode: read
 */

/**
 * @Operation
 * name: deleteConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Config
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryAllConfigs
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Config
 *     access_mode: read
 */

/**
 * @Operation
 * name: getPriceByWeightAndRegion
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignPrice
 *     access_mode: read
 */

/**
 * @Operation
 * name: queryConsignPrice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignPrice
 *     access_mode: read
 */

/**
 * @Operation
 * name: createAndModifyPrice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignPrice
 *     access_mode: write
 */

/**
 * @Operation
 * name: getConsignPrice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignPrice
 *     access_mode: read
 */

/**
 * @Operation
 * name: insertConsignRecord
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignPrice
 *     access_mode: read
 *   - entity_name: ConsignRecord
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateConsignRecord
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignPrice
 *     access_mode: read
 *   - entity_name: ConsignRecord
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryConsignByAccountId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignRecord
 *     access_mode: read
 */

/**
 * @Operation
 * name: queryConsignByOrderId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignRecord
 *     access_mode: read
 */

/**
 * @Operation
 * name: queryConsignByConsignee
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: ConsignRecord
 *     access_mode: read
 */

/**
 * @Operation
 * name: findContactsById
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Contacts
 *     access_mode: read
 */

/**
 * @Operation
 * name: findContactsByAccountId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Contacts
 *     access_mode: read
 */

/**
 * @Operation
 * name: createContact
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Contacts
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteContact
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Contacts
 *     access_mode: write
 */

/**
 * @Operation
 * name: modifyContact
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Contacts
 *     access_mode: write
 */

/**
 * @Operation
 * name: getAllContacts
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Contacts
 *     access_mode: read
 */

/**
 * @Operation
 * name: processDelivery
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Delivery
 *     access_mode: write
 */

/**
 * @Operation
 * name: ticketExecute
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: ticketCollect
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: createFoodStore
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodStore
 *     access_mode: write
 */

/**
 * @Operation
 * name: createTrainFood
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainFood
 *     access_mode: write
 */

/**
 * @Operation
 * name: listFoodStores
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodStore
 *     access_mode: read
 */

/**
 * @Operation
 * name: listTrainFood
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainFood
 *     access_mode: read
 */

/**
 * @Operation
 * name: listFoodStoredByStationId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodStore
 *     access_mode: read
 */

/**
 * @Operation
 * name: listTrainFoodByTripIds
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainFood
 *     access_mode: read
 */

/**
 * @Operation
 * name: createFoodOrdersInBatch
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodOrder
 *     access_mode: write
 *   - entity_name: Delivery
 *     access_mode: write
 */

/**
 * @Operation
 * name: createFoodOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodOrder
 *     access_mode: write
 *   - entity_name: Delivery
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteFoodOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodOrder
 *     access_mode: write
 */

/**
 * @Operation
 * name: findFoodOrderByOrderId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodOrder
 *     access_mode: read
 */

/**
 * @Operation
 * name: findAllFoodOrders
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodOrder
 *     access_mode: read
 */

/**
 * @Operation
 * name: updateFoodOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: FoodOrder
 *     access_mode: write
 */

/**
 * @Operation
 * name: getAllFoods
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainFood
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: read
 *   - entity_name: FoodStore
 *     access_mode: read
 */

/**
 * @Operation
 * name: pay
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: read
 *   - entity_name: Payment
 *     access_mode: write
 *   - entity_name: Money
 *     access_mode: write
 */

/**
 * @Operation
 * name: createPaymentAccount
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Money
 *     access_mode: write
 */

/**
 * @Operation
 * name: addMoney
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Money
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryPaymentAccount
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: User
 *     access_mode: read
 *   - entity_name: Money
 *     access_mode: read
 *   - entity_name: Payment
 *     access_mode: read
 *   - entity_name: Balance
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryPayments
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Payment
 *     access_mode: read
 */

/**
 * @Operation
 * name: drawBack
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Money
 *     access_mode: write
 */

/**
 * @Operation
 * name: payDifference
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Payment
 *     access_mode: write
 *   - entity_name: Money
 *     access_mode: read
 */

/**
 * @Operation
 * name: queryMoney
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Money
 *     access_mode: read
 */

/**
 * @Operation
 * name: initPayment
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Payment
 *     access_mode: write
 */

/**
 * @Operation
 * name: getSoldTickets
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: createOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: cancelOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: modifyOrderStatus
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: getOrderPrice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: read
 */

/**
 * @Operation
 * name: payOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: initOrder
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: checkOrderValidity
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: read
 */

/**
 * @Operation
 * name: preserve
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: read
 *   - entity_name: Order
 *     access_mode: write
 *   - entity_name: Contacts
 *     access_mode: read
 *   - entity_name: Station
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 *   - entity_name: PriceConfig
 *     access_mode: read
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: Travel
 *     access_mode: read
 *   - entity_name: TravelResult
 *     access_mode: read
 */

/**
 * @Operation
 * name: createNewPriceConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: PriceConfig
 *     access_mode: write
 */

/**
 * @Operation
 * name: findPriceConfigById
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: PriceConfig
 *     access_mode: read
 */

/**
 * @Operation
 * name: findByRouteIdAndTrainType
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: PriceConfig
 *     access_mode: read
 */

/**
 * @Operation
 * name: findAllPriceConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: PriceConfig
 *     access_mode: read
 */

/**
 * @Operation
 * name: deletePriceConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: PriceConfig
 *     access_mode: write
 */

/**
 * @Operation
 * name: updatePriceConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: PriceConfig
 *     access_mode: write
 */

/**
 * @Operation
 * name: rebook
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: write
 *   - entity_name: Trip
 *     access_mode: read
 */

/**
 * @Operation
 * name: payDifferenceRebook
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: Payment
 *     access_mode: write
 *   - entity_name: Money
 *     access_mode: read
 */

/**
 * @Operation
 * name: searchCheapestRouteResult
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: PriceConfig
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: write
 */

/**
 * @Operation
 * name: searchMinStopRouteResult
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: write
 */

/**
 * @Operation
 * name: searchQuickestRouteResult
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: write
 */

/**
 * @Operation
 * name: createAndModifyRoute
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteRoute
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: write
 */

/**
 * @Operation
 * name: getAllRoutes
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: read
 */

/**
 * @Operation
 * name: getRouteById
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: read
 */

/**
 * @Operation
 * name: getRouteByStartAndTerminal
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: read
 */

/**
 * @Operation
 * name: distributeSeat
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: read
 *   - entity_name: Order
 *     access_mode: write
 *   - entity_name: TrainType
 *     access_mode: write
 */

/**
 * @Operation
 * name: getLeftTicketOfInterval
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Route
 *     access_mode: read
 *   - entity_name: Order
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 *   - entity_name: Config
 *     access_mode: read
 */

/**
 * @Operation
 * name: findAllSecurityConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: SecurityConfig
 *     access_mode: read
 */

/**
 * @Operation
 * name: addNewSecurityConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: SecurityConfig
 *     access_mode: write
 */

/**
 * @Operation
 * name: modifySecurityConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: SecurityConfig
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteSecurityConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: SecurityConfig
 *     access_mode: write
 */

/**
 * @Operation
 * name: checkSecurityConfig
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Order
 *     access_mode: read
 *   - entity_name: SecurityConfig
 *     access_mode: read
 */

/**
 * @Operation
 * name: createStation
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: write
 */

/**
 * @Operation
 * name: existStation
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: read
 */

/**
 * @Operation
 * name: updateStation
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteStation
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryStations
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: read
 */

/**
 * @Operation
 * name: queryStationById
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: read
 */

/**
 * @Operation
 * name: getAllOffices
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Office
 *     access_mode: read
 */

/**
 * @Operation
 * name: getSpecificOffice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Office
 *     access_mode: read
 */

/**
 * @Operation
 * name: addOffice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Office
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteOffice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Office
 *     access_mode: write
 */

/**
 * @Operation
 * name: updateOffice
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Office
 *     access_mode: write
 */

/**
 * @Operation
 * name: createTrain
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainType
 *     access_mode: write
 */

/**
 * @Operation
 * name: retrieveTrain
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainType
 *     access_mode: read
 */

/**
 * @Operation
 * name: queryTrains
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainType
 *     access_mode: read
 */

/**
 * @Operation
 * name: updateTrain
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainType
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteTrain
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: TrainType
 *     access_mode: write
 */

/**
 * @Operation
 * name: getCheapestTravelResult
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: write
 *   - entity_name: PriceConfig
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: write
 *   - entity_name: Order
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 */

/**
 * @Operation
 * name: getQuickestTravelResult
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: write
 *   - entity_name: Route
 *     access_mode: write
 *   - entity_name: Order
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 */

/**
 * @Operation
 * name: getMinStopTravelResult
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: write
 *   - entity_name: Route
 *     access_mode: write
 *   - entity_name: Order
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 */

/**
 * @Operation
 * name: createTrip
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: write
 */

/**
 * @Operation
 * name: getRouteByTripId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: read
 */

/**
 * @Operation
 * name: getTrainTypeByTripId
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 */

/**
 * @Operation
 * name: retrieveTrip
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: read
 */

/**
 * @Operation
 * name: updateTrip
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: write
 */

/**
 * @Operation
 * name: deleteTrip
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Trip
 *     access_mode: write
 */

/**
 * @Operation
 * name: getTickets
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Station
 *     access_mode: read
 *   - entity_name: TrainType
 *     access_mode: read
 *   - entity_name: Route
 *     access_mode: read
 *   - entity_name: PriceConfig
 *     access_mode: read
 *   - entity_name: Trip
 *     access_mode: read
 *   - entity_name: Travel
 *     access_mode: read
 *   - entity_name: TravelResult
 *     access_mode: read
 *   - entity_name: Order
 *     access_mode: write
 */

/**
 * @Operation
 * name: addVoucher
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Voucher
 *     access_mode: write
 */

/**
 * @Operation
 * name: queryVoucher
 * integrity: low
 * frequency: 1
 * forced_entities:
 *   -
 * entities:
 *   - entity_name: Voucher
 *     access_mode: read
 */

