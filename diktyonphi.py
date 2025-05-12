import enum
import subprocess
from typing import Dict, Hashable, Any, Optional, Iterator, Tuple


class GraphType(enum.Enum):
    DIRECTED = 0
    UNDIRECTED = 1


class Edge:
    def __init__(self, src: 'Node', dest: 'Node', attrs: Dict[str, Any]):
        self.src = src
        self.dest = dest
        self._attrs = attrs

    def __getitem__(self, key: str) -> Any:
        return self._attrs[key]

    def __setitem__(self, key: str, val: Any) -> None:
        self._attrs[key] = val

    def __repr__(self):
        return f"Edge({self.src.id}→{self.dest.id}, {self._attrs})"


class Node:
    def __init__(self, graph: 'Graph', node_id: Hashable, attrs: Dict[str, Any]):
        self.id = node_id
        self.graph = graph
        self._attrs = attrs
        self._neighbors: Dict[Hashable, Dict[str, Any]] = {}

    def __getitem__(self, item: str) -> Any:
        return self._attrs[item]

    def __setitem__(self, item: str, val: Any) -> None:
        self._attrs[item] = val

    def to(self, dest: Hashable | 'Node') -> Edge:
        dest_id = dest.id if isinstance(dest, Node) else dest
        if dest_id not in self._neighbors:
            raise ValueError(f"No edge from {self.id} to {dest_id}")
        return Edge(self, self.graph.node(dest_id), self._neighbors[dest_id])

    def connect_to(self,  dest: Hashable | 'Node', attrs: Optional[Dict[str, Any]] = None):
        dest = dest if isinstance(dest, Node) else self.graph.node(dest)
        self.graph.add_edge(self.id, dest.id, attrs if attrs is not None else {})

    def is_edge_to(self, dest: Hashable | 'Node') -> bool:
        dest_id = dest.id if isinstance(dest, Node) else dest
        return dest_id in self._neighbors

    @property
    def neighbor_ids(self) -> Iterator[Hashable]:
        return iter(self._neighbors)

    @property
    def neighbors_nodes(self) -> Iterator['Node']:
        for id in self.neighbor_ids:
            yield self.graph.node(id)

    @property
    def out_degree(self) -> int:
        return len(self._neighbors)

    def __repr__(self):
        return f"Node({self.id}, {self._attrs})"

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Graph:
    def __init__(self, type: GraphType):
        self.type = type
        self._nodes: Dict[Hashable, Node] = {}

    def add_node(self, node_id: Hashable, attrs: Optional[Dict[str, Any]] = None) -> Node:
        if node_id in self._nodes:
            raise ValueError(f"Node {node_id} already exists")
        return self._create_node(node_id, attrs if attrs is not None else {})

    def add_edge(self, src_id: Hashable, dst_id: Hashable,
                 attrs: Optional[Dict[str, Any]] = None) -> Tuple[Node, Node]:
        attrs = attrs if attrs is not None else {}
        if src_id not in self._nodes:
            self._create_node(src_id, {})
        if dst_id not in self._nodes:
            self._create_node(dst_id, {})
        self._set_edge(src_id, dst_id, attrs)
        if self.type == GraphType.UNDIRECTED:
            self._set_edge(dst_id, src_id, attrs)
        return (self._nodes[src_id], self._nodes[dst_id])

    def __contains__(self, node_id: Hashable) -> bool:
        return node_id in self._nodes

    def __len__(self) -> int:
        return len(self._nodes)

    def __iter__(self) -> Iterator[Node]:
        return iter(self._nodes.values())

    def node_ids(self) -> Iterator[Hashable]:
        return iter(self._nodes.keys())

    def node(self, node_id: Hashable) -> Node:
        return self._nodes[node_id]

    def _create_node(self, node_id: Hashable, attrs: Optional[Dict[str, Any]] = None) -> Node:
        node = Node(self, node_id, attrs)
        self._nodes[node_id] = node
        return node

    def _set_edge(self, src_id: Hashable, target_id: Hashable, attrs: Dict[str, Any]) -> None:
        if target_id in self._nodes[src_id]._neighbors:
            raise ValueError(f"Edge {src_id}→{target_id} already exists")
        self._nodes[src_id]._neighbors[target_id] = attrs

    def __repr__(self):
        edges = sum(node.out_degree for node in self._nodes.values())
        if self.type == GraphType.UNDIRECTED:
            edges //= 2
        return f"Graph({self.type}, nodes: {len(self._nodes)}, edges: {edges})"

    def to_dot(self, label_attr="label", weight_attr="weight") -> str:
        lines = []
        name = "G"
        connector = "->" if self.type == GraphType.DIRECTED else "--"
        lines.append(f'digraph {name} {{' if self.type == GraphType.DIRECTED else f'graph {name} {{')
        for node_id in self.node_ids():
            node = self.node(node_id)
            label = node[label_attr] if label_attr in node._attrs else str(node_id)
            color = node._attrs.get("color", "black")
            lines.append(f'    "{node_id}" [label="{label}", color="{color}", style=filled, fillcolor="{color}"];')
        seen = set()
        for node_id in self.node_ids():
            node = self.node(node_id)
            for dst_id in node.neighbor_ids:
                if self.type == GraphType.UNDIRECTED and (dst_id, node_id) in seen:
                    continue
                seen.add((node_id, dst_id))
                edge = node.to(dst_id)
                label = edge[weight_attr] if weight_attr in edge._attrs else ""
                lines.append(f'    "{node_id}" {connector} "{dst_id}" [label="{label}"];')
        lines.append("}")
        return "\n".join(lines)

    def export_to_png(self, filename: str = None) -> None:
        dot_data = self.to_dot()
        subprocess.run(["dot", "-Tpng", "-o", filename], input=dot_data, text=True, check=True)
