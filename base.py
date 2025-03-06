# magicConch.py
# i got tired and didnt wanna make it myself

import os
import math


# Define a simple Player class
class Player:
    def __init__(self, name, elo=1000):
        self.name = name
        self.elo = elo


# Load players from a text file (each line: name,elo)
def load_players(filename):
    players = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    name = parts[0].strip()
                    try:
                        elo = float(parts[1].strip())
                    except ValueError:
                        elo = 1000
                    players.append(Player(name, elo))
    return players


# Save players to a text file
def save_players(players, filename):
    with open(filename, "w") as f:
        for player in players:
            f.write(f"{player.name},{player.elo}\n")


# Add a new player with default Elo
def add_player(players):
    name = input("Enter player name: ").strip()
    # Check if player already exists
    if any(p.name.lower() == name.lower() for p in players):
        print("Player already exists!")
        return
    players.append(Player(name))
    print(f"Added player {name} with default Elo of 1000.")


# Helper function to find a player by name (case-insensitive)
def find_player(players, name):
    for player in players:
        if player.name.lower() == name.lower():
            return player
    return None


# Record a match result between two players
def record_match(players):
    winner_name = input("Enter the winner's name: ").strip()
    loser_name = input("Enter the loser's name: ").strip()
    winner = find_player(players, winner_name)
    loser = find_player(players, loser_name)
    if winner is None or loser is None:
        print("One or both players not found!")
        return

    if (winner.elo != loser.elo):
        # Update ratings using the provided formula.
        # Note: As written, the formula is:
        #   R_w' = R_w + (R_l - R_w) / (1 + 10^((R_l - R_w)/400))
        # and we subtract the same delta from the loser so that total Elo is conserved.
        delta = (loser.elo - winner.elo) / (1 + 10 ** ((loser.elo - winner.elo) / 400))
        winner.elo -= delta
        loser.elo += delta
    else:
        winner.elo += 50
        loser.elo -= 50



    print(f"Match recorded:")
    print(f"  Winner {winner.name} new Elo: {winner.elo:.2f}")
    print(f"  Loser {loser.name} new Elo: {loser.elo:.2f}")


# Display the probability of a matchup
def display_probability(players):
    name1 = input("Enter first player's name: ").strip()
    name2 = input("Enter second player's name: ").strip()
    player1 = find_player(players, name1)
    player2 = find_player(players, name2)
    if player1 is None or player2 is None:
        print("One or both players not found!")
        return

    # Compute probability of player1 beating player2 using Elo expected score:
    probability = 1 / (1 + 10 ** ((player2.elo - player1.elo) / 400))
    print(f"Probability of {player1.name} beating {player2.name}: {probability * 100:.2f}%")


# Display top 10 players sorted by Elo descending
def display_top_players(players):
    sorted_players = sorted(players, key=lambda p: p.elo, reverse=True)
    print("\n--- Top 10 Players ---")
    for i, player in enumerate(sorted_players[:10], start=1):
        print(f"{i}. {player.name} - Elo: {player.elo:.2f}")


# Main menu loop
def main():
    filename = "players.txt"
    players = load_players(filename)

    while True:
        print("\nMenu:")
        print("1. Add new player")
        print("2. Record match result")
        print("3. Display matchup probability")
        print("4. Show top 10 players")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_player(players)
            save_players(players, filename)
        elif choice == "2":
            record_match(players)
            save_players(players, filename)
        elif choice == "3":
            display_probability(players)
        elif choice == "4":
            display_top_players(players)
        elif choice == "5":
            save_players(players, filename)
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
