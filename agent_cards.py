from a2a.types import AgentCard, AgentSkill, AgentInterface,AgentCapabilities

agent_card_greet = AgentCard(
    name="Greeting agent",
    description="This agent is designed to greet users and provide a friendly introduction.",
    supported_interfaces=[AgentInterface(url="http://localhost:9999/agents/greeting")],
    skills=[AgentSkill(id="hello_world", name="Greet", tags=["greeting", "introduction"])],
      capabilities=AgentCapabilities(
        streaming=True
    )
)
agent_card_calc = AgentCard(
    name="Calculator Agent",
    description="Handles math",
    supported_interfaces=[AgentInterface(url="http://localhost:9999/agents/calculator")],
    skills=[AgentSkill(id="math_solver", name="Calculate", tags=["math"])],
    capabilities=AgentCapabilities(
        streaming=True
    )
    
)