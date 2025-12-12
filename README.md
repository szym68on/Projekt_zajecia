# ⚽ Football Teams Data Scraper

Automated web scraper for extracting detailed match lineup data from Transfermarkt.pl. The project enables mass data collection across multiple seasons for selected football teams.

## 📋 Description

This scraper uses Selenium with Firefox to extract comprehensive match information, including:
- Starting XI lineups
- Substitute players who entered the match
- Competition and matchday information
- Match dates
- Home and away teams

## 🎯 Features

- **Mass scraping**: Download data for multiple teams and seasons in a single run
- **Checkpoint system**: Automatic progress saving every N matches
- **Intelligent delays**: Randomized wait times between requests (3-45s) to avoid IP blocking
- **Dual format output**: Data saved as both JSON and text reports
- **Summary report**: Automatic generation of comprehensive summary (_SUMMARY_REPORT.json)
- **Headless mode**: Option to run without browser window
- **Error handling**: Graceful handling with continuation on individual request failures

## 🚀 Requirements

### Software
- Python 3.7+
- Firefox
- geckodriver (Firefox driver)

### Python Libraries
```
selenium
```

## 📦 Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd <repo-directory>
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install selenium
```

4. **Install geckodriver**

**Linux/Mac:**
```bash
# Download from https://github.com/mozilla/geckodriver/releases
# Extract and move to /usr/local/bin/
```

**Windows:**
- Download from https://github.com/mozilla/geckodriver/releases
- Add to PATH or place in project folder

## 💻 Usage

### Basic Usage

1. **Configure teams and seasons** in `football_teams_scrapper.py`:

```python
TEAMS_CONFIG = [
    {
        'name': 'FC Barcelona',
        'url': 'https://www.transfermarkt.pl/fc-barcelona/spielplan/verein/131',
        'seasons': [2024, 2023, 2022, 2021, 2020]
    },
    {
        'name': 'Real Madrid',
        'url': 'https://www.transfermarkt.pl/real-madrid/spielplan/verein/418',
        'seasons': [2024, 2023, 2022]
    }
]
```

2. **Run the scraper**:
```bash
python football_teams_scrapper.py
```

3. **Follow the prompts**:
   - Confirm scraping start (y/n)
   - Choose headless mode (y/n)

### Advanced Usage

```python
from football_teams_scrapper import TransfermarktMassScraper

# Create scraper instance
scraper = TransfermarktMassScraper(headless=True)

# Define configuration
teams_config = [
    {
        'name': 'Athletic Bilbao',
        'url': 'https://www.transfermarkt.pl/athletic-bilbao/spielplan/verein/621',
        'seasons': [2023, 2022, 2021]
    }
]

# Run scraping
results = scraper.scrape_multiple_teams_seasons(
    teams_config=teams_config,
    output_dir="my_football_data"
)

# Close scraper
scraper.close()
```

## 📂 Output Data Structure

### JSON Format
```json
[
  {
    "url": "https://www.transfermarkt.pl/.../aufstellung/spielbericht/2899906",
    "match_id": "2899906",
    "date": "Mon, 09.04.2018",
    "competition": "LALIGA",
    "matchday": "31st Matchday",
    "home_team": "Villarreal CF",
    "away_team": "Athletic Bilbao",
    "home_players": [
      {
        "number": "1",
        "name": "Sergio Asenjo",
        "substituted_in": true,
        "starting_lineup": true
      }
    ],
    "away_players": [...]
  }
]
```

### Output Files
```
football_data/
├── _SUMMARY_REPORT.json              # Comprehensive summary
├── athletic_bilbao_2023_2024.json    # JSON data
├── athletic_bilbao_2023_2024.txt     # Text report
├── athletic_bilbao_2023_2024_checkpoint_5.json   # Checkpoint
└── ...
```

## ⚙️ Configuration Parameters

### TransfermarktMassScraper

**`__init__(headless=False)`**
- `headless`: Run without browser window (default: False)

**`scrape_multiple_teams_seasons(teams_config, output_dir="scraped_data")`**
- `teams_config`: List of dictionaries with team configurations
- `output_dir`: Output folder (default: "scraped_data")

**`scrape_season(team_url, season, output_file=None, checkpoint_interval=5)`**
- `team_url`: Team URL on Transfermarkt
- `season`: Season start year (e.g., 2023 for 2023/2024 season)
- `output_file`: Output filename
- `checkpoint_interval`: Checkpoint save frequency

## ⏱️ Estimated Runtime

- **1 season**: ~3 minutes (depending on number of matches)
- **10 seasons**: ~30-45 minutes
- **50 seasons**: ~2-3 hours

*Time includes intelligent delays between requests*

## 🛡️ Safety Mechanisms

1. **Random delays**:
   - After page load: 3-5s
   - Between matches: 5-10s
   - Between seasons: 15-25s
   - Between teams: 30-45s

2. **Checkpoint system**: Automatic progress saving

3. **Error handling**: Continuation on individual request failures

## 🐛 Troubleshooting

### "geckodriver not found"
```bash
# Make sure geckodriver is in PATH
# or install via package manager:
sudo apt install firefox-geckodriver  # Ubuntu/Debian
brew install geckodriver              # macOS
```

### Firefox crashes in headless mode
- Update Firefox and geckodriver to latest version
- Check console logs

## 📊 Sample Data

Currently in repository:
- **5 teams**: Villarreal CF, Athletic Bilbao, [...]
- **Season ranges**: 2005-2025
- **Total matches**: ~1000+ (depends on configuration)