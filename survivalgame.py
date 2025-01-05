import streamlit as st
import random
import time

# Function to calculate random damage within ±50% range
def calculate_random_damage(base_attack):
    min_damage = int(base_attack * 0.5)  # 50% below base attack
    max_damage = int(base_attack * 1.5)  # 50% above base attack
    return random.randint(min_damage, max_damage)

# Function to display stats for player and enemy
def display_battlefield_stats(player, enemy, player_health_change, enemy_health_change):
    stats_placeholder = st.empty()
    with stats_placeholder.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Your Stats")
            st.write(f"**Health:** {player['health']} {player_health_change}")
            st.write(f"**Attack:** {player['attack']} (±50%)")
            st.write(f"**Defense:** {player['defense']}")
            st.write(f"**Experience:** {player['experience']}")
        with col2:
            st.markdown("### Enemy Stats")
            st.write(f"**Name:** {enemy['name']}")
            st.write(f"**Health:** {enemy['health']} {enemy_health_change}")
            st.write(f"**Attack:** {enemy['attack']} (±50%)")
    return stats_placeholder

# Function to format health change
def format_health_change(change):
    if change > 0:
        return f"*(+{change})*"  # Green for healing
    elif change < 0:
        return f"*({change})*"  # Red for damage
    else:
        return ""

