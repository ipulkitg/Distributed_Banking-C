# Distributed_Banking-C
Part 3 of Distributed banking project
Overview
This project, developed as part of the CSE 531 course, implements a distributed banking system using gRPC for communication between customers and branches. The system involves multiple customers interacting with branches, all sharing the same account. Each customer can make deposit and withdrawal requests, and branches maintain the overall account balance.

Features
gRPC Communication: The project utilizes gRPC (Google Remote Procedure Call) for communication between customers and branches in a distributed manner.

Customer Interactions: Customers can submit deposit and withdrawal requests, each identified by a unique customer-request-id.

Branch Operations: Branches handle customer requests and maintain the overall account balance.

Requirements
To run the project, make sure you have the following dependencies installed:

pip install grpcio grpcio-tools
Usage
Clone the repository:

git clone https://github.com/your-username/grpc-bandc.git
cd grpc-bandc
Run the main file:

python main.py
The main.py file can be edited to change what json file is to be read as input The output files are generated and can be checked by the checker files

Example Input
The provided example input is represented in JSON format. It includes customer and branch details, along with customer requests.
