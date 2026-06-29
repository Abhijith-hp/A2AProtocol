import uvicorn
import inspect
from starlette.routing import Mount, Router
from starlette.applications import Starlette
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
#from a2a.server.routes import create_agent_card_routes,create_jsonrpc_routes
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from agent_executor import math_runner, joke_runner
from agent_cards import math_agent_card, developer_joke_agent_card
from agent_executor import MathAgentExecutor,JokeExecutor
def make_agent_app(agent_card, executor):
    request_handler = DefaultRequestHandler(
        agent_card=agent_card,
        agent_executor=executor,
        task_store=InMemoryTaskStore()
    )

    routes = []
    routes.extend(create_agent_card_routes(agent_card))
    routes.extend(create_jsonrpc_routes(request_handler, rpc_url="/v1/message:stream", enable_v0_3_compat=True))
    return Router(routes=routes)

math_agent_app = make_agent_app(math_agent_card, MathAgentExecutor())
joke_agent_app = make_agent_app(developer_joke_agent_card, JokeExecutor())

app = Starlette(
    routes=[
        Mount("/agents/math", math_agent_app),
        Mount("/agents/dev_jokes", joke_agent_app)
    ]
)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
