# app.py

from flask import Flask, render_template, request, jsonify
from crewai import Crew, Process
from agents import product_owner, scrum_master, developer
from tasks import backlog_creation_task, development_task
import os
from dotenv import load_dotenv
import markdown
import logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/kickoff', methods=['POST'])
def kickoff():
    data = request.json
    project_name = data.get('inputs', {}).get('project_name')

    if not project_name:
        return jsonify({'error': 'Project name is required'}), 400

    crew = Crew(
        agents=[product_owner, scrum_master, developer],
        tasks=[backlog_creation_task, development_task],
        process=Process.sequential,
        verbose=True
    )

    logging.debug(f"Starting crew kickoff for project: {project_name}")
    result = crew.kickoff(inputs={'project_name': project_name})
    logging.debug(f"Crew kickoff completed. Result type: {type(result)}")

    task_outputs = []
    for task in crew.tasks:
        logging.debug(f"Task: {task.description}")
        logging.debug(f"Task output: {task.output}")
        task_outputs.append(f"## Task: {task.description}\n\n{task.output}")

    # Prepare the markdown output
    markdown_result = f"""
# Project: {project_name}

{''.join(task_outputs)}

## Final Result:
{result}
"""

    # Convert Markdown to HTML
    html_result = markdown.markdown(markdown_result, extensions=['fenced_code', 'tables'])

    return jsonify(result=html_result)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
