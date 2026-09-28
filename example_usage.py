from client import MaximumFlowSolver

def run_example():
    print("=== GenPark Maximum Flow Solver Example ===")
    solver = MaximumFlowSolver()
    print("Max Flow:", solver.benchmark_max_flow())

if __name__ == "__main__":
    run_example()
