from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
import random
from datetime import datetime
import os

class TransfermarktMassScraper:
    def __init__(self, headless=False):
        """
        Mass scraper - multiple teams, multiple seasons
        """
        print("🦊 Starting Firefox...")
        
        firefox_options = Options()
        if headless:
            firefox_options.add_argument('--headless')
            print("   (Headless mode - no browser window)")
        
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()
        
        print("✅ Firefox ready!\n")
    
    def scrape_multiple_teams_seasons(self, teams_config, output_dir="scraped_data"):
        """
        Scrape multiple teams and seasons
        
        Args:
            teams_config: list of dictionaries with team configuration
                [
                    {
                        'name': 'FC Barcelona',
                        'url': 'https://www.transfermarkt.pl/fc-barcelona/spielplan/verein/131',
                        'seasons': [2024, 2023, 2022]
                    },
                    ...
                ]
            output_dir: output folder
        """
        # Create data folder
        os.makedirs(output_dir, exist_ok=True)
        
        total_teams = len(teams_config)
        total_seasons = sum(len(team['seasons']) for team in teams_config)
        
        print("="*100)
        print(f"🎯 MASS SCRAPING")
        print("="*100)
        print(f"📊 Teams: {total_teams}")
        print(f"📅 Total seasons: {total_seasons}")
        print(f"💾 Output folder: {output_dir}/")
        print(f"⏱️  Estimated time: ~{total_seasons * 3} minutes (with delays)")
        print("="*100)
        print()
        
        all_results = []
        completed = 0
        failed = 0
        
        for team_idx, team in enumerate(teams_config, 1):
            print("\n" + "▓"*100)
            print(f"🏟️  TEAM {team_idx}/{total_teams}: {team['name']}")
            print("▓"*100 + "\n")
            
            for season_idx, season in enumerate(team['seasons'], 1):
                print(f"\n{'='*80}")
                print(f"📅 Season {season_idx}/{len(team['seasons'])}: {season}/{season+1}")
                print(f"   Overall progress: {completed}/{total_seasons} ({(completed/total_seasons*100):.1f}%)")
                print('='*80)
                
                try:
                    # Filename
                    team_slug = re.sub(r'[^\w\s-]', '', team['name'].lower())
                    team_slug = re.sub(r'[\s_]+', '_', team_slug)
                    output_file = os.path.join(output_dir, f"{team_slug}_{season}_{season+1}.txt")
                    
                    # Scrape season
                    matches = self.scrape_season(
                        team_url=team['url'],
                        season=season,
                        output_file=output_file,
                        checkpoint_interval=5
                    )
                    
                    if matches:
                        all_results.append({
                            'team': team['name'],
                            'season': f"{season}/{season+1}",
                            'matches': len(matches),
                            'file': output_file,
                            'status': 'success'
                        })
                        completed += 1
                        print(f"\n✅ Success! Saved {len(matches)} matches to: {output_file}")
                    else:
                        all_results.append({
                            'team': team['name'],
                            'season': f"{season}/{season+1}",
                            'matches': 0,
                            'file': output_file,
                            'status': 'no_data'
                        })
                        failed += 1
                        print(f"\n⚠️  No data for this season")
                    
                    # LONG DELAY between seasons (15-25 seconds)
                    if season_idx < len(team['seasons']):
                        wait_time = random.randint(15, 25)
                        print(f"\n⏳ Waiting {wait_time} seconds before next season...")
                        time.sleep(wait_time)
                    
                except Exception as e:
                    print(f"\n❌ Error for {team['name']} {season}/{season+1}: {e}")
                    all_results.append({
                        'team': team['name'],
                        'season': f"{season}/{season+1}",
                        'matches': 0,
                        'file': None,
                        'status': 'error',
                        'error': str(e)
                    })
                    failed += 1
                    import traceback
                    traceback.print_exc()
            
            # VERY LONG DELAY between teams (30-45 seconds)
            if team_idx < total_teams:
                wait_time = random.randint(30, 45)
                print(f"\n\n💤 Waiting {wait_time} seconds before next team...")
                print("   (This helps avoid IP blocking)")
                time.sleep(wait_time)
        
        # Summary
        print("\n\n" + "="*100)
        print("📊 MASS SCRAPING SUMMARY")
        print("="*100)
        print(f"✅ Completed: {completed}/{total_seasons}")
        print(f"❌ Failed: {failed}/{total_seasons}")
        print(f"📁 Saved to: {output_dir}/")
        
        # Save report
        report_file = os.path.join(output_dir, "_SUMMARY_REPORT.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_teams': total_teams,
                'total_seasons': total_seasons,
                'completed': completed,
                'failed': failed,
                'results': all_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Report saved: {report_file}")
        print("="*100)
        
        return all_results
    
    def scrape_season(self, team_url, season, output_file=None, checkpoint_interval=5):
        """
        Automatically scrape entire season for a team
        """
        if output_file is None:
            output_file = f"season_{season}.txt"
        
        print(f"🎯 Starting scraping for season {season}/{season+1}")
        
        # Open schedule
        schedule_url = f"{team_url}/saison_id/{season}"
        print(f"🌐 Opening schedule: {schedule_url}")
        self.driver.get(schedule_url)
        
        # RANDOM DELAY after page load (3-5 seconds)
        wait_time = random.uniform(3, 5)
        time.sleep(wait_time)
        
        # Find links to all matches
        match_links = self._find_match_links()
        
        if not match_links:
            print("❌ No matches found!")
            return []
        
        print(f"✅ Found {len(match_links)} matches to process")
        
        # Scrape each match
        all_matches = []
        
        for idx, match_url in enumerate(match_links, 1):
            print(f"\n🔍 Match {idx}/{len(match_links)}")
            
            try:
                match_data = self._scrape_single_match(match_url)
                
                if match_data:
                    all_matches.append(match_data)
                    
                    # Count starting lineup vs substitutes who entered
                    home_starting = sum(1 for p in match_data['home_players'] if p.get('starting_lineup'))
                    away_starting = sum(1 for p in match_data['away_players'] if p.get('starting_lineup'))
                    home_subs = len(match_data['home_players']) - home_starting
                    away_subs = len(match_data['away_players']) - away_starting
                    
                    print(f"   ✅ {match_data['home_team']} vs {match_data['away_team']}")
                    print(f"      📊 {match_data.get('competition', 'Unknown')} - {match_data.get('matchday', 'Unknown')}")
                    print(f"      🏠 {home_starting}+{home_subs} | ✈️  {away_starting}+{away_subs}")
                else:
                    print(f"   ⚠️  Skipped (no data)")
                
                # Checkpoint every N matches
                if idx % checkpoint_interval == 0:
                    checkpoint_file = output_file.replace('.txt', f'_checkpoint_{idx}.json')
                    self._save_checkpoint(all_matches, checkpoint_file)
                    print(f"   💾 Checkpoint: {idx}/{len(match_links)}")
                
                # RANDOM DELAY between matches (2-4 seconds)
                if idx < len(match_links):
                    wait_time = random.uniform(2, 4)
                    time.sleep(wait_time)
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                continue
        
        print(f"\n✅ Completed: {len(all_matches)}/{len(match_links)} matches")
        
        # Save final results
        if all_matches:
            self._save_results(all_matches, output_file)
        
        return all_matches
    
    def _find_match_links(self):
        """Find all links to match reports"""
        match_links = []
        
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".box")))
            
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/spielbericht/index/spielbericht/']")
            
            for link in links:
                href = link.get_attribute('href')
                if href and href not in match_links:
                    match_links.append(href)
            
            match_links = list(set(match_links))
            
        except Exception as e:
            print(f"⚠️  Error finding links: {e}")
        
        return match_links
    
    def _scrape_single_match(self, match_url):
        """Scrape single match"""
        self.driver.get(match_url)
        time.sleep(2)
        
        match_id = match_url.split('/')[-1]
        
        # Extract team names
        home_team = None
        away_team = None
        
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".box")))
            
            # METHOD 1: Page header
            try:
                team_containers = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='sb-team'], .sb-heim, .sb-gast")
                
                if len(team_containers) >= 2:
                    home_link = team_containers[0].find_element(By.CSS_SELECTOR, "a[href*='/startseite/verein/']")
                    home_team = home_link.text.strip()
                    
                    away_link = team_containers[1].find_element(By.CSS_SELECTOR, "a[href*='/startseite/verein/']")
                    away_team = away_link.text.strip()
            except:
                pass
            
            # METHOD 2: Page title
            if not home_team or not away_team:
                try:
                    page_title = self.driver.title
                    if ' - ' in page_title:
                        parts = page_title.split(' - ')
                        if len(parts) >= 2:
                            home_team = parts[0].strip()
                            away_team = parts[1].split(',')[0].strip()
                except:
                    pass
            
            if not home_team or not away_team:
                return None
            
        except Exception as e:
            return None
        
        # Build lineup URL
        home_slug = self._slugify_team_name(home_team)
        away_slug = self._slugify_team_name(away_team)
        
        lineup_url = f"https://www.transfermarkt.pl/{home_slug}_{away_slug}/aufstellung/spielbericht/{match_id}"
        
        self.driver.get(lineup_url)
        time.sleep(2)
        
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".box")))
        except:
            return None
        
        match_date = self._get_match_date()
        competition_info = self._get_competition_info()
        
        match_data = {
            'url': lineup_url,
            'match_id': match_id,
            'date': match_date,
            'competition': competition_info.get('competition', 'Unknown'),
            'matchday': competition_info.get('matchday', 'Unknown'),
            'home_team': home_team,
            'away_team': away_team,
            'home_players': [],
            'away_players': []
        }
        
        formations = self.driver.find_elements(By.CSS_SELECTOR, ".row.sb-formation")
        
        if len(formations) >= 2:
            starting_section = formations[0]
            columns = starting_section.find_elements(By.CSS_SELECTOR, ".large-6.columns")
            
            if len(columns) >= 2:
                home_starting = self._extract_lineup_from_table(columns[0], is_bench=False)
                away_starting = self._extract_lineup_from_table(columns[1], is_bench=False)
            else:
                home_starting = []
                away_starting = []
            
            bench_section = formations[1]
            columns = bench_section.find_elements(By.CSS_SELECTOR, ".large-6.columns")
            
            if len(columns) >= 2:
                home_bench = self._extract_lineup_from_table(columns[0], is_bench=True)
                away_bench = self._extract_lineup_from_table(columns[1], is_bench=True)
            else:
                home_bench = []
                away_bench = []
            
            match_data['home_players'] = home_starting + [p for p in home_bench if p.get('substituted_in')]
            match_data['away_players'] = away_starting + [p for p in away_bench if p.get('substituted_in')]
        else:
            return None
        
        return match_data
    
    def _slugify_team_name(self, team_name):
        """Convert team name to URL slug"""
        slug = team_name.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    def _get_match_date(self):
        """Get match date"""
        try:
            date_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='waspassiertheute']")
            if date_elements:
                return date_elements[0].text.strip()
        except:
            pass
        
        try:
            date_element = self.driver.find_element(By.CSS_SELECTOR, ".sb-datum a")
            return date_element.text.strip()
        except:
            pass
        
        return "Unknown date"
    
    def _get_competition_info(self):
        """Get competition and matchday information"""
        info = {'competition': 'Unknown', 'matchday': 'Unknown'}
        
        try:
            try:
                matchday_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/jumplist/spieltag/']")
                if matchday_links:
                    info['matchday'] = matchday_links[0].text.strip()
            except:
                pass
            
            try:
                comp_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/startseite/wettbewerb/']")
                if comp_links:
                    for link in comp_links:
                        comp_text = link.text.strip()
                        if comp_text and len(comp_text) > 2:
                            info['competition'] = comp_text
                            break
            except:
                pass
            
        except Exception as e:
            pass
        
        return info
    
    def _extract_lineup_from_table(self, section, is_bench=False):
        """Extract players from table"""
        players = []
        
        try:
            table = section.find_element(By.CSS_SELECTOR, "table.items")
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                try:
                    number_div = row.find_element(By.CSS_SELECTOR, ".rn_nummer")
                    number = number_div.text.strip()
                    
                    name_link = row.find_element(By.CSS_SELECTOR, "a.wichtig")
                    name = name_link.text.strip()
                    name = re.split(r'\(|\s\(', name)[0].strip()
                    
                    if not name or not number:
                        continue
                    
                    player = {
                        'number': number,
                        'name': name,
                        'substituted_in': False,
                        'starting_lineup': not is_bench
                    }
                    
                    if is_bench:
                        substituted_in = False
                        
                        try:
                            row.find_element(By.CSS_SELECTOR, ".sb-sprite.sb-ein")
                            substituted_in = True
                        except:
                            pass
                        
                        if not substituted_in:
                            try:
                                imgs = row.find_elements(By.TAG_NAME, "img")
                                for img in imgs:
                                    title = img.get_attribute("title")
                                    if title and "substituted in" in title.lower():
                                        substituted_in = True
                                        break
                            except:
                                pass
                        
                        player['substituted_in'] = substituted_in
                    else:
                        player['substituted_in'] = True
                    
                    players.append(player)
                    
                except:
                    continue
                    
        except Exception as e:
            pass
        
        return players
    
    def _save_checkpoint(self, matches, filename):
        """Save checkpoint"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)
    
    def _save_results(self, matches, output_file):
        """Save final results"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("                        FOOTBALL TEAM - SEASON MATCHES REPORT\n")
            f.write("=" * 100 + "\n\n")
            
            f.write(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"⚽ Total matches: {len(matches)}\n")
            
            if matches:
                total_home_players = sum(len(m['home_players']) for m in matches)
                total_away_players = sum(len(m['away_players']) for m in matches)
                total_players = total_home_players + total_away_players
                avg_players = total_players / len(matches)
                
                competitions = {}
                for m in matches:
                    comp = m.get('competition', 'Unknown')
                    competitions[comp] = competitions.get(comp, 0) + 1
                
                f.write(f"👥 Total players tracked: {total_players}\n")
                f.write(f"📊 Average players per match: {avg_players:.1f}\n\n")
                
                f.write("🏆 Competitions breakdown:\n")
                for comp, count in competitions.items():
                    f.write(f"   • {comp}: {count} matches\n")
                
            f.write("\n" + "=" * 100 + "\n\n")
            
            for idx, match in enumerate(matches, 1):
                f.write("\n" + "▓" * 100 + "\n")
                f.write(f"MATCH #{idx:02d}\n")
                f.write("▓" * 100 + "\n\n")
                
                f.write(f"🏠 HOME:  {match['home_team']}\n")
                f.write(f"✈️  AWAY:  {match['away_team']}\n")
                f.write(f"📅 DATE:  {match['date']}\n")
                f.write(f"🏆 COMP:  {match.get('competition', 'Unknown')}\n")
                f.write(f"🔢 ROUND: {match.get('matchday', 'Unknown')}\n")
                f.write(f"🔗 URL:   {match['url']}\n")
                
                f.write("\n" + "-" * 100 + "\n")
                
                home_starting = [p for p in match['home_players'] if p.get('starting_lineup')]
                home_subs = [p for p in match['home_players'] if not p.get('starting_lineup')]
                
                f.write(f"\n🏠 {match['home_team'].upper()} - {len(match['home_players'])} players\n")
                f.write("-" * 100 + "\n")
                
                if home_starting:
                    f.write("   ⭐ STARTING XI:\n")
                    for p in home_starting:
                        f.write(f"      {p['number']:>3}. {p['name']}\n")
                
                if home_subs:
                    f.write(f"\n   🔄 SUBSTITUTES IN ({len(home_subs)}):\n")
                    for p in home_subs:
                        f.write(f"      {p['number']:>3}. {p['name']}\n")
                
                away_starting = [p for p in match['away_players'] if p.get('starting_lineup')]
                away_subs = [p for p in match['away_players'] if not p.get('starting_lineup')]
                
                f.write(f"\n✈️  {match['away_team'].upper()} - {len(match['away_players'])} players\n")
                f.write("-" * 100 + "\n")
                
                if away_starting:
                    f.write("   ⭐ STARTING XI:\n")
                    for p in away_starting:
                        f.write(f"      {p['number']:>3}. {p['name']}\n")
                
                if away_subs:
                    f.write(f"\n   🔄 SUBSTITUTES IN ({len(away_subs)}):\n")
                    for p in away_subs:
                        f.write(f"      {p['number']:>3}. {p['name']}\n")
                
                all_players = match['home_players'] + match['away_players']
                player_names = [p['name'] for p in all_players]
                competition = match.get('competition', 'Unknown').replace('|', '-')
                matchday = match.get('matchday', 'Unknown').replace('|', '-')
                
                f.write(f"\n" + "-" * 100 + "\n")
                f.write("📋 PARSE FORMAT:\n")
                f.write(f"{match['date']}|{competition}|{matchday}|{match['home_team']}|{match['away_team']}|{'|'.join(player_names)}\n")
                f.write("\n")
        
        json_file = output_file.replace('.txt', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)
    
    def close(self):
        """Close browser"""
        print("\n🔒 Closing browser...")
        self.driver.quit()


