import pytest
from backend.models import Node, Edge, PipelineData
from backend.graph_utils import is_dag, calculate_pipeline_stats

def test_empty_graph():
    pipeline = PipelineData(nodes=[], edges=[])
    stats = calculate_pipeline_stats(pipeline)
    assert stats["num_nodes"] == 0
    assert stats["num_edges"] == 0
    assert stats["is_dag"] is True

def test_single_node():
    pipeline = PipelineData(nodes=[Node(id="1")], edges=[])
    stats = calculate_pipeline_stats(pipeline)
    assert stats["num_nodes"] == 1
    assert stats["num_edges"] == 0
    assert stats["is_dag"] is True

def test_multiple_nodes_no_edges():
    pipeline = PipelineData(nodes=[Node(id="1"), Node(id="2"), Node(id="3")], edges=[])
    stats = calculate_pipeline_stats(pipeline)
    assert stats["num_nodes"] == 3
    assert stats["num_edges"] == 0
    assert stats["is_dag"] is True

def test_valid_dag():
    nodes = [Node(id="1"), Node(id="2"), Node(id="3"), Node(id="4")]
    edges = [Edge(source="1", target="2"), Edge(source="1", target="3"), Edge(source="2", target="4"), Edge(source="3", target="4")]
    pipeline = PipelineData(nodes=nodes, edges=edges)
    stats = calculate_pipeline_stats(pipeline)
    assert stats["num_nodes"] == 4
    assert stats["num_edges"] == 4
    assert stats["is_dag"] is True

def test_graph_with_cycle():
    nodes = [Node(id="1"), Node(id="2"), Node(id="3")]
    # 1 -> 2 -> 3 -> 1
    edges = [Edge(source="1", target="2"), Edge(source="2", target="3"), Edge(source="3", target="1")]
    pipeline = PipelineData(nodes=nodes, edges=edges)
    stats = calculate_pipeline_stats(pipeline)
    assert stats["num_nodes"] == 3
    assert stats["num_edges"] == 3
    assert stats["is_dag"] is False

def test_multiple_disconnected_dags():
    nodes = [Node(id="1"), Node(id="2"), Node(id="3"), Node(id="4")]
    # Comp 1: 1 -> 2
    # Comp 2: 3 -> 4
    edges = [Edge(source="1", target="2"), Edge(source="3", target="4")]
    pipeline = PipelineData(nodes=nodes, edges=edges)
    stats = calculate_pipeline_stats(pipeline)
    assert stats["num_nodes"] == 4
    assert stats["num_edges"] == 2
    assert stats["is_dag"] is True
    
def test_multiple_components_one_cycle():
    nodes = [Node(id="1"), Node(id="2"), Node(id="3"), Node(id="4")]
    # Comp 1: 1 -> 2
    # Comp 2: 3 -> 4 -> 3
    edges = [Edge(source="1", target="2"), Edge(source="3", target="4"), Edge(source="4", target="3")]
    pipeline = PipelineData(nodes=nodes, edges=edges)
    stats = calculate_pipeline_stats(pipeline)
    assert stats["num_nodes"] == 4
    assert stats["num_edges"] == 3
    assert stats["is_dag"] is False
