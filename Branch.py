import grpc
import example_pb2_grpc
import example_pb2

class Branch(example_pb2_grpc.BranchServicer):
    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()
        self.recvMsg = list()

    def createStubs(self):
        self.stubList = [
            example_pb2_grpc.BranchStub(grpc.insecure_channel(f"localhost:{60000 + branchId}"))
            for branchId in self.branches if branchId != self.id
        ]

    def _handleQuery(self, request):
        return example_pb2.MsgResponse(interface=request.interface, money=self.balance)

    def _handleDeposit(self, request, propagate):
        self.balance += request.money
        if propagate:
            self._propagateMessage(request, "deposit")
        return "success"

    def _handleWithdraw(self, request, propagate):
        if self.balance >= request.money:
            self.balance -= request.money
            if propagate:
                self._propagateMessage(request, "withdraw")
            return "success"
        else:
            return "fail"

    def _propagateMessage(self, request, interface):
        for stub in self.stubList:
            stub.MsgPropagation(example_pb2.MsgRequest(id=request.id, interface=interface, branchId=request.branchId, money=request.money))

    def _prepareMsg(self, request, result):
        msg = {"interface": request.interface, "result": result, "branchId": request.branchId}
        if request.interface != "query":
            msg["result"] = result
        else:
            msg["money"] = request.money
        return msg

    def constructmessageforprop(self, request, propagate):
        result = "success"
        if request.money < 0:
            result = "fail"
        elif request.interface == "query":
            return self._handleQuery(request)
        elif request.interface == "deposit":
            result = self._handleDeposit(request, propagate)
        elif request.interface == "withdraw":
            result = self._handleWithdraw(request, propagate)
        else:
            result = "fail"

        msg = self._prepareMsg(request, result)
        self.recvMsg.append(msg)
        return example_pb2.MsgResponse(interface=request.interface, result=result, money=self.balance, branchId=request.branchId)


    def MsgDelivery(self, request, context):
        return self.constructmessageforprop(request, True)

    def MsgPropagation(self, request, context):
        return self.constructmessageforprop(request, False)
