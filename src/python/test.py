# Quick check script
from pathlib import Path

clubs = ['athletic_bilbao', 'atletico_madryt', 'fc_barcelona', 'real_madryt', 'villarreal_cf']
seasons = list(range(2005, 2025))  # 2005-2024 = 20 sezonów

formatted_dir = Path('formatted_data')
graphs_dir = Path('graphs')

print("Checking for missing files...\n")

for club in clubs:
    txt_count = len(list(formatted_dir.glob(f'{club}_*.txt')))
    graph_count = len(list(graphs_dir.glob(f'{club}_*_graph.txt')))
    
    print(f"{club}:")
    print(f"  TXT files: {txt_count}/20")
    print(f"  Graph files: {graph_count}/20")
    
    if txt_count < 20 or graph_count < 20:
        # Find missing
        for year in seasons:
            txt_file = formatted_dir / f"{club}_{year}_{year+1}.txt"
            if not txt_file.exists():
                print(f"  ❌ MISSING: {year}/{year+1}")