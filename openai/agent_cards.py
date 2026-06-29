from a2a.types import AgentCard,AgentCapabilities, AgentInterface, AgentSkill   

math_agent_card = AgentCard(
     name="Math_Agent",
    description="Expert in mathematics, arithmetic, algebra and calculations.",
    supported_interfaces=[
        AgentInterface(  url="http://localhost:9999/agents/math")
    ],
    skills = [
        AgentSkill(
            id = "math_solver",
            name = "Math_Solver",
            tags = ["math", "arithmetic", "algebra", "calculation"]

        )
    ],
    capabilities=AgentCapabilities(
        streaming=True
    )
)

developer_joke_agent_card = AgentCard(
    name="Developer_Joke_Agent",
    description="Provides humorous developer-related jokes and anecdotes.",
    supported_interfaces=[
        AgentInterface(url="http://localhost:9999/agents/dev_jokes")
    ],
    skills=[
        AgentSkill(
            id="dev_joke_generator",
            name="Developer_Joke_Generator",
            tags=["jokes", "developer", "humor"]
        )
    ],
    capabilities=AgentCapabilities(
        streaming=True
    )
)