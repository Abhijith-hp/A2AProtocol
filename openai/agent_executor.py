from email.mime import message
import uuid
from dotenv import load_dotenv
load_dotenv()
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from a2a.server.agent_execution import AgentExecutor
from a2a.types import Message, Role, Part

math_agent = Agent(
    model = "gpt-4o-mini",
    name = "Math_Agent",
    description = "Expert in mathematics, arithmetic, algebra and calculations.",
    instruction="Your task is to solve mathematical problems, perform calculations, and provide accurate results. You should be able to handle arithmetic, algebra, and other mathematical queries.",
)

math_runner = Runner(
    app_name = "Math_Agent",
    agent = math_agent,
    artifact_service = InMemoryArtifactService(),
    memory_service = InMemoryMemoryService(),
    session_service = InMemorySessionService()
)


developer_joke_agent = Agent(
    model="gpt-4o-mini",
    name="Developer_Joke_Agent",
    description="Programming joke expert.",
    instruction="""
You are a comedian.

Only tell jokes related to

- Programming
- Databases
- AI
- Python
- Java
- C++
- Software Engineering

Keep jokes under 3 lines.
"""
)

joke_runner = Runner(
    app_name="Developer_Joke_Agent",
    agent=developer_joke_agent,
    artifact_service=InMemoryArtifactService(),
    session_service=InMemorySessionService(),
    memory_service=InMemoryMemoryService(),
)


async def run_agent(runner,app_name,user_message,user_id,session_id):
    session_service = runner.session_service
    session = await session_service.get_session(
        app_name = app_name,
        user_id = user_id,
        session_id = session_id
    )
    if not session:
        session = await session_service.create_session(
            app_name = app_name,
            user_id = user_id,
            session_id = session_id or str(uuid.uuid4()),
            state={}
        )
    content = types.Content(
        role="user",
        parts=[types.Part(text=user_message)]
    )
    response = '' 
    async for event in runner.run_async(
        user_id = user_id,
        session_id = session.id,
        new_message = content
    ):
        if event.is_final_response():
             
            if (
                event.content
                and event.content.parts
            ):

                response = "\n".join(
                    [
                        p.text
                        for p in event.content.parts
                        if p.text
                    ]
                )

    return response


class MathAgentExecutor(AgentExecutor):
    async def execute(self,context,event_queue):
        try:
            params  =getattr(context,'_params',None)
            if params is None or params.message is None:
                error_text = "No message provided for calculation."
                error_event = Message(
                    role=Role.ROLE_AGENT,
                    parts=[Part(text=error_text)]
                )
                await event_queue.enqueue_event(error_event)
                return
            message = params.message
            user_id = message.context_id
            session_id = message.task_id
            print(f"The user_id is {user_id} and session_id is {session_id}")
            user_message = ""
            for part in message.parts:
                if hasattr(part, "text") and part.text:
                    user_message += part.text
            result = await run_agent(
                runner=math_runner,
                app_name="Math_Agent",
                user_message=user_message,
                user_id=user_id,
                session_id=session_id
            )

            await event_queue.enqueue_event(
                Message(
                    role=Role.ROLE_AGENT,
                    parts=[Part(text=result)]
                )
            )

        except Exception as e:
            error_text = f"Error executing Math Agent: {str(e)}"
            error_event = Message(
                role=Role.ROLE_AGENT,
                parts=[Part(text=error_text)]
            )
            await event_queue.enqueue_event(error_event)

            
    async def cancel(self, context, event_queue):
        pass
                




class JokeExecutor(AgentExecutor):
    async def execute(self,context,event_queue):
        try:
            params  =getattr(context,'_params',None)
            print("The params are ",params)
            user_message = ""
            if params is None or params.message is None:
                error_text = "No message provided for joke."
                error_event = Message(
                    role=Role.ROLE_AGENT,
                    parts=[Part(text=error_text)]
                )
                await event_queue.enqueue_event(error_event)
                return
            message = params.message
            session_id = message.context_id

            user_id = message.metadata.fields["userId"].string_value
            print(f"The user_id is {user_id} and session_id is {session_id}")
            for part in message.parts:
                if hasattr(part, "text") and part.text:
                    user_message += part.text
            result = await run_agent(
                runner=joke_runner,
                app_name="Developer_Joke_Agent",
                user_message=user_message,
                user_id=user_id,
                session_id=session_id
            )

            await event_queue.enqueue_event(
                Message(
                    role=Role.ROLE_AGENT,
                    parts=[Part(text=result)]
                )
            )

        except Exception as e:
            error_text = f"Error executing Joke Agent: {str(e)}"
            error_event = Message(
                role=Role.ROLE_AGENT,
                parts=[Part(text=error_text)]
            )
            await event_queue.enqueue_event(error_event)

            
    async def cancel(self, context, event_queue):
        pass
                

           



