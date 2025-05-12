
import argparse
from network_config import build_network
from analysis import bfs, dfs, dijkstra_path
import os

def main():
    parser = argparse.ArgumentParser(description="Analýza počítačové sítě")
    parser.add_argument("--bfs", help="Spustí BFS od zadaného uzlu")
    parser.add_argument("--dfs", help="Spustí DFS od zadaného uzlu")
    parser.add_argument("--dijkstra", nargs=2, metavar=("START", "END"), help="Najde nejkratší cestu z START do END")
    parser.add_argument("--output", choices=["png", "svg"], default="png", help="Typ výstupního souboru (png nebo svg)")
    args = parser.parse_args()

    print("=== GENERUJI GRAF SÍTĚ ===")
    g = build_network()

    filename = "network"

    if args.bfs:
        bfs(g, args.bfs)
        filename = f"network_bfs_{args.bfs}"

    if args.dfs:
        dfs(g, args.dfs)
        filename = f"network_dfs_{args.dfs}"

    if args.dijkstra:
        start, end = args.dijkstra
        dijkstra_path(g, start, end)
        filename = f"network_dijkstra_{start}_{end}"

    print("=== EXPORTUJÍ VÝSTUP ===")
    if args.output == "png":
        g.export_to_png(f"{filename}.png")
        print(f"Uloženo jako {filename}.png")
    elif args.output == "svg":
        svg = g.to_image()
        with open(f"{filename}.svg", "w", encoding="utf-8") as f:
            f.write(svg.data)
        print(f"Uloženo jako {filename}.svg")

if __name__ == "__main__":
    main()
