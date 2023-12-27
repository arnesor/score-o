"""Functions for working with the solutions from opsolver."""
import json
from pathlib import Path


def check_solution(filename: Path) -> None:
    """Check and extract information from the solution generated by opsolver."""
    with open(filename) as file:
        last_line = file.readlines()[-1]
    last_sol = json.loads(last_line)

    # print(last_sol)
    print(f"\nName: {last_sol['prob']['name']}-{last_sol['prob']['d0']}")
    print(f"  N       : {last_sol['sol']['sol_ns']}")
    print(f"  Score   : {last_sol['sol']['val']}")
    print(f"  Distance: {last_sol['sol']['cap']}")
    print(f"  Controls: {last_sol['sol']['cycle']}")
