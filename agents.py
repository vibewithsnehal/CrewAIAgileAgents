# agents.py

from crewai import Agent
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API keys from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable is missing")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is missing")

# Initialize tools with API keys
search_tool = SerperDevTool(api_key=SERPER_API_KEY)

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

search_tool = SerperDevTool(api_key=SERPER_API_KEY)

product_owner = Agent(
    role='Product Owner',
    goal='Create and prioritize a comprehensive product backlog',
    verbose=True,
    memory=True,
    backstory=(
        "With a keen understanding of customer needs and market trends, "
        "you are responsible for defining the vision of the product and ensuring "
        "that the development team is working on the most valuable features."
    ),
    tools=[search_tool],
    allow_delegation=True
)

scrum_master = Agent(
    role='Scrum Master',
    goal='Facilitate the agile process and ensure smooth communication',
    verbose=True,
    memory=True,
    backstory=(
        "As a Scrum Master, you are dedicated to ensuring that the agile process "
        "is followed and that the team can work efficiently and effectively. "
        "You remove obstacles and facilitate communication within the team."
    ),
    tools=[search_tool],
    allow_delegation=True
)

developer = Agent(
    role='Developer',
    goal='Develop features from the product backlog',
    verbose=True,
    memory=True,
    backstory=(
        "You are a skilled developer with a passion for building high-quality software. "
        "Your goal is to take tasks from the product backlog and turn them into working features."
    ),
    tools=[search_tool],
    allow_delegation=False
)
