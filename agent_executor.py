import asyncio
from a2a.server.agent_execution import AgentExecutor
# ✅ THE CRITICAL FIX: Import 'Part' from the types package layout
from a2a.types import Message, Role, Part

class GreetingAgentExecuor(AgentExecutor):
    async def execute(self, context, event_queue) -> None:
    
        task_text = getattr(context, "task", "Greet User")
        reply_text = f"Hello! I am executing the task: {task_text}"
        
        message_event = Message(
            role=Role.ROLE_AGENT,
            parts=[Part(text=reply_text)]  
        )
        
      
        await event_queue.enqueue_event(message_event)
    
    async def cancel(self, context, event_queue):
        pass
    

class CalculatorAgentExecutor(AgentExecutor):
    async def execute(self, context, event_queue) -> None:
        try:
            print(f"The context is {context}")
            task_text = getattr(context, "task", "Calculation")
            client_message_text = ""

            print("==================================================")
            print(f"DEBUG: context type is {type(context)}")
            
        
            if hasattr(context, "_params") and getattr(context, "_params"):
                params = context._params
        
            if hasattr(params, "message") and params.message:
                for part in params.message.parts:
                    if hasattr(part, "text") and part.text:
                        client_message_text += part.text



            print(f"🎯 SUCCESS! The client message is: '{client_message_text}'")
            result = eval(client_message_text)
            reply_text = f"The result of the calculation '{task_text}' is: {result}"
            
        
            message_event = Message(
                role=Role.ROLE_AGENT,
                parts=[Part(text=reply_text)]
            )
            await event_queue.enqueue_event(message_event)
            
        except Exception as e:
            error_text = f"Error executing calculation: {str(e)}"
          
            error_event = Message(
                role=Role.ROLE_AGENT,
                parts=[Part(text=error_text)]
            )
            await event_queue.enqueue_event(error_event)

    async def cancel(self, context, event_queue):
        pass
