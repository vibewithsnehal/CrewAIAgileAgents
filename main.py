# app.py

from flask import Flask, render_template, request, jsonify
from crewai import Crew, Process
from agents import product_owner, scrum_master, developer
from tasks import backlog_creation_task, development_task
import os
from dotenv import load_dotenv
import markdown

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


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
        process=Process.sequential
    )

    result = crew.kickoff(inputs={'project_name': project_name})

    # Convert the result to Markdown
    markdown_result = "```markdown\n" + result + "\n```"
    # Convert Markdown to HTML
    html_result = markdown.markdown(markdown_result, extensions=['fenced_code', 'tables'])

    return jsonify(result=html_result)


if __name__ == '__main__':
    app.run(debug=True)
