
# 🔁 Distributed Banking System with Client-Centric Consistency (Read-Your-Writes)

## 🧩 Problem Statement

The current distributed banking system lacks support for client-centric consistency guarantees. Specifically, there is no mechanism ensuring that a customer's write (e.g., deposit or withdrawal) at one branch is visible during subsequent reads (queries) at a different branch. This project addresses the challenge of implementing **read-your-writes consistency**, ensuring a coherent and seamless experience across replicated branch processes.

---

## 🎯 Project Goal

Implement and enforce the **read-your-writes client-centric consistency model** in a gRPC-based distributed banking system. The aim is to allow customers to perform write operations at one branch and receive up-to-date results from read operations at any other branch they interact with thereafter.

---

## ✅ Key Objectives

- Modify the system to track read and write events per customer across multiple branches.
- Implement mechanisms to enforce **read-your-writes** consistency in the presence of replication.
- Ensure customer requests always return results reflecting their own most recent writes.

---

## ⚙️ Technologies Used

| Tool/Library       | Version  |
|--------------------|----------|
| Python             | 3.9      |
| gRPC (grpcio)      | 1.59     |
| grpcio-tools       | 1.59     |
| Protobuf           | 4.24.4   |
| Multiprocessing    | Stdlib   |
| JSON, OS, Future   | Various  |

---

## 🚀 Implementation Highlights

- **Protocol Buffers (`example.proto`)** define services and messages for consistency-aware operations.
- Customers may now interact with **multiple branches** during a session.
- The system uses **event tracking and branch coordination** to enforce consistency.
- Interfaces for `Deposit`, `Withdraw`, and `Query` now accept a `branch` identifier to ensure routing and result visibility is handled correctly.
- Branch processes synchronize states via propagation so that read requests return updated results from any branch.

---

## 🧪 Output and Results

- A single **customer process** may perform events across different branches.
- Output is logged in `output.txt`, showing accurate query responses after deposits or withdrawals.
- Verified using `checker.py` script, the implementation produced:
  - ✅ **19/19 correct** cross-branch query responses

Example Result Format:
```json
[
  {"id":1,"recv":[{"interface":"deposit","branch":1,"result":"success"}]},
  {"id":1,"recv":[{"interface":"query","branch":1,"balance":400}]},
  {"id":1,"recv":[{"interface":"query","branch":2,"balance":400}]}
]
```

---

## 📖 Notes

This project demonstrates a critical aspect of distributed system design: how to ensure **session-level consistency** for individual users even in the presence of replicated state. Read-your-writes consistency improves user experience and correctness without requiring full linearizability, making it an efficient and effective strategy in real-world distributed services.

---
