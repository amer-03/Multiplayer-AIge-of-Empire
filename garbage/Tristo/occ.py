import orca

# Create an ORCA simulator
sim = orca.Simulator()

# Add agents
for agent in agents:
    sim.addAgent(position=agent.position, radius=agent.radius, maxSpeed=agent.max_speed)

# Set goals for agents
for i, agent in enumerate(agents):
    sim.setAgentGoal(i, goal=agent.target)

# Simulation step
sim.step()
for i, agent in enumerate(agents):
    agent.position = sim.getAgentPosition(i)
