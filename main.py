import streamlit as st
import math
import os
import pandas as pd

# --- Load & Save players as CSV ---
FILENAME = "players.csv"

def load_players():
    if os.path.exists(FILENAME):
        return pd.read_csv(FILENAME).to_dict(orient="records")
    return []

def save_players(players):
    df = pd.DataFrame(players)
    df.to_csv(FILENAME, index=False)

# --- Elo functions ---
def find_player(players, name):
    for player in players:
        if player["name"].lower() == name.lower():
            return player
    return None

def add_player(players, name):
    if find_player(players, name):
        st.warning(f"Player '{name}' already exists!")
    else:
        players.append({"name": name, "elo": 1000})
        st.success(f"Added player '{name}' with default Elo 1000.")

def record_match(players, winner_name, loser_name):
    winner = find_player(players, winner_name)
    loser = find_player(players, loser_name)
    if not winner or not loser:
        st.error("One or both players not found!")
        return
    if winner["elo"] != loser["elo"]:
        delta = (loser["elo"] - winner["elo"]) / (1 + 10 ** ((loser["elo"] - winner["elo"]) / 400))
        winner["elo"] -= delta
        loser["elo"] += delta
    else:
        winner["elo"] += 50
        loser["elo"] -= 50
    st.success(f"Match recorded: {winner_name} (Elo: {winner['elo']:.2f}) beat {loser_name} (Elo: {loser['elo']:.2f})")

def matchup_probability(p1, p2):
    return 1 / (1 + 10 ** ((p2["elo"] - p1["elo"]) / 400))

# --- Main Streamlit app ---
st.title("🎲 Magic Conch Elo Tracker")

players = load_players()

# Add player
st.header("➕ Add Player")
new_player = st.text_input("Player Name")
if st.button("Add Player"):
    add_player(players, new_player)
    save_players(players)

# Record match
st.header("⚔️ Record Match")
winner_name = st.text_input("Winner Name")
loser_name = st.text_input("Loser Name")
if st.button("Record Match"):
    record_match(players, winner_name, loser_name)
    save_players(players)

# Matchup probability
st.header("📊 Matchup Probability")
player1_name = st.text_input("Player 1")
player2_name = st.text_input("Player 2")
if st.button("Show Probability"):
    p1 = find_player(players, player1_name)
    p2 = find_player(players, player2_name)
    if p1 and p2:
        prob = matchup_probability(p1, p2) * 100
        st.info(f"Chance of {p1['name']} beating {p2['name']}: {prob:.2f}%")
    else:
        st.error("One or both players not found!")

# Show top 10
st.header("🏆 Top 10 Players")
top_players = sorted(players, key=lambda p: p["elo"], reverse=True)[:10]
for i, player in enumerate(top_players, start=1):
    st.write(f"{i}. {player['name']} - Elo: {player['elo']:.2f}")
