from graph_utils import calculate_pipeline_stats, is_dag

def test_empty_graph():
    stats = calculate_pipeline_stats([], [])
    assert stats["num_nodes"] == 0, f'Expected 0, got {stats["num_nodes"]}'
    assert stats["num_edges"] == 0
    assert stats["is_dag"] is True
    print("test_empty_graph passed")

def test_single_node():
    stats = calculate_pipeline_stats([{"id": "1"}], [])
    assert stats["num_nodes"] == 1
    assert stats["num_edges"] == 0
    assert stats["is_dag"] is True
    print("test_single_node passed")

def test_multiple_nodes_no_edges():
    stats = calculate_pipeline_stats([{"id": "1"}, {"id": "2"}], [])
    assert stats["num_nodes"] == 2
    assert stats["num_edges"] == 0
    assert stats["is_dag"] is True
    print("test_multiple_nodes_no_edges passed")

def test_valid_dag():
    nodes = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    edges = [{"source": "1", "target": "2"}, {"source": "1", "target": "3"}]
    stats = calculate_pipeline_stats(nodes, edges)
    assert stats["num_nodes"] == 3
    assert stats["num_edges"] == 2
    assert stats["is_dag"] is True
    print("test_valid_dag passed")

def test_graph_with_cycle():
    nodes = [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    edges = [
        {"source": "1", "target": "2"},
        {"source": "2", "target": "3"},
        {"source": "3", "target": "1"}
    ]
    stats = calculate_pipeline_stats(nodes, edges)
    assert stats["num_nodes"] == 3
    assert stats["num_edges"] == 3
    assert stats["is_dag"] is False
    print("test_graph_with_cycle passed")

def test_multiple_disconnected_dags():
    nodes = [{"id": "1"}, {"id": "2"}, {"id": "3"}, {"id": "4"}]
    edges = [
        {"source": "1", "target": "2"},
        {"source": "3", "target": "4"}
    ]
    stats = calculate_pipeline_stats(nodes, edges)
    assert stats["num_nodes"] == 4
    assert stats["num_edges"] == 2
    assert stats["is_dag"] is True
    print("test_multiple_disconnected_dags passed")

def test_multiple_components_one_cycle():
    nodes = [{"id": "1"}, {"id": "2"}, {"id": "3"}, {"id": "4"}]
    edges = [
        {"source": "1", "target": "2"},
        {"source": "3", "target": "4"},
        {"source": "4", "target": "3"}
    ]
    stats = calculate_pipeline_stats(nodes, edges)
    assert stats["num_nodes"] == 4
    assert stats["num_edges"] == 3
    assert stats["is_dag"] is False
    print("test_multiple_components_one_cycle passed")

if __name__ == "__main__":
    test_empty_graph()
    test_single_node()
    test_multiple_nodes_no_edges()
    test_valid_dag()
    test_graph_with_cycle()
    test_multiple_disconnected_dags()
    test_multiple_components_one_cycle()
    print("All graph tests passed!")
