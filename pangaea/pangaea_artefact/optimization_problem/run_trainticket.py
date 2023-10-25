import microservices
import sys

solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=0, coupling_weight=100, num_microservices=27, executionTime=7200, file_name='trainticket_0_100.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=10, coupling_weight=90, num_microservices=27, executionTime=7200, file_name='trainticket_10_90.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=20, coupling_weight=80, num_microservices=27, executionTime=7200, file_name='trainticket_20_80.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=30, coupling_weight=70, num_microservices=27, executionTime=7200, file_name='trainticket_30_70.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=40, coupling_weight=60, num_microservices=27, executionTime=7200, file_name='trainticket_40_60.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=50, coupling_weight=50, num_microservices=27, executionTime=7200, file_name='trainticket_50_50.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=60, coupling_weight=40, num_microservices=27, executionTime=7200, file_name='trainticket_60_40.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=70, coupling_weight=30, num_microservices=27, executionTime=7200, file_name='trainticket_70_30.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=80, coupling_weight=20, num_microservices=27, executionTime=7200, file_name='trainticket_80_20.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=90, coupling_weight=10, num_microservices=27, executionTime=7200, file_name='trainticket_90_10.csv')
solution = microservices.optimizer(debug=True, writeCsv=True, communication_weight=100, coupling_weight=0, num_microservices=27, executionTime=7200, file_name='trainticket_100_0.csv')
