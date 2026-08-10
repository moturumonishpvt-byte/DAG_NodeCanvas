from typing import List, Dict, Set, Any

def build_adjacency_list(nodes: List[Dict], edges: List[Dict]) -> Dict[str, List[str]]:
    """
    Builds an adjacency list representation of the graph.
    """
    adj_list = {node.get("id"): [] for node in nodes if "id" in node}
    
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source and target:
            if source in adj_list:
                adj_list[source].append(target)
            else:
                adj_list[source] = [target]
    return adj_list

def is_dag(nodes: List[Dict], edges: List[Dict]) -> bool:
    """
    Determines whether the given nodes and edges form a Directed Acyclic Graph (DAG).
    Uses Depth-First Search (DFS) to detect cycles.
    """
    adj_list = build_adjacency_list(nodes, edges)
    
    visited: Set[str] = set()
    rec_stack: Set[str] = set()
    
    def dfs(node_id: str) -> bool:
        """
        Returns True if a cycle is detected, False otherwise.
        """
        visited.add(node_id)
        rec_stack.add(node_id)
        
        for neighbor in adj_list.get(node_id, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
                
        rec_stack.remove(node_id)
        return False

    # Check all components of the graph
    for node_id in list(adj_list.keys()):
        if node_id not in visited:
            if dfs(node_id):
                return False # Cycle detected, not a DAG

    return True # No cycles detected, is a DAG

def calculate_pipeline_stats(nodes: List[Dict], edges: List[Dict]) -> Dict[str, Any]:
    """
    Calculates the required statistics for the pipeline.
    """
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    if num_nodes == 0 and num_edges == 0:
        is_dag_flag = True
    else:
        is_dag_flag = is_dag(nodes, edges)
        
    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag_flag
    }

