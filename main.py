import json
import multiprocessing
from time import sleep
from concurrent import futures
import grpc
import example_pb2_grpc
from Branch import Branch
from Customer import Customer


def startBranchServers(branch):
    branch.createStubs()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_BranchServicer_to_server(branch, server)
    server.add_insecure_port("localhost:" + str(60000 + branch.id))
    server.start()
    server.wait_for_termination()
def finish_branch_processes(branchProcessList):
    [branch_process.terminate() for branch_process in branchProcessList]

def customerprocess_init(customers, customerProcessList):
    for customer in customers:
        customer_process = multiprocessing.Process(target=customerProcessing, args=(customer,))
        customerProcessList.append(customer_process)
        customer_process.start()
        sleep(1)

def customer_process_data(customerProcessList):
    [customer_process.join() for customer_process in customerProcessList]

def customerProcessing(customer):
    customer.createStub()
    customer.processor_event()
    output = customer.output()
    writeOutputToFile(output)


def process_init(processes):
    branches, branchIds, branchProcessList  = [], [], []

    for process in processes:
        if process["type"] == "branch":
            branch = Branch(process["id"], process["balance"], branchIds)
            branches.append(branch)
            branchIds.append(branch.id)

    for branch in branches:
        branch_process = multiprocessing.Process(target=startBranchServers, args=(branch,))
        branchProcessList.append(branch_process)
        branch_process.start()

    # Allow branch processes to start
    sleep(0.25)
    customers = []
    customerProcessList = []

    for process in processes:
        if process["type"] == "customer":
            customer = Customer(process["id"], process["events"])
            customers.append(customer)


    customerprocess_init(customers,customerProcessList)
    customer_process_data(customerProcessList)
    finish_branch_processes(branchProcessList)
def writeOutputToFile(output):
    with open("output.json", "a") as output_file:
        output_file.write(json.dumps(output, indent=2) + "\n")
def read_input_file(input_file_path):

    with open(input_file_path, 'r') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    input_data = read_input_file('input.json')
    open("output.json", "w").close()
    process_init(input_data)
