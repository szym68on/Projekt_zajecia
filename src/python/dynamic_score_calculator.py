"""
DynamicScore Calculator for Football Team Evolution Project
Calculates V-DynamicScore and E-DynamicScore between consecutive seasons
"""

import networkx as nx
import json
from pathlib import Path
from collections import defaultdict


def load_graph(filepath):
    """
    Load graph from GraphStream format file
    Format: EDGE player1 | player2 | weight | matches1 | matches2
    """
    G = nx.Graph()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith('EDGE'):
                continue
            
            parts = line[5:].split('|')  # Skip 'EDGE '
            if len(parts) < 5:
                continue
            
            player1 = parts[0].strip()
            player2 = parts[1].strip()
            weight = int(parts[2].strip())
            matches1 = int(parts[3].strip())
            matches2 = int(parts[4].strip())
            
            # Add nodes with matches attribute
            if player1 not in G:
                G.add_node(player1, matches=matches1)
            if player2 not in G:
                G.add_node(player2, matches=matches2)
            
            # Add edge with weight
            G.add_edge(player1, player2, weight=weight)
    
    return G


def calculate_v_dynamic_score(G_t, G_t1):
    """
    Calculate V-DynamicScore (vertex/player changes)
    Formula: |V_{t+1} △ V_t| / |V_{t+1} ∪ V_t|
    where △ is symmetric difference (A∪B - A∩B)
    """
    V_t = set(G_t.nodes())
    V_t1 = set(G_t1.nodes())
    
    symmetric_diff = V_t.symmetric_difference(V_t1)
    union = V_t.union(V_t1)
    
    if len(union) == 0:
        return 0.0
    
    return len(symmetric_diff) / len(union)


def calculate_e_dynamic_score(G_t, G_t1):
    """
    Calculate E-DynamicScore (edge/partnership changes)
    Formula: |E_{t+1} △ E_t| / |E_{t+1} ∪ E_t|
    """
    # Convert edges to frozensets for proper set operations
    E_t = set(frozenset(edge) for edge in G_t.edges())
    E_t1 = set(frozenset(edge) for edge in G_t1.edges())
    
    symmetric_diff = E_t.symmetric_difference(E_t1)
    union = E_t.union(E_t1)
    
    if len(union) == 0:
        return 0.0
    
    return len(symmetric_diff) / len(union)


def get_player_changes(G_t, G_t1):
    """
    Get lists of players who left and joined
    """
    V_t = set(G_t.nodes())
    V_t1 = set(G_t1.nodes())
    
    players_left = list(V_t - V_t1)
    players_joined = list(V_t1 - V_t)
    
    # Sort by number of matches (if available)
    players_left_with_matches = [(p, G_t.nodes[p].get('matches', 0)) for p in players_left]
    players_joined_with_matches = [(p, G_t1.nodes[p].get('matches', 0)) for p in players_joined]
    
    players_left_with_matches.sort(key=lambda x: x[1], reverse=True)
    players_joined_with_matches.sort(key=lambda x: x[1], reverse=True)
    
    return players_left_with_matches, players_joined_with_matches


def get_edge_changes(G_t, G_t1):
    """
    Get lists of edges (partnerships) that were lost and gained
    """
    E_t = set(frozenset(edge) for edge in G_t.edges())
    E_t1 = set(frozenset(edge) for edge in G_t1.edges())
    
    edges_lost_set = E_t - E_t1
    edges_gained_set = E_t1 - E_t
    
    # Convert back to list with weights
    edges_lost = []
    for edge in edges_lost_set:
        p1, p2 = list(edge)
        weight = G_t[p1][p2]['weight']
        edges_lost.append([p1, p2, weight])
    
    edges_gained = []
    for edge in edges_gained_set:
        p1, p2 = list(edge)
        weight = G_t1[p1][p2]['weight']
        edges_gained.append([p1, p2, weight])
    
    # Sort by weight (strongest partnerships first)
    edges_lost.sort(key=lambda x: x[2], reverse=True)
    edges_gained.sort(key=lambda x: x[2], reverse=True)
    
    return edges_lost, edges_gained


def process_season_pair(graph_t_path, graph_t1_path, club, season_t, season_t1):
    """
    Process a pair of consecutive seasons and calculate all metrics
    """
    G_t = load_graph(graph_t_path)
    G_t1 = load_graph(graph_t1_path)
    
    # Calculate DynamicScores
    v_score = calculate_v_dynamic_score(G_t, G_t1)
    e_score = calculate_e_dynamic_score(G_t, G_t1)
    
    # Get changes
    players_left, players_joined = get_player_changes(G_t, G_t1)
    edges_lost, edges_gained = get_edge_changes(G_t, G_t1)
    
    result = {
        "club": club,
        "season_from": season_t,
        "season_to": season_t1,
        "v_score": round(v_score, 3),
        "e_score": round(e_score, 3),
        "stats": {
            "total_players_t": G_t.number_of_nodes(),
            "total_players_t1": G_t1.number_of_nodes(),
            "total_edges_t": G_t.number_of_edges(),
            "total_edges_t1": G_t1.number_of_edges()
        },
        "players_left": [{"name": p, "matches": m} for p, m in players_left[:10]],  # Top 10
        "players_joined": [{"name": p, "matches": m} for p, m in players_joined[:10]],  # Top 10
        "edges_lost": [{"player1": e[0], "player2": e[1], "weight": e[2]} for e in edges_lost[:10]],  # Top 10
        "edges_gained": [{"player1": e[0], "player2": e[1], "weight": e[2]} for e in edges_gained[:10]]  # Top 10
    }
    
    return result


