# 📋 TODO

## 🚀 Uruchomienie Projektu

### 1. Pobierz repo
```bash
git clone [URL_REPO]
cd PROJEKT_ZAJECIA
```

### 2. Zainstaluj biblioteki
```bash
# Python
pip install -r requirements.txt

# Java/Maven
cd visualization
mvn clean compile
```

Jeśli coś się wywala → zapytaj mnie albo ChatGPT

### 3. Uruchom wizualizację
```bash
cd visualization
mvn exec:java
```

**TERAZ MASZ GRAF!** 🎉

---

## 🎨 Propozycje Ulepszenia UI

### 1. Dropdown do wyboru sezonu

**Co dodać:**
- Menu dropdown z listą wszystkich grafów
- Po wyborze: wyczyść obecny graf i wczytaj nowy

**Jak to zrobić:**
```java
import javax.swing.*;
import java.io.File;

// Dodaj w GraphViewer:
JFrame frame = new JFrame("Select Season");
JComboBox<String> dropdown = new JComboBox<>();

// Załaduj pliki
File graphsDir = new File("../graphs");
for (File f : graphsDir.listFiles()) {
    dropdown.addItem(f.getName());
}

// Po wyborze: wczytaj nowy graf
dropdown.addActionListener(e -> {
    graph.clear();
    loadGraph("../graphs/" + dropdown.getSelectedItem());
});
```

### 2. Panel ze statystykami

**Co pokazać:**
- Liczba graczy
- Liczba połączeń
- Gęstość grafu
- Top 3 graczy (najwięcej meczów)

**Jak to zrobić:**
```java
import javax.swing.*;

JPanel statsPanel = new JPanel();
statsPanel.setLayout(new BoxLayout(statsPanel, BoxLayout.Y_AXIS));

// Po wczytaniu grafu:
statsPanel.add(new JLabel("Players: " + graph.getNodeCount()));
statsPanel.add(new JLabel("Connections: " + graph.getEdgeCount()));
statsPanel.add(new JLabel("Density: " + calculateDensity()));

// Dodaj panel do okna
```

### 3. Przycisk "Eksport do PNG"

**Jak to zrobić:**
```java
JButton exportButton = new JButton("Export to PNG");
exportButton.addActionListener(e -> {
    graph.write("graph_export.png");
    System.out.println("✅ Saved to graph_export.png");
});
```

### 4. Animacja między sezonami

**Pomysł:**
- Automatycznie przełączaj między sezonami co 2 sekundy
- Pokaż jak skład ewoluuje w czasie

**Hint:**
```java
Timer timer = new Timer(2000, e -> {
    // Wczytaj następny sezon
    loadNextSeason();
});
timer.start();
```

---

## 💡 Przydatne Linki

- GraphStream Docs: https://graphstream-project.org/
- Java Swing Tutorial: https://docs.oracle.com/javase/tutorial/uiswing/

---

**Powodzenia!** 🚀
