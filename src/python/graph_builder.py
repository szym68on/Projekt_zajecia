"""
Graph Builder: Build co-occurrence graph from match data
Creates a graph where nodes are players and edges represent matches played together.
Edge weights = number of matches two players played together.
"""

import networkx as nx
from pathlib import Path
from collections import defaultdict

class FootballGraphBuilder:
    def __init__(self, txt_file):
        self.txt_file = txt_file
        self.graph = nx.Graph()
        self.matches = []
        self.player_stats = defaultdict(lambda: {'matches': 0, 'partners': set()})
        
    def load_data(self):
        """Load data from text file"""
        print(f"📂 Loading: {Path(self.txt_file).name}")
        
        with open(self.txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_match = None
        
        for line in lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            # New match
            if line.startswith('MATCH:'):
                parts = line.split('|')
                match_id = parts[0].replace('MATCH:', '').strip()
                date = parts[1].strip() if len(parts) > 1 else ''
                opponent = parts[2].strip() if len(parts) > 2 else ''
                current_match = {'id': match_id, 'date': date, 'opponent': opponent}
            
            # Players
            elif line.startswith('PLAYERS:'):
                if current_match:
                    players_str = line.replace('PLAYERS:', '').strip()
                    players = [p.strip() for p in players_str.split(',')]
                    current_match['players'] = players
                    self.matches.append(current_match)
        
        print(f"✅ Loaded {len(self.matches)} matches")
        return self
    
    def build_graph(self):
        """Build co-occurrence graph"""
        print(f"🔨 Building graph...")
        
        for match in self.matches:
            players = match['players']
            
            # Add nodes
            for player in players:
                if not self.graph.has_node(player):
                    self.graph.add_node(player, matches=0)
                
                # Increment match counter
                self.graph.nodes[player]['matches'] += 1
                self.player_stats[player]['matches'] += 1
            
            # Add edges (every player with every other player in the lineup)
            for i, player1 in enumerate(players):
                for player2 in players[i+1:]:
                    if self.graph.has_edge(player1, player2):
                        # Increase weight
                        self.graph[player1][player2]['weight'] += 1
                    else:
                        # Add new edge
                        self.graph.add_edge(player1, player2, weight=1)
                    
                    # Statistics
                    self.player_stats[player1]['partners'].add(player2)
                    self.player_stats[player2]['partners'].add(player1)
        
        print(f"✅ Graph ready:")
        print(f"   - Players: {self.graph.number_of_nodes()}")
        print(f"   - Connections: {self.graph.number_of_edges()}")
        
        return self
    
    def calculate_statistics(self):
        """Calculate graph statistics"""
        print(f"\n{'='*60}")
        print("📊 GRAPH STATISTICS")
        print(f"{'='*60}")
        
        # Basic stats
        print(f"Players: {self.graph.number_of_nodes()}")
        print(f"Connections: {self.graph.number_of_edges()}")
        print(f"Density: {nx.density(self.graph):.3f}")
        
        # Top players by number of matches
        top_players = sorted(
            [(node, data['matches']) for node, data in self.graph.nodes(data=True)],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        print(f"\n🏆 Top 10 players (by matches):")
        for i, (player, matches) in enumerate(top_players, 1):
            partners = len(self.player_stats[player]['partners'])
            print(f"   {i:2}. {player:30} - {matches} matches, {partners} partners")
        
        # Strongest connections
        top_edges = sorted(
            [(u, v, d['weight']) for u, v, d in self.graph.edges(data=True)],
            key=lambda x: x[2],
            reverse=True
        )[:5]
        
        print(f"\n🤝 Top 5 pairs (most matches together):")
        for i, (p1, p2, weight) in enumerate(top_edges, 1):
            print(f"   {i}. {p1} ↔ {p2}: {weight} matches")
        
        # Centrality
        degree_centrality = nx.degree_centrality(self.graph)
        top_central = sorted(
            degree_centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        print(f"\n⭐ Top 5 centrality (most important):")
        for i, (player, centrality) in enumerate(top_central, 1):
            print(f"   {i}. {player:30} - {centrality:.3f}")
        
        print(f"{'='*60}\n")
        
        return self
    
    def save_for_java(self, output_file):
        """Save graph in format easy to read for Java"""
        print(f"💾 Saving graph for Java: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write(f"# Graph for Java/GraphStream\n")
            f.write(f"# Nodes: {self.graph.number_of_nodes()}\n")
            f.write(f"# Edges: {self.graph.number_of_edges()}\n\n")
            
            # Format: player1 | player2 | weight
            f.write("# Format: EDGE player1 | player2 | weight | matches1 | matches2\n\n")
            
            for u, v, data in self.graph.edges(data=True):
                weight = data['weight']
                matches_u = self.graph.nodes[u]['matches']
                matches_v = self.graph.nodes[v]['matches']
                
                f.write(f"EDGE {u} | {v} | {weight} | {matches_u} | {matches_v}\n")
        
        print(f"✅ Saved!")
        return self


def main():
    """Example usage for one file"""
    
    # Use relative paths from project root
    project_root = Path(__file__).parent.parent.parent
    txt_file = project_root / 'formatted_data' / 'fc_barcelona_2015_2016.txt'
    output_file = project_root / 'graphs' / 'fc_barcelona_2015_2016_graph.txt'
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Build graph
    builder = FootballGraphBuilder(str(txt_file))
    builder.load_data()
    builder.build_graph()
    builder.calculate_statistics()
    builder.save_for_java(str(output_file))
    
    print("\n✅ Done! Graph saved and ready for Java.")


if __name__ == "__main__":
    main()