def process_all_clubs(graphs_dir, output_dir):
    """
    Process all clubs and all their consecutive seasons
    """
    graphs_path = Path(graphs_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Check if graphs directory exists
    if not graphs_path.exists():
        print(f"\nError: Graphs directory not found: {graphs_path}")
        print(f"Make sure you're running from the correct directory")
        print(f"Expected path: {graphs_path.absolute()}")
        return []
    
    # List all graph files to show user what exists
    all_files = list(graphs_path.glob("*_graph.txt"))
    if len(all_files) == 0:
        print(f"\nError: No graph files found in {graphs_path}")
        print(f"Expected files like: Barcelona_2015_2016_graph.txt")
        return []
    
    print(f"\nFound {len(all_files)} graph files in {graphs_path}")
    
    # Club names (matching actual file format)
    clubs = ["athletic_bilbao", "atletico_madryt", "fc_barcelona", "real_madryt", "villarreal_cf"]
    
    # Seasons from 2005-2006 to 2024-2025 (20 seasons, 19 transitions)
    seasons = [f"{year}_{year+1}" for year in range(2005, 2025)]
    
    all_results = []
    
    for club in clubs:
        print(f"\nProcessing {club}...")
        club_results = []
        
        for i in range(len(seasons) - 1):
            season_t = seasons[i]
            season_t1 = seasons[i + 1]
            
            graph_t_file = graphs_path / f"{club}_{season_t}_graph.txt"
            graph_t1_file = graphs_path / f"{club}_{season_t1}_graph.txt"
            
            if not graph_t_file.exists() or not graph_t1_file.exists():
                print(f"  Skipping {season_t} -> {season_t1} (files not found)")
                continue
            
            print(f"  {season_t} -> {season_t1}")
            result = process_season_pair(graph_t_file, graph_t1_file, club, season_t, season_t1)
            club_results.append(result)
            all_results.append(result)
        
        # Save club-specific results
        club_output_file = output_path / f"{club}_dynamic_scores.json"
        with open(club_output_file, 'w', encoding='utf-8') as f:
            json.dump(club_results, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved {len(club_results)} transitions to {club_output_file}")
    
    # Save all results combined
    all_output_file = output_path / "all_dynamic_scores.json"
    with open(all_output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Total: {len(all_results)} transitions processed")
    print(f"✓ Saved to {output_path}/")
    
    return all_results


def generate_summary_report(results, output_file):
    """
    Generate a summary report with rankings and statistics
    """
    if len(results) == 0:
        print("\n⚠ No transitions found - cannot generate summary report")
        return
    
    # Sort by V-Score
    v_sorted = sorted(results, key=lambda x: x['v_score'], reverse=True)
    
    # Sort by E-Score
    e_sorted = sorted(results, key=lambda x: x['e_score'], reverse=True)
    
    report = {
        "summary": {
            "total_transitions": len(results),
            "avg_v_score": round(sum(r['v_score'] for r in results) / len(results), 3),
            "avg_e_score": round(sum(r['e_score'] for r in results) / len(results), 3)
        },
        "top_v_changes": [
            {
                "club": r['club'],
                "transition": f"{r['season_from']} -> {r['season_to']}",
                "v_score": r['v_score']
            }
            for r in v_sorted[:10]
        ],
        "top_e_changes": [
            {
                "club": r['club'],
                "transition": f"{r['season_from']} -> {r['season_to']}",
                "e_score": r['e_score']
            }
            for r in e_sorted[:10]
        ],
        "most_stable_v": [
            {
                "club": r['club'],
                "transition": f"{r['season_from']} -> {r['season_to']}",
                "v_score": r['v_score']
            }
            for r in sorted(results, key=lambda x: x['v_score'])[:10]
        ],
        "most_stable_e": [
            {
                "club": r['club'],
                "transition": f"{r['season_from']} -> {r['season_to']}",
                "e_score": r['e_score']
            }
            for r in sorted(results, key=lambda x: x['e_score'])[:10]
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Summary report saved to {output_file}")
    
    # Print top changes
    print("\n=== TOP 10 BIGGEST PLAYER CHANGES (V-Score) ===")
    for i, item in enumerate(report['top_v_changes'], 1):
        print(f"{i}. {item['club']} {item['transition']}: {item['v_score']}")
    
    print("\n=== TOP 10 BIGGEST PARTNERSHIP CHANGES (E-Score) ===")
    for i, item in enumerate(report['top_e_changes'], 1):
        print(f"{i}. {item['club']} {item['transition']}: {item['e_score']}")


if __name__ == "__main__":
    # Paths (script is in src/python/, graphs is at root level)
    GRAPHS_DIR = "../../graphs"
    OUTPUT_DIR = "../../dynamic_scores"
    
    print("=" * 60)
    print("DynamicScore Calculator")
    print("Football Team Evolution Project")
    print("=" * 60)
    
    # Process all clubs
    results = process_all_clubs(GRAPHS_DIR, OUTPUT_DIR)
    
    # Generate summary report
    summary_file = Path(OUTPUT_DIR) / "summary_report.json"
    generate_summary_report(results, summary_file)
    
    print("\n" + "=" * 60)
    print("✓ Processing complete!")
    print("=" * 60)