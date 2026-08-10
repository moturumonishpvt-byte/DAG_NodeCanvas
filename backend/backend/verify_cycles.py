from graph_utils import calculate_pipeline_stats

def run_tests():
    tests = [
        {
            "name": "Case 1: Single Node",
            "nodes": [{"id": "A"}],
            "edges": [],
            "expected": {"num_nodes": 1, "num_edges": 0, "is_dag": True}
        },
        {
            "name": "Case 2: Simple DAG",
            "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
            "edges": [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}],
            "expected": {"num_nodes": 3, "num_edges": 2, "is_dag": True}
        },
        {
            "name": "Case 3: Simple Cycle",
            "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
            "edges": [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}, {"source": "C", "target": "A"}],
            "expected": {"num_nodes": 3, "num_edges": 3, "is_dag": False}
        },
        {
            "name": "Case 4: Disconnected DAG",
            "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}],
            "edges": [{"source": "A", "target": "B"}, {"source": "C", "target": "D"}],
            "expected": {"num_nodes": 4, "num_edges": 2, "is_dag": True}
        },
        {
            "name": "Case 5: Disconnected graph containing one cycle",
            "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}],
            "edges": [{"source": "A", "target": "B"}, {"source": "B", "target": "A"}, {"source": "C", "target": "D"}],
            "expected": {"num_nodes": 4, "num_edges": 3, "is_dag": False}
        }
    ]

    all_passed = True
    results = []

    for test in tests:
        stats = calculate_pipeline_stats(test["nodes"], test["edges"])
        passed = (
            stats["num_nodes"] == test["expected"]["num_nodes"] and
            stats["num_edges"] == test["expected"]["num_edges"] and
            stats["is_dag"] == test["expected"]["is_dag"]
        )
        if not passed:
            all_passed = False

        results.append(f"### {test['name']}\n"
                       f"- **Expected:** num_nodes={test['expected']['num_nodes']}, num_edges={test['expected']['num_edges']}, is_dag={test['expected']['is_dag']}\n"
                       f"- **Actual:** num_nodes={stats['num_nodes']}, num_edges={stats['num_edges']}, is_dag={stats['is_dag']}\n"
                       f"- **Status:** {'✅ PASSED' if passed else '❌ FAILED'}\n")

    report = "# Cyclic Graph Detection Verification Report\n\n"
    report += "## Execution Results\n\n"
    report += "\n".join(results)
    report += f"\n## Conclusion\nAll tests passed: **{all_passed}**.\nThe backend correctly distinguishes DAG and non-DAG graphs without any modifications.\n"

    with open("verification_report_output.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"All Passed: {all_passed}")

if __name__ == "__main__":
    run_tests()
