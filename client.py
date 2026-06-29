import asyncio
import httpx

from a2a.client import A2ACardResolver
from agno.client.a2a import A2AClient

from a2a.types import AgentCard

BASE_URL = "http://localhost:9999/agents/calculator"
PUBLIC_AGENT_CARD_PATH = "/agent-card.json"

async def main() -> None:
   
    async with httpx.AsyncClient() as httpx_client:
        
      
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
        )

        final_agent_card_to_use: AgentCard | None = None

        try:
            print(f"[Discovery] Fetching public agent card from: {BASE_URL}{PUBLIC_AGENT_CARD_PATH}")
            _public_card = await resolver.get_agent_card()
            print("✅ Successfully fetched and verified public agent card.")
           
            if hasattr(_public_card, "to_json"):
                print(_public_card.to_json())
            else:
                print(str(_public_card))

            final_agent_card_to_use = _public_card

        except Exception as e:
            print(f"❌ Error fetching public agent card: {e}")
            raise RuntimeError("Failed to fetch public agent card")

        client = A2AClient(
            base_url=BASE_URL
        )
        print("A2AClient initialized.")
        print("📨 Forwarding message over Agno's A2A protocol wrapper...")
        # response = await client.send_message(message="2 + 21")
        
        print("\n📥 Response Received:")
        try:
          
            async for chunk in client.stream_message(message="2 + 25"):
                
        
                if hasattr(chunk, "content") and chunk.content:
                    print(chunk.content, end="", flush=True)
                
        
                elif hasattr(chunk, "message") and chunk.message:
                
                    parts = getattr(chunk.message, "parts", [])
                    for part in parts:
                        text_val = getattr(part, "text", str(part))
                        print(text_val, end="", flush=True)
                else:
            
                    print(f"\n[Raw Event Block]: {str(chunk)}")
                    
            print("\n\n🏁 Stream channel closed successfully.")
            
        except Exception as e:
            print(f"\n❌ Streaming Session Disconnected: {e}")

if __name__ == "__main__":
    asyncio.run(main())
