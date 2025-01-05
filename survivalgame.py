import streamlit as st
import random

# Function to display stats
def display_stats(player):
    st.sidebar.subheader("Your Stats:")
    st.sidebar.write(f"Health: {player['health']}")
    st.sidebar.write(f"Attack: {player['attack']}")
    st.sidebar.write(f"Defense: {player['defense']}")
    st.sidebar.write(f"Experience: {player['experience']}")

# Fight logic
def fight(player, enemy):
    st.write(f"A wild **{enemy['name']}** appears!")
    st.write(f"Enemy Stats - Health: {enemy['health']}, Attack: {enemy['attack']}")

    while player['health'] > 0 and enemy['health'] > 0:
        # Player attacks first
        damage_to_enemy = max(player['attack'] - enemy['attack'] // 2, 1)
        enemy['health'] -= damage_to_enemy
        st.write(f"You attack the {enemy['name']} for **{damage_to_enemy}** damage. Enemy health: {enemy['health']}")

        if enemy['health'] <= 0:
            st.write(f"You defeated the **{enemy['name']}**!")
            player['experience'] += enemy['experience']
            player['attack'] += 1
            player['health'] += 5  # Small health boost
            return True

        # Enemy attacks back
        damage_to_player = max(enemy['attack'] - player['defense'], 1)
        player['health'] -= damage_to_player
        st.write(f"The {enemy['name']} attacks you for **{damage_to_player}** damage. Your health: {player['health']}")

    if player['health'] <= 0:
        st.error("You have been defeated! Game Over.")
        return False

    return True

# Streamlit app
def main():
    st.title("Survival Game by Sol")
    st.write("Survive as long as you can by defeating enemies and growing stronger!")
    st.write("Press **Start Game** to begin.")

    # Initial player stats
    player = {
        'health': 1000,
        'attack': 15,
        'defense': 5,
        'experience': 0
    }

    enemies = [
        {'name': 'Goblin', 'health': 30, 'attack': 5, 'experience': 10},
        {'name': 'Orc', 'health': 50, 'attack': 8, 'experience': 20},
        {'name': 'Troll', 'health': 70, 'attack': 12, 'experience': 30},
        {'name': 'Dragon', 'health': 100, 'attack': 15, 'experience': 50},
        {'name' : 'ninja', 'health': 1000, 'attack' : 10, 'experience': 100}
    ]

    # Game state
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "player" not in st.session_state:
        st.session_state.player = player

    if st.button("Start Game"):
        st.session_state.game_started = True
        st.session_state.player = player  # Reset player stats

    if st.session_state.game_started:
        display_stats(st.session_state.player)

        # Generate a random enemy
        enemy = random.choice(enemies)

        # Fight button
        if st.button("Fight Enemy"):
            survived = fight(st.session_state.player, enemy)
            if not survived:
                st.session_state.game_started = False

        # Reset button
        if not st.session_state.game_started:
            if st.button("Restart Game"):
                st.session_state.game_started = True
                st.session_state.player = player  # Reset player stats
                st.experimental_rerun()

if __name__ == "__main__":
    main()
