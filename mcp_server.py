import sys, json
from client import MaximumFlowSolver

solver = MaximumFlowSolver()

def handle_jsonrpc(line):
    global solver
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-maximum-flow-edmonds-karp-network-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "compute_max_flow", "description": "Solve max flow with Edmonds-Karp.", "inputSchema": {"type": "object", "properties": {"capacity": {"type": "object"}, "source": {"type": "string"}, "sink": {"type": "string"}}, "required": ["capacity", "source", "sink"]}},
                {"name": "benchmark_max_flow", "description": "Run max flow benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "compute_max_flow":
                res = solver.edmonds_karp(args.get("capacity", {}), args.get("source"), args.get("sink"))
            elif tool == "benchmark_max_flow":
                res = solver.benchmark_max_flow()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
