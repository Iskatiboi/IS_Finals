"""
rl_agent.py - REINFORCEMENT LEARNING: learn when to restock Pancit Canton.

The agent tries actions, receives rewards, and slowly learns which action
is best for each stock level. Q-learning is written from scratch here.
"""

import numpy as np
import pandas as pd

# ----- Store rules (the environment) -----
MAX_STOCK = 20           # the shelf holds at most 20 units
ORDER_SIZES = [0, 5, 10] # action 0, 1, 2 = order 0, 5, or 10 units
DEMAND_MEAN = 4          # customers want 4 units per day on average
EPISODE_DAYS = 30        # one episode is one 30-day month
START_STOCK = 10         # stock on day 1 of a simulation

PROFIT_PER_UNIT = 5.0    # earned for each unit sold
STORAGE_COST = 0.5       # paid for each unit left at the end of the day
LOST_CUSTOMER_COST = 3.0 # penalty for each unit we could not sell
DELIVERY_FEE = 10.0      # paid on any day we place an order


def step(stock, action, demand):
    """Simulate one day. Returns what happened and the reward."""
    # The order arrives first. Anything above the shelf limit does not fit.
    order = ORDER_SIZES[action]
    stock_after_delivery = min(stock + order, MAX_STOCK)

    # Customers buy what they want, as long as we still have stock.
    sold = min(stock_after_delivery, demand)
    leftover = stock_after_delivery - sold
    unmet = demand - sold

    # Reward = profit - storage cost - lost customers - delivery fee.
    reward = sold * PROFIT_PER_UNIT - leftover * STORAGE_COST - unmet * LOST_CUSTOMER_COST
    if order > 0:
        reward -= DELIVERY_FEE

    return leftover, sold, unmet, reward


def train(episodes=2000, alpha=0.1, gamma=0.9, seed=42):
    """Run Q-learning. Returns the Q-table and total reward per episode."""
    rng = np.random.default_rng(seed)

    # One row per stock level (0 to 20) and one column per action.
    # Each cell estimates how good that action is at that stock level.
    Q = np.zeros((MAX_STOCK + 1, len(ORDER_SIZES)))
    episode_rewards = []

    for episode in range(episodes):
        # Epsilon goes down in a straight line from 1.0 to 0.05.
        progress = episode / max(episodes - 1, 1)
        epsilon = 1.0 - progress * (1.0 - 0.05)

        # Start at a random stock level so every state gets practice.
        stock = int(rng.integers(0, MAX_STOCK + 1))
        total_reward = 0.0

        for day in range(EPISODE_DAYS):
            # Epsilon-greedy: sometimes explore, otherwise use the best action.
            if rng.random() < epsilon:
                action = int(rng.integers(len(ORDER_SIZES)))
            else:
                action = int(np.argmax(Q[stock]))

            # Play one day in the store.
            demand = int(rng.poisson(DEMAND_MEAN))
            next_stock, _, _, reward = step(stock, action, demand)

            # The Q-learning update: move the old estimate toward
            # (today's reward + discounted value of the best next action).
            best_next = np.max(Q[next_stock])
            Q[stock, action] += alpha * (reward + gamma * best_next - Q[stock, action])

            stock = next_stock
            total_reward += reward

        episode_rewards.append(total_reward)

    return Q, np.array(episode_rewards)


def get_policy(Q):
    """Turn the Q-table into a simple table: stock level -> best action."""
    best_actions = np.argmax(Q, axis=1)
    return pd.DataFrame({
        "stock_level": range(MAX_STOCK + 1),
        "action": best_actions,
        "order_units": [ORDER_SIZES[a] for a in best_actions],
    })


def choose_action(policy, stock, rng):
    """Pick today's action for a learned table, "random", or "always_10"."""
    if isinstance(policy, str):
        if policy == "random":
            return int(rng.integers(len(ORDER_SIZES)))
        if policy == "always_10":
            return ORDER_SIZES.index(10)
        raise ValueError("Unknown policy: " + policy)

    # A learned policy: look up the action in the table.
    return int(policy["action"].iloc[stock])


def simulate(policy, days=30, seed=0):
    """Run one month with a policy. Returns the daily table and total profit."""
    rng = np.random.default_rng(seed)

    # Decide all demand first, so every policy faces the same customers.
    demands = rng.poisson(DEMAND_MEAN, days)

    stock = START_STOCK
    rows = []

    for day in range(days):
        action = choose_action(policy, stock, rng)
        demand = int(demands[day])
        leftover, sold, unmet, reward = step(stock, action, demand)

        rows.append({
            "day": day + 1,
            "order": ORDER_SIZES[action],
            "stock": leftover + sold,  # stock on the shelf after delivery
            "demand": demand,
            "sales": sold,
            "unmet": unmet,
            "leftover": leftover,
            "profit": reward,
        })
        stock = leftover

    daily = pd.DataFrame(rows)
    return daily, float(daily["profit"].sum())


def compare_policies(policy, runs=200, days=30):
    """Average profit of each strategy over many simulated months."""
    strategies = {
        "Learned Agent": policy,
        "Random": "random",
        "Always Order 10": "always_10",
    }

    rows = []
    for name, strategy in strategies.items():
        profits = [simulate(strategy, days, seed)[1] for seed in range(runs)]
        rows.append({"strategy": name, "average_profit": float(np.mean(profits))})

    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Quick self-test: python rl_agent.py
    q_table, rewards = train(2000)
    learned = get_policy(q_table)
    print(learned.to_string(index=False))
    print("First 100 episodes, average reward:", round(rewards[:100].mean(), 1))
    print("Last 100 episodes, average reward:", round(rewards[-100:].mean(), 1))
    print(compare_policies(learned).round(2).to_string(index=False))
