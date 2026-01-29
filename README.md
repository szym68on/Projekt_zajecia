# ⚽ Football Team Evolution - Graph Visualization

A graph-based analysis and visualization tool for studying the evolution of football team compositions over time. Uses graph theory to represent players as nodes and their co-occurrence in matches as edges, with dynamic scoring to quantify changes between seasons.

## 📊 Dataset

- **Clubs**: 5 La Liga teams (Athletic Bilbao, Atlético Madrid, FC Barcelona, Real Madrid, Villarreal CF)
- **Timespan**: 20 seasons (2005-2025)
- **Graphs**: 100 total (5 clubs × 20 seasons)
- **Matches**: ~5,000 scraped from official sources
- **Representation**: Players as nodes, partnerships as edges, weighted by matches played together

## ✨ Features

- **Interactive Graph Visualization**: View team composition with node size representing matches played and edge thickness representing partnership strength
- **Statistics Panel**: Real-time metrics including player count, pair count, density, top partnerships, and key players
- **Dynamic Score Analysis**: Quantify team changes between seasons using V-Score (player changes) and E-Score (partnership changes)
- **Timeline Charts**: Visualize 20-year evolution with line charts showing biggest changes and stable periods

## 🔧 Requirements

- **Java**: 11 or higher
- **Maven**: 3.6 or higher
- **Python**: 3.7 or higher
- **Git**: For cloning the repository

---

## 📥 Installation Instructions

### Windows

#### 1. Install Prerequisites

**Java 11+**
```powershell
# Download from https://adoptium.net/
# Verify installation
java -version
```

**Maven 3.6+**
```powershell
# Download from https://maven.apache.org/download.cgi
# Extract to C:\Program Files\Apache\apache-maven-3.9.x
# Add to PATH (PowerShell as Administrator)
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Apache\apache-maven-3.9.x\bin", [System.EnvironmentVariableTarget]::Machine)

# Verify installation
mvn -version
```

**Python 3.7+**
```powershell
# Download from https://www.python.org/downloads/
# During installation, check "Add Python to PATH"
# Verify installation
python --version
```

#### 2. Clone Repository
```powershell
git clone https://github.com/your-repo/football-team-evolution.git
cd football-team-evolution
```

#### 3. Install Python Dependencies
```powershell
pip install -r requirements.txt --break-system-packages
```

#### 4. Build and Run Visualization
```powershell
cd visualization
mvn clean install
mvn exec:java
```

---

### macOS

#### 1. Install Prerequisites

**Homebrew** (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Java 11+**
```bash
brew install openjdk@11
# Add to PATH
echo 'export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
java -version
```

**Maven 3.6+**
```bash
brew install maven

# Verify installation
mvn -version
```

**Python 3.7+**
```bash
brew install python3

# Verify installation
python3 --version
```

#### 2. Clone Repository
```bash
git clone https://github.com/your-repo/football-team-evolution.git
cd football-team-evolution
```

#### 3. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

#### 4. Build and Run Visualization
```bash
cd visualization
mvn clean install
mvn exec:java
```

---

### Linux (Ubuntu/Debian)

#### 1. Install Prerequisites

**Java 11+**
```bash
sudo apt update
sudo apt install openjdk-11-jdk

# Verify installation
java -version
```

**Maven 3.6+**
```bash
sudo apt install maven

# Verify installation
mvn -version
```

**Python 3.7+**
```bash
sudo apt install python3 python3-pip

# Verify installation
python3 --version
```

#### 2. Clone Repository
```bash
git clone https://github.com/your-repo/football-team-evolution.git
cd football-team-evolution
```

#### 3. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

#### 4. Build and Run Visualization
```bash
cd visualization
mvn clean install
mvn exec:java
```

---

## 📂 Project Structure

```
football-team-evolution/
├── src/
│   └── python/
│       ├── football_teams_scrapper.py    # Data scraping
│       ├── format_converter.py           # JSON to text conversion
│       ├── graph_builder.py              # Graph generation
│       └── dynamic_score_calculator.py   # DynamicScore computation
├── visualization/
│   ├── src/main/java/
│   │   ├── GraphViewer.java             # Main application
│   │   ├── StatsPanel.java              # Statistics panel
│   │   ├── TimelineWindow.java          # Timeline charts
│   │   ├── DynamicScoreLoader.java      # JSON data loader
│   │   └── DynamicScoreData.java        # Data model
│   ├── pom.xml                          # Maven configuration
│   └── README.md
├── graphs/                               # Generated graph files (100 files)
├── dynamic_scores/                       # DynamicScore JSON files
├── formatted_data/                       # Converted data
├── football_data/                        # Raw scraped data
├── requirements.txt                      # Python dependencies
└── README.md                            # This file
```

## 🎮 Usage

### Main Application

1. **Select Club**: Choose from dropdown (Athletic Bilbao, Atlético Madrid, etc.)
2. **Select Season**: Choose year range (2005-2025)
3. **Load**: Display graph visualization
4. **Timeline**: View 20-year evolution chart with DynamicScore

### Graph Visualization 🎨

- **Node Size**: Proportional to matches played (larger = more matches)
- **Node Color**: Darker blue = more matches, lighter blue = fewer matches
- **Edge Thickness**: Proportional to matches played together
- **Edge Color**: Darker = stronger partnership, lighter = weaker partnership

### Statistics Panel 📈

- **Current Season**: Basic metrics (players, pairs, density)
- **Dynamic Score**: V-Score and E-Score for previous/next season transitions
- **Pairs**: Scrollable list of all partnerships sorted by strength
- **Players**: Scrollable list of all players sorted by matches played

### Timeline Window 📉

- **Line Chart**: V-Score (blue) and E-Score (orange) over 20 years
- **Interactive**: Click points to see specific seasons
- **Table**: Top 5 biggest changes with both scores

## 🔬 Technical Details

### Graph Representation

- **Vertices**: Players who appeared in starting lineups
- **Edges**: Two players connected if they played together in a match
- **Edge Weight**: Number of matches the pair played together in the season

### DynamicScore Metrics 📊

**V-DynamicScore** (Player Changes):
```
V-Score = |V_{t+1} △ V_t| / |V_{t+1} ∪ V_t|
```
where △ is symmetric difference (players who left + players who joined)

**E-DynamicScore** (Partnership Changes):
```
E-Score = |E_{t+1} △ E_t| / |E_{t+1} ∪ E_t|
```
where △ is symmetric difference (partnerships lost + partnerships gained)

### Technologies 🛠️

- **Backend**: Python 3.11 (scraping, data processing, analysis)
- **Frontend**: Java 11 (visualization, UI)
- **Libraries**:
  - NetworkX (graph analysis)
  - GraphStream 2.0 (graph rendering)
  - JFreeChart 1.5.4 (timeline charts)
  - Gson 2.10.1 (JSON parsing)
  - BeautifulSoup4 (web scraping)
- **Build Tool**: Maven 3.9

## 👥 Team

- Adam Waśko
- Szymon Świercz
- Aleksandra Szymańska
- Karolina Woch

**University**: Cardinal Stefan Wyszyński University in Warsaw
**Course**: Team Project  
**Year**: 2025/2026

## 📄 License

This project is part of academic coursework at UKSW.
