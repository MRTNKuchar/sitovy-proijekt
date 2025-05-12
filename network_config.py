from diktyonphi import Graph, GraphType

DEVICE_COLORS = {
    "router": "red",
    "switch": "orange",
    "client": "skyblue",
    "server": "green",
    "ap": "violet",
    "nas": "brown",
    "mobile": "pink"
}

def build_network() -> Graph:
    g = Graph(GraphType.DIRECTED)

    # 🧩 Definice uzlů (zařízení)
    devices = {
        # Routery
        "R1": {"label": "Router 1", "type": "router"},
        "R2": {"label": "Router 2", "type": "router"},
        "R3": {"label": "Router 3", "type": "router"},
        "R4": {"label": "Router 4", "type": "router"},
        "R5": {"label": "Router 5", "type": "router"},

        # Počítače
        "PC1": {"label": "PC 1", "type": "client"},
        "PC2": {"label": "PC 2", "type": "client"},
        "PC3": {"label": "PC 3", "type": "client"},
        "PC4": {"label": "PC 4", "type": "client"},

        # Servery
        "S1": {"label": "Web Server", "type": "server"},
        "S2": {"label": "DB Server", "type": "server"},

        # NAS úložiště
        "NAS": {"label": "NAS", "type": "nas"},

        # Mobilní zařízení
        "M1": {"label": "Smartphone", "type": "mobile"},
        "M2": {"label": "Tablet", "type": "mobile"},

        # Přístupový bod
        "AP1": {"label": "Wi-Fi AP", "type": "ap"}
    }

    for node_id, attrs in devices.items():
        attrs["color"] = DEVICE_COLORS.get(attrs["type"], "gray")
        g.add_node(node_id, attrs)

    # 🔁 Redundantní propojení mezi routery (částečná mesh)
    mesh_edges = [
        ("R1", "R2", 1.0),
        ("R1", "R3", 2.0),
        ("R1", "R4", 2.5),
        ("R2", "R3", 1.2),
        ("R2", "R4", 2.2),
        ("R3", "R4", 1.1),
        ("R3", "R5", 2.3),
        ("R4", "R5", 1.0),
        ("R2", "R5", 2.4),
        ("R1", "R5", 2.8),
    ]

    # 🔌 Připojení koncových zařízení
    device_edges = [
        ("PC1", "R1", 1.0),
        ("PC2", "R2", 1.0),
        ("PC3", "R3", 1.0),
        ("PC4", "R4", 1.0),
        ("R5", "S1", 1.5),
        ("R4", "S2", 1.6),
        ("R3", "NAS", 2.0),
        ("R2", "AP1", 1.3),
        ("AP1", "M1", 0.5),
        ("AP1", "M2", 0.5),
    ]

    for src, dst, weight in mesh_edges + device_edges:
        g.add_edge(src, dst, {"weight": weight})

    return g
