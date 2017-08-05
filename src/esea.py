import re
import cfscrape
from bs4 import BeautifulSoup

class Team:
    def __init__(self, name, win, loss, tie, rf, ra):
        self.name = name
        self.win = int(win)
        self.loss = int(loss)
        self.tie = int(tie)
        self.rf = int(rf)
        self.ra = int(ra)

    def __gt__(self, team2):
        if self.win > team2.win:
            return True
        elif self.win < team2.win:
            return False
        elif self.win == team2.win and self.rf > team2.rf:
            return True
        elif self.win == team2.win and self.rf < team2.rf:
            return False
        elif self.win == team2.win and self.ra < team2.ra:
            return True
        else:
            return False

    def __repr__(self):
        return "{0:<30} {1:>2} {2:>2} {3:>2} {4:>3} {5:>3}".format(self.name, self.win, self.loss, self.tie, self.rf, self.ra)

    def __str__(self):
        return "{0:<30} {1:>2} {2:>2} {3:>2} {4:>3} {5:>3}".format(self.name, self.win, self.loss, self.tie, self.rf, self.ra)

def scrape_teams(url="https://play.esea.net/index.php?s=league&d=standings&division_id=2925"):
    scraper = cfscrape.create_scraper()

    page = scraper.get(url).content

    # Setup beautifulsoup
    page_bs = BeautifulSoup(page, "html.parser")

    # Get rows
    rows = page_bs.find_all("tr", attrs={"class": re.compile("row[12]")})

    # Extract name, win, loss, tie, rf, ra
    teams = []
    for row in rows:
        t_name = row.find("a", attrs={"href": re.compile("/teams/")}).get_text()
        stats = [elem.get_text() for elem in row.select("td.stat")] # 0 = W, 1 = L, 2 = T, 5 = RF, 6 = RA
        teams.append(Team(t_name, stats[0], stats[1], stats[2], stats[5], stats[6]))

    # Sort teams
    teams.sort(reverse=True)

    # Save standings to a file
    with open("standings.txt", 'w') as f:
        f.write("      {0:^30} {1:^2} {2:^2} {3:^2} {4:^3} {5:^3}\n".format("Name", "W", "L", "T", "RF", "RA"))
        i = 1
        for team in teams:
            f.write("{:>4}. ".format(i))
            f.write("{}".format(team))
            f.write("\n")
            i += 1

    print("Done!")

def main():
    url = raw_input('Enter the esea division url: ')
    scrape_teams(url)

if __name__ == "__main__":
    main()