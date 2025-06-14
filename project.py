import pandas as pd
import matplotlib.pyplot as plt
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') #to accomodate UTF-8

fd = pd.read_csv("Info.csv")

fd.dropna() #removing null valued entries

# Aggregate goals by club across all seasons
TeamGoals = fd.groupby("Club")["Goals"].sum()
plt.barh(TeamGoals.index, TeamGoals.values, color='orange')
plt.xlim(0, 250)  
plt.xlabel("Goals Scored")
plt.ylabel("Team Name")
plt.tight_layout()
plt.legend()
plt.show()

# Scorer of max scoring team
MaxGoals = TeamGoals[TeamGoals == TeamGoals.max()].reset_index()
MaxScoringTeam = MaxGoals["Club"].iloc[0]
Max = fd[fd["Club"] == MaxScoringTeam] # get the max scoring team name


# Aggregate goals by player for pie chart
PlayerGoals = Max.groupby("PlayerName")["Goals"].sum()
plt.pie(PlayerGoals.values, labels=PlayerGoals.index, autopct='%1.1f%%')
plt.title("Goal Distribution of Maximum Scoring Team")
plt.tight_layout()
plt.savefig('Max Scoring Team.png')
plt.show()
# overall information about max scoring player

#  Aggregate player stats across seasons
PlayerStats = Max.groupby("PlayerName").agg({
    "Goals": "sum",
    "Assists": "sum", 
    "MatchesPlayed": "sum"
}).reset_index()

NoOfGoals = PlayerStats["Goals"].max()
Playerinfo = PlayerStats[PlayerStats["Goals"] == NoOfGoals].iloc[0]

# Get the values for the bar chart
stats = Playerinfo[["MatchesPlayed", "Goals", "Assists"]]
plt.bar(stats.index, stats.values, color="green")
playername = Playerinfo["PlayerName"]
plt.title(f"{playername}'s Performance")
plt.ylabel("Count")
plt.savefig('Max Scoring Team analysis.png')
plt.show()

# Now I will get Team red and yellow cards
Cards = fd.groupby("Club")["RedCards"].sum().reset_index()
Cards["YellowCards"] = fd.groupby("Club")["YellowCards"].sum().values
Cards["TotalCards"] = Cards["YellowCards"] + Cards["RedCards"]

fig, ax = plt.subplots(1, 2, figsize=(6, 5))
ax[0].barh(Cards["Club"], Cards["YellowCards"], color='Yellow')
ax[1].barh(Cards["Club"], Cards["RedCards"], color='Red')
ax[0].set_title('Yellow Cards of Teams')
ax[1].set_title('Red Cards of Teams')
fig.suptitle("Cards by teams")
plt.tight_layout()
plt.savefig("Team Bookings.png")
plt.show()

season_comparison = fd.groupby(["Season", "Club"])["Goals"].sum().reset_index()
pivot_seasons = season_comparison.pivot(index="Club", columns="Season", values="Goals").fillna(0)
pivot_seasons.plot(kind='bar', stacked=False, figsize=(10, 6))  # Add figsize here instead
plt.title("Goals by Team Across Seasons")
plt.xlabel("Team")
plt.ylabel("Goals")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('Goals Per Season.png')
plt.show()

# scatter plot to compare all forwards
Forwards = fd[fd["Position"] == 'Forward']
ForwardsAgg = Forwards.groupby("PlayerName").agg({
    "Goals": "sum",
    "MatchesPlayed": "sum"
}).reset_index()

plt.scatter(ForwardsAgg["MatchesPlayed"], ForwardsAgg["Goals"])

for i in range(len(ForwardsAgg)):
    plt.text(ForwardsAgg["MatchesPlayed"].iloc[i],
             ForwardsAgg["Goals"].iloc[i],
             ForwardsAgg["PlayerName"].iloc[i],
             fontsize=9, ha='right', va='bottom')

plt.title("Scatter Plot of Forwards")
plt.xlabel("Matches Played")
plt.ylabel("Goals")
plt.grid(True)
plt.tight_layout()
plt.savefig('Forwards plot.png')
plt.show()

# now comparison of top scorer performancs for each season

TopScorerSeasons = fd[fd["PlayerName"] == playername]

plt.figure(figsize=(10, 6))
plt.plot(TopScorerSeasons["Season"], TopScorerSeasons["Goals"], marker='o', label='Goals', linewidth=2)
plt.plot(TopScorerSeasons["Season"], TopScorerSeasons["MatchesPlayed"], marker='s', label='Matches Played', linewidth=2)
plt.plot(TopScorerSeasons["Season"], TopScorerSeasons["Goals"]/TopScorerSeasons["MatchesPlayed"]*10, marker='^', label='Goals per Game (x10)', linewidth=2)

plt.title(f"{playername}'s Performance Across Seasons")
plt.xlabel("Season")
plt.ylabel("Count")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("Best player's form.png")
plt.show()