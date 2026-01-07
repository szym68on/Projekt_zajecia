# ⚽ Football Team Evolution Analysis

Analysis and visualization of football team composition evolution over 20 seasons (2005-2025) using graph theory.

## 🎯 Project Goal

Visualize how football team lineups evolve over time by representing players as graph nodes and their co-occurrences in matches as edges.

## 📊 Dataset

- **5 La Liga clubs**: Athletic Bilbao, Atlético Madrid, FC Barcelona, Real Madrid, Villarreal CF
- **20 seasons**: 2005/2006 - 2024/2025
- **100 season graphs** generated
- **~5,000 matches** analyzed

## 🚀 Quick Start

### 1. Python - Data Processing
```bash
# Install dependencies
pip install -r requirements.txt

# Convert data (if needed)
python src/python/format_converter.py

# Build all graphs
python src/python/build_all_graphs.py
```

### 2. Java - Visualization
```bash
cd visualization

# Compile
mvn clean compile

# Run (default: Barcelona 2015/2016)
mvn exec:java

# Run custom graph
mvn exec:java -Dexec.args="../graphs/real_madryt_2024_2025_graph.txt"
```

## 📁 Project Structure
```
PROJEKT_ZAJECIA/
├── src/python/              # Data processing scripts
│   ├── football_teams_scrapper.py
│   ├── format_converter.py
│   ├── graph_builder.py
│   └── build_all_graphs.py
├── visualization/           # Java GraphStream viewer
│   ├── pom.xml
│   └── src/main/java/GraphViewer.java
├── football_data/           # Raw scraped data (JSON)
├── formatted_data/          # Converted to simple text format
├── graphs/                  # Graph files (100 seasons)
├── requirements.txt
└── README.md
```

## 🔧 Requirements

- **Python**: 3.7+
- **Java**: 11+
- **Maven**: 3.6+

## ✅ What's Done

- [x] Data scraping (Selenium + Transfermarkt)
- [x] Data format conversion (JSON → TXT)
- [x] Graph generation (NetworkX)
- [x] Basic visualization (GraphStream)
- [x] 100 complete season graphs

## 🎯 Next Steps (See TODO.md)

- Animation between seasons
- Comparative analysis (club vs club)
- Advanced graph metrics
- Export capabilities
- LaTeX report

## 📝 Graph Format

**Nodes**: Players  
**Edges**: Co-occurrence in matches  
**Edge weights**: Number of matches played together  
**Node size**: Total matches played

## 👥 Team

Cardinal Stefan Wyszyński University - Computer Science  
Adam Waśko
Szymon Świercz
Aleksandra Szymańska
Karolina Woch

## 📄 License

Educational project - UKSW 2025