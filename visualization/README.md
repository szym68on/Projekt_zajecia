# Football Graph Visualization

Basic GraphStream viewer for football team evolution graphs.

## Requirements

- Java 11+
- Maven 3.6+

## Build
```bash
cd visualization
mvn clean compile
```

## Run

### Default (Barcelona 2015/2016):
```bash
mvn exec:java
```

### Custom graph:
```bash
mvn exec:java -Dexec.args="../graphs/real_madryt_2024_2025_graph.txt"
```

## Controls

- **Drag nodes**: Reorganize layout
- **Mouse wheel**: Zoom
- **Drag background**: Pan

## Features

- Node size = number of matches
- Edge thickness = matches played together
- Interactive layout

## For Development

Add more features:
- Season comparison
- Animation between seasons
- Player statistics panel
- Export to image