import json
from pathlib import Path

class SimpleFormatConverter:
    def __init__(self, json_file, output_file):
        self.json_file = json_file
        self.output_file = output_file
    
    def convert(self):
        """Convert JSON to simple text format"""
        
        # Load JSON
        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different structures
        if isinstance(data, dict):
            matches = [data]
        elif isinstance(data, list):
            matches = data
        else:
            print(f"❌ Unknown structure: {self.json_file}")
            return
        
        if not matches or len(matches) == 0:
            print(f"⚠️  No matches in: {self.json_file}")
            return
        
        # Check first match structure
        first_match = matches[0]
        if not isinstance(first_match, dict) or 'home_team' not in first_match:
            print(f"❌ Invalid match structure in: {self.json_file}")
            return
        
        # Detect team name (most frequent)
        team_counts = {}
        for match in matches:
            if not isinstance(match, dict):
                continue
            home = match.get('home_team', '')
            away = match.get('away_team', '')
            if home:
                team_counts[home] = team_counts.get(home, 0) + 1
            if away:
                team_counts[away] = team_counts.get(away, 0) + 1
        
        if not team_counts:
            print(f"❌ No teams found in: {self.json_file}")
            return
        
        team_name = max(team_counts.items(), key=lambda x: x[1])[0]
        
        print(f"📊 Team: {team_name}")
        print(f"⚽ Matches: {len(matches)}")
        
        # Save in simple format
        with open(self.output_file, 'w', encoding='utf-8') as out:
            out.write(f"# Team: {team_name}\n")
            out.write(f"# Format: MATCH: id | date | opponent\n")
            out.write(f"#         PLAYERS: player1, player2, ...\n\n")
            
            for match in matches:
                if not isinstance(match, dict):
                    continue
                
                # Determine if our team is home or away
                if match.get('home_team') == team_name:
                    players = match.get('home_players', [])
                    opponent = match.get('away_team', 'Unknown')
                else:
                    players = match.get('away_players', [])
                    opponent = match.get('home_team', 'Unknown')
                
                # Only starting lineup (11 players)
                starting_lineup = [
                    p['name'] for p in players 
                    if isinstance(p, dict) and p.get('starting_lineup', False)
                ]
                
                # Skip match if no players
                if not starting_lineup:
                    continue
                
                # Save match
                match_id = match.get('match_id', 'unknown')
                match_date = match.get('date', 'unknown')
                
                out.write(f"MATCH: {match_id} | {match_date} | {opponent}\n")
                out.write(f"PLAYERS: {', '.join(starting_lineup)}\n\n")
        
        print(f"✅ Saved: {self.output_file}")


def convert_all_clubs():
    """Convert all JSON files to simple text format"""
    
    # Use relative paths from project root
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'football_data'
    output_dir = project_root / 'formatted_data'
    output_dir.mkdir(exist_ok=True)
    
    # Find all final JSONs (skip checkpoints)
    json_files = [f for f in data_dir.glob('*.json') if 'checkpoint' not in f.name]
    
    print(f"🔄 Converting {len(json_files)} files...\n")
    
    success = 0
    errors = 0
    
    for json_file in json_files:
        output_name = json_file.stem + '.txt'
        output_path = output_dir / output_name
        
        try:
            converter = SimpleFormatConverter(str(json_file), str(output_path))
            converter.convert()
            success += 1
        except Exception as e:
            print(f"❌ Error in {json_file.name}: {e}")
            errors += 1
        
        print()
    
    print(f"\n{'='*60}")
    print(f"✅ Success: {success} files")
    print(f"❌ Errors: {errors} files")
    print(f"{'='*60}")


if __name__ == "__main__":
    convert_all_clubs()
    print("\n✅ Conversion completed!")