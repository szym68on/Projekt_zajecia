# 📋 TODO

## 🚀 Uruchomienie Projektu

### 1. Pobierz repo
```bash
git clone [URL_REPO]
cd PROJEKT_ZAJECIA
```

### 2. Zainstaluj Maven

**Opcja A: IntelliJ IDEA (Najłatwiejsza)**
- Pobierz **IntelliJ IDEA Community** (darmowe): [https://www.jetbrains.com/idea/download/](https://www.jetbrains.com/idea/download/other.html)
- Zainstaluj i otwórz
- File → Open → Wybierz folder `visualization/`
- IntelliJ automatycznie wykryje Maven i pobierze biblioteki
- Run → GraphViewer

**Opcja B: Maven z linii komend**
1. Pobierz: https://maven.apache.org/download.cgi (Binary zip)
2. Rozpakuj do: `C:\Program Files\Apache\apache-maven-3.9.12`
3. Dodaj do PATH (PowerShell jako Admin):
```powershell
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Apache\apache-maven-3.9.12\bin", [System.EnvironmentVariableTarget]::Machine)
```
4. Restart terminala i sprawdź: `mvn -version`

### 3. Zainstaluj biblioteki Python
```bash
pip install -r requirements.txt
```

Jeśli coś się wywala → zapytaj mnie albo ChatGPT

### 4. Uruchom wizualizację
```bash
cd visualization
mvn exec:java
```

**TERAZ MASZ GRAF!** 🎉

---

## 🎨 Propozycje Ulepszenia UI

### 1. Dropdown do wyboru sezonu
**Cel:** Możliwość przełączania między różnymi sezonami/klubami bez restartowania programu

**Propozycja narzędzi:**
- `JComboBox` (Java Swing) - dropdown menu
- `File.listFiles()` - lista plików z folderu `graphs/`
- `graph.clear()` (GraphStream) - czyszczenie obecnego grafu

**Co zrobić:**
1. Stwórz dropdown z nazwami wszystkich plików grafów
2. Po wyborze: wyczyść graf i wczytaj nowy plik
3. Dodaj panel z dropdownem do okna

### 2. Panel ze statystykami
**Cel:** Wyświetlanie kluczowych metryk grafu w czasie rzeczywistym

**Co pokazać:**
- Liczba graczy (węzłów)
- Liczba połączeń (krawędzi)
- Gęstość grafu
- Top 3-5 graczy z największą liczbą meczów

**Propozycja narzędzi:**
- `JPanel` + `JLabel` (Java Swing)
- `graph.getNodeCount()`, `graph.getEdgeCount()` (GraphStream)
- Layout: `BoxLayout` lub `GridLayout`

### 3. Eksport grafu do obrazu
**Cel:** Zapisywanie wizualizacji do pliku PNG

**Propozycja narzędzi:**
- GraphStream: `FileSinkImages`
- `JButton` do triggera eksportu
- Automatyczne generowanie nazwy pliku (np. z datą/nazwą klubu)

### 4. Animacja między sezonami
**Cel:** Automatyczne przełączanie grafów pokazujące ewolucję w czasie

**Pomysł:**
- Wczytuj kolejne sezony tego samego klubu co 2-3 sekundy
- Pokaż jak gracze pojawiają się i znikają

**Propozycja narzędzi:**
- `javax.swing.Timer` - cykliczne wykonywanie akcji
- `graph.addNode()`, `graph.removeNode()` (GraphStream) - dynamiczne zmiany
- Sortowanie plików po dacie/sezonie

### 5. Porównanie dwóch klubów
**Cel:** Zestawienie składów dwóch drużyn w tym samym sezonie

**Pomysł:**
- Dwa grafy obok siebie
- Barcelona 2015 vs Real Madrid 2015
- Podświetlenie graczy którzy grali w obu klubach (transfery)

**Propozycja narzędzi:**
- Dwa obiekty `Graph` w jednej aplikacji
- `JSplitPane` (Java Swing) - podział okna
- Porównanie list graczy między grafami

### 6. Wyszukiwarka gracza
**Cel:** Znalezienie wszystkich sezonów w których grał dany zawodnik

**Propozycja narzędzi:**
- `JTextField` do wpisania nazwiska
- Przeszukiwanie wszystkich plików grafów
- Wyświetlenie listy sezonów/klubów

### 7. Lepszy layout grafu
**Cel:** Czytelniejsze rozmieszczenie węzłów

**Narzędzia GraphStream:**
- `SpringBox` - siły odpychające/przyciągające
- `LinLog` - logarytmiczny layout
- Parametry: `quality`, `stabilization-limit`
- Dokumentacja: https://graphstream-project.org/doc/Algorithms/

---

## 💡 Przydatne Linki

- **IntelliJ IDEA Community** (DARMOWE): https://www.jetbrains.com/idea/download/
- **GraphStream Docs**: https://graphstream-project.org/
- **Java Swing Tutorial**: https://docs.oracle.com/javase/tutorial/uiswing/

---

**Powodzenia!** 🚀
