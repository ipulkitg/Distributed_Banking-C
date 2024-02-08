import grpc
import example_pb2_grpc
import example_pb2

class Customer:
    def __init__(self, id, events):
        self.id = id
        self.events = events
        self.recvMsg = list()
        self.finalAppend = list()
        self.stub = None

    def createStub(self):
        port = str(60000 + self.id)
        channel = grpc.insecure_channel("localhost:" + port)
        self.stub = example_pb2_grpc.BranchStub(channel)

    def _prepareRequestParams(self, event):
        request_params = {
            "id": event["id"],
            "branchId": event["branch"],
            "interface": event["interface"]
        }
        if event["interface"] != "query":
            request_params["money"] = event["money"]
        return request_params

    def _sendRequest(self, request_params, event):
        return self.stub.MsgDelivery(example_pb2.MsgRequest(**request_params))

    def _processResponse(self, response, event):
        if response.interface != "query":
            stringToAppend = {"interface": response.interface, "result": response.result, "branch": event["branch"]}
        else:
            stringToAppend = {"interface": response.interface, "balance": response.money, "branch": event["branch"]}
        self.recvMsg.append(stringToAppend)

    def processor_event(self):
        for event in self.events:
            request_params = self._prepareRequestParams(event)
            response = self._sendRequest(request_params, event)
            self._processResponse(response, event)

    def output(self):
        output_list = [{"id": self.id, "recv": [event]} for event in self.recvMsg]
        return output_list
