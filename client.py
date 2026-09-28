from collections import deque
from typing import Dict, Any

class MaximumFlowSolver:
    @classmethod
    def edmonds_karp(cls, capacity: Dict[str, Dict[str, float]], source: str, sink: str) -> Dict[str, Any]:
        flow = {u: {v: 0.0 for v in capacity.get(u, {})} for u in capacity}
        max_flow = 0.0
        while True:
            parent = {}
            queue = deque([source])
            while queue and sink not in parent:
                u = queue.popleft()
                for v in capacity.get(u, {}):
                    residual = capacity[u][v] - flow[u].get(v, 0.0)
                    if residual > 1e-9 and v not in parent and v != source:
                        parent[v] = u
                        queue.append(v)
            if sink not in parent:
                break
            path_flow = float('inf')
            curr = sink
            while curr != source:
                p = parent[curr]
                path_flow = min(path_flow, capacity[p][curr] - flow[p].get(curr, 0.0))
                curr = p
            curr = sink
            while curr != source:
                p = parent[curr]
                flow[p][curr] = flow[p].get(curr, 0.0) + path_flow
                curr = p
            max_flow += path_flow
        return {"source": source, "sink": sink, "maximum_flow": round(max_flow, 2)}

    def benchmark_max_flow(self) -> Dict[str, Any]:
        cap = {
            "s": {"a": 10.0, "b": 5.0},
            "a": {"b": 15.0, "t": 10.0},
            "b": {"t": 10.0},
            "t": {}
        }
        return self.edmonds_karp(cap, "s", "t")
