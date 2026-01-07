"""
Build All Graphs: Process all formatted data and generate graph files
Batch processing script that creates graph files for all clubs and seasons.
Output files are ready for visualization in Java/GraphStream.
"""

from pathlib import Path
from graph_builder import FootballGraphBuilder

def build_all_graphs():
    """Process all formatted data files and generate graphs"""
    
    project_root = Path(__file__).parent.parent.parent
    formatted_dir = project_root / 'formatted_data'
    graphs_dir = project_root / 'graphs'
    graphs_dir.mkdir(exist_ok=True)
    
    txt_files = sorted(formatted_dir.glob('*.txt'))
    
    print(f"🔄 Processing {len(txt_files)} files...\n")
    
    success = 0
    errors = 0
    
    for i, txt_file in enumerate(txt_files, 1):
        output_name = txt_file.stem + '_graph.txt'
        output_file = graphs_dir / output_name
        
        print(f"\n{'='*60}")
        print(f"[{i}/{len(txt_files)}] Processing: {txt_file.name}")
        print(f"{'='*60}")
        
        try:
            builder = FootballGraphBuilder(str(txt_file))
            builder.load_data()
            builder.build_graph()
            builder.calculate_statistics()
            builder.save_for_java(str(output_file))
            success += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"📊 FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Success: {success} files")
    print(f"❌ Errors: {errors} files")
    print(f"📁 Output directory: {graphs_dir}")
    print(f"{'='*60}")


if __name__ == "__main__":
    build_all_graphs()
    print("\n✅ All graphs generated!")