# Fight logic with rewards included in logs
def fight(player, enemy, use_skill):
    st.write(f"A wild **{enemy['name']}** appears!")
    battle_log_placeholder = st.empty()  # Placeholder for battle logs
    clash_placeholder = st.empty()  # Placeholder for Light Saber Clash
    logs = st.session_state.get("logs", [])  # Store the last 5 logs

    player_health_change = ""
    enemy_health_change = ""

    stats_placeholder = display_battlefield_stats(player, enemy, player_health_change, enemy_health_change)

    # Apply Light Saber Clash if selected
    if use_skill and player['experience'] >= 50:
        player['experience'] -= 50
        extra_damage = random.randint(50, 100)
        enemy['health'] -= extra_damage
        clash_placeholder.markdown(
            f"""
            <div style="text-align:center; font-size:20px; color:gold; font-weight:bold;">
                ⚡ **Light Saber Clash Activated!** ⚡<br>
                <span style="font-size:24px; color:red;">Dealt {extra_damage} extra damage!</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        enemy_health_change = format_health_change(-extra_damage)
        with stats_placeholder.container():
            display_battlefield_stats(player, enemy, player_health_change, enemy_health_change)

    # Animated fight sequence
    while player['health'] > 0 and enemy['health'] > 0:
        # Player attacks with random damage
        player_attack = calculate_random_damage(player['attack'])
        damage_to_enemy = max(player_attack - enemy['attack'] // 2, 1)
        is_critical = player_attack > player['attack'] * 1.3
        enemy['health'] -= damage_to_enemy
        enemy_health_change = format_health_change(-damage_to_enemy)

        # Log attack with critical hit check
        if is_critical:
            logs.append(f"🔥 **CRITICAL HIT!** You attack the {enemy['name']} for {damage_to_enemy} damage! 🔥")
        else:
            logs.append(f"You attack the {enemy['name']} for {damage_to_enemy} damage.")

        if len(logs) > 5:  # Limit logs to 5 lines
            logs.pop(0)
        st.session_state["logs"] = logs  # Save updated logs to session state
        battle_log_placeholder.markdown("<br>".join(logs), unsafe_allow_html=True)
        with stats_placeholder.container():
            display_battlefield_stats(player, enemy, player_health_change, enemy_health_change)
        time.sleep(0.3)

        if enemy['health'] <= 0:
            # Calculate rewards
            experience_gained = enemy['experience']
            attack_gained = 1
            health_gained = 5

            # Apply rewards
            player['experience'] += experience_gained
            player['attack'] += attack_gained
            player['health'] += health_gained

            # Log rewards and victory
            logs.append(f"🎉 **You defeated the {enemy['name']}!** 🎉")
            logs.append(f"**Rewards:** Experience +{experience_gained}, Attack +{attack_gained}, Health +{health_gained}")

            if len(logs) > 5:  # Ensure logs are limited to 5 lines
                logs = logs[-5:]
            st.session_state["logs"] = logs
            battle_log_placeholder.markdown("<br>".join(logs), unsafe_allow_html=True)
            return True

        # Enemy attacks with random damage
        enemy_attack = calculate_random_damage(enemy['attack'])
        damage_to_player = max(enemy_attack - player['defense'], 1)
        is_critical = enemy_attack > enemy['attack'] * 1.3
        player['health'] -= damage_to_player
        player_health_change = format_health_change(-damage_to_player)

        # Log enemy attack with critical hit check
        if is_critical:
            logs.append(f"🔥 **CRITICAL HIT!** {enemy['name']} attacks you for {damage_to_player} damage! 🔥")
        else:
            logs.append(f"The {enemy['name']} attacks you for {damage_to_player} damage.")

        if len(logs) > 5:  # Limit logs to 5 lines
            logs.pop(0)
        st.session_state["logs"] = logs  # Save updated logs to session state
        battle_log_placeholder.markdown("<br>".join(logs), unsafe_allow_html=True)
        with stats_placeholder.container():
            display_battlefield_stats(player, enemy, player_health_change, enemy_health_change)
        time.sleep(0.3)

    if player['health'] <= 0:
        st.error("❌ **You have been defeated! Game Over.** ❌")
        return False

    return True

# Streamlit app
def main():
    st.title("Survival Game by Sol")
    st.write("Survive as long as you can by defeating enemies and growing stronger!")
    st.write("Press **Start Game** to begin.")

    # Initial player stats
    player = {
        'health': 1500,
        'attack': 15,
        'defense': 5,
        'experience': 0
    }

    enemies = [
        {'name': 'Goblin', 'health': 30, 'attack': 5, 'experience': 10},
        {'name': 'Orc', 'health': 50, 'attack': 8, 'experience': 20},
        {'name': 'Troll', 'health': 70, 'attack': 12, 'experience': 30},
        {'name': 'Dragon', 'health': 100, 'attack': 15, 'experience': 50},
        {'name': 'Ninja', 'health': 500, 'attack': 10, 'experience': 100},
        {'name': 'Darth Vader', 'health': 500, 'attack': 15, 'experience': 200},
        {'name': 'crab', 'health': 10, 'attack': 5, 'experience': 15},
        {'name': 'Legendary Plant', 'health': 300, 'attack': 15, 'experience': 100}
    ]

    # Game state
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "player" not in st.session_state:
        st.session_state.player = player
    if "logs" not in st.session_state:
        st.session_state.logs = []  # Initialize logs in session state

    if st.button("Start Game", key="start_game"):
        st.session_state.game_started = True
        st.session_state.player = player  # Reset player stats
        st.session_state.logs = []  # Reset logs

    if st.session_state.game_started:
        # Generate a random enemy
        enemy = random.choice(enemies)

        # Ask if player wants to use Light Saber Clash
        use_skill = False
        if st.session_state.player['experience'] >= 50:
            use_skill_input = st.radio(
                "Do you want to use **Light Saber Clash** for an extra attack?",
                options=["No", "Yes"],
                index=0,
                key="light_saber_clash",
            )
            use_skill = use_skill_input == "Yes"

        # Fight button
        if st.button("Fight Enemy", key="fight_enemy"):
            survived = fight(st.session_state.player, enemy, use_skill)
            if not survived:
                st.session_state.game_started = False

        # Reset button
        if not st.session_state.game_started:
            if st.button("Restart Game", key="restart_game"):
                st.session_state.game_started = True
                st.session_state.player = player  # Reset player stats
                st.session_state.logs = []  # Reset logs
                st.experimental_rerun()

if __name__ == "__main__":
    main()
