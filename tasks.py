# tasks.py

from crewai import Task
from agents import product_owner, developer
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

backlog_creation_task = Task(
    description=(
        "Create a prioritized product backlog and user stories for {project_name}. "
        "Ensure that each user story has acceptance criteria and is estimated."
        "Make sure each story has a different persona"
    ),
    expected_output='A comprehensive and prioritized product backlog with detailed user stories.',
    output_file='product-backlog.md',
    tools=[search_tool],
    agent=product_owner,
)

development_task = Task(
    description=(
        "Pick tasks from the product backlog and develop the features. "
        "Ensure to write unit tests and document the code."
    ),
    expected_output='Working features with unit tests and documentation.',
    agent=developer,
    async_execution=False,
    output_file='dev-tasks-output.md'
)