# ==================== CONFIGURATION ====================

TEAMS_CONFIG = [


    {
        'name': 'Villarreal CF',
        'url': 'https://www.transfermarkt.pl/fc-villarreal/spielplan/verein/1050',
        'seasons': [2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005]
    },
    {
        'name': 'Athletic Bilbao',
        'url': 'https://www.transfermarkt.pl/athletic-bilbao/spielplan/verein/621',
        'seasons': [2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005]
    },
]

# ==================== EXECUTION ====================

if __name__ == "__main__":
    print("🚀 Transfermarkt MASS Scraper")
    print("="*100)
    print()
    
    print("📋 CONFIGURATION:")
    for team in TEAMS_CONFIG:
        print(f"   • {team['name']}: {len(team['seasons'])} seasons ({min(team['seasons'])}-{max(team['seasons'])+1})")
    print()
    
    # Confirmation
    response = input("❓ Start scraping? This may take ~90-120 minutes. (y/n): ")
    
    if response.lower() != 'y':
        print("❌ Cancelled.")
        exit()
    
    # Headless option
    use_headless = input("❓ Use headless mode (no browser window)? (y/n): ")
    headless = use_headless.lower() == 'y'
    
    print("\n" + "="*100)
    print("🚀 STARTING MASS SCRAPING...")
    print("="*100)
    
    # Create scraper
    scraper = TransfermarktMassScraper(headless=headless)
    
    try:
        # Scrape everything
        results = scraper.scrape_multiple_teams_seasons(
            teams_config=TEAMS_CONFIG,
            output_dir="football_data"
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.close()
    
    print("\n✅ Done!")