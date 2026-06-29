import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Router
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
#from a2a.server.routes import create_agent_card_routes,create_jsonrpc_routes
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from agent_executor import CalculatorAgentExecutor, GreetingAgentExecuor
from agent_cards import agent_card_greet,agent_card_calc

def make_agent_app(agent_card,executor):
    request_handler = DefaultRequestHandler(
        agent_card=agent_card,
        agent_executor=executor,
        task_store=InMemoryTaskStore()
    )

    routes = []
    routes.extend(create_agent_card_routes(agent_card))
    routes.extend(create_jsonrpc_routes(request_handler,rpc_url="/v1/message:stream",enable_v0_3_compat=True))
    return Router(routes=routes)



greeting_app = make_agent_app(agent_card_greet, GreetingAgentExecuor())
calculator_app = make_agent_app(agent_card_calc, CalculatorAgentExecutor())

app= Starlette(
    routes=[
        Mount("/agents/greeting", greeting_app),
        Mount("/agents/calculator", calculator_app)
    ]
)

if __name__ == "__main__":
    
    uvicorn.run(app,host="0.0.0.0",port=9999)
   