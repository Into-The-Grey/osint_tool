import networkx as nx

class GraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def add_results(self, results):
        for entity in results.get("entities", []):
            self.graph.add_node(entity["value"], type=entity["type"], details=entity.get("details", {}))
        for relation in results.get("relations", []):
            source = relation["source"]
            target = relation["target"]
            rel_type = relation.get("relation", "")
            self.graph.add_edge(source, target, relation=rel_type)

    def get_data(self):
        data = {"nodes": [], "edges": []}
        for node, attrs in self.graph.nodes(data=True):
            data["nodes"].append({
                "value": node,
                "type": attrs.get("type"),
                "details": attrs.get("details")
            })
        for u, v, attrs in self.graph.edges(data=True):
            data["edges"].append({
                "source": u,
                "target": v,
                "relation": attrs.get("relation", "")
            })
        return data
