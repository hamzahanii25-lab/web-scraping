import requests
from bs4 import BeautifulSoup
import csv
import os


# pip install requests
# pip install beautifulsoup4
# pip install lxml

def get_match_info(championship, matches_details):
    """Extract match information from a championship section."""
    try:
        championship_title = championship.contents[1].find("h2").text.strip()
        all_matches = championship.contents[3].find_all('li')
        number_of_matches = len(all_matches)
        
        print(f"Processing {number_of_matches} matches in {championship_title}")
        
        for i in range(number_of_matches):
            try:
                # Get teams names 
                team_A = all_matches[i].find('div', {'class': 'teamA'}).text.strip()
                team_B = all_matches[i].find('div', {'class': 'teamB'}).text.strip()

                # Get score 
                match_result = all_matches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
                score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

                # Get match time
                match_time = all_matches[i].find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

                # Add match info to matches_details 
                matches_details.append({
                    "نوع البطوله": championship_title,
                    "الفريق الاول": team_A,
                    "الفريق الثانى": team_B,
                    "ميعاد المباراه": match_time,
                    "النتيجه": score
                })
                print(f"Added match: {team_A} vs {team_B}")
            except Exception as e:
                print(f"Error processing match {i} in {championship_title}: {e}")
    except Exception as e:
        print(f"Error processing championship: {e}")

def save_to_csv(matches_details):
    """Save matches details to a CSV file."""
    try:
        if not matches_details:
            print("No matches found for the given date.")
            return

        output_dir = 'document/yallakora'
        os.makedirs(output_dir, exist_ok=True)
        output_file = f'{output_dir}/matches-details.csv'

        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            dict_writer = csv.DictWriter(f, matches_details[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)
        print(f"Successfully saved {len(matches_details)} matches to {output_file}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main(page):
    """Main function to process the webpage and extract match information."""
    try:
        src = page.content
        soup = BeautifulSoup(src, "lxml")
        matches_details = []

        championships = soup.find_all("div", {'class': 'matchCard'})
        print(f"Found {len(championships)} championship sections")

        if not championships:
            print("No championships found. Please check if the date is correct.")
            return

        for championship in championships:
            get_match_info(championship, matches_details)

        save_to_csv(matches_details)

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    print("YallaKora Match Scraper")
    print("----------------------")
    
    # Get date input and fetch page
    date = input("Please enter a date (MM/DD/YY): ")
    try:
        url = f"https://www.yallakora.com/match-center?date={date}"
        print(f"Fetching data from: {url}")
        
        page = requests.get(url)
        page.raise_for_status()
        print("Successfully connected to the website")
        
        main(page)
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        exit(1)








