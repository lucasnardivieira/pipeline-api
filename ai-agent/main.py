from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.postgres import PostgresTools

from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize PostgresTools with connection details
postgres_tools = PostgresTools(
    host="dpg-d0kdhs7fte5s738js9ag-a.ohio-postgres.render.com",
    port=5432,
    db_name="dbname_kgba",
    user="dbname_kgba_user",
    password="JOwYbL7u66qLZ6SEErd0yp2PhSHppSfS",
    table_schema="public",
)

# Initialize the agent with an LLM via Groq and DuckDuckGoTools
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    description="Você é um assistente de IA que pode fazer consultas em um banco de dados Postgres e á um analista sobre bitcoin.",
    tools=[postgres_tools],      
    show_tool_calls=True,           # Shows tool calls in the response, set to False to hide
    markdown=True                   # Format responses in markdown
)

# Prompt the agent to fetch a breaking news story from New York
agent.print_response("Faça uma query para pegar todas as cotações de bitcoin na tabela bitcoin_data e faça uma análise simples")