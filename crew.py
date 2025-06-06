# crew_yaml_runner.py
import yaml
import re
from crewai import Agent, Task, Crew
from llm import get_gemini_llm
from tools import tool_map
import os
from datetime import datetime

# Load LLM and tools
llm = get_gemini_llm()

def extract_url(user_input):
    match = re.search(r'https?://[^\s]+', user_input)
    return match.group() if match else "https://www.example.com"

def save_output_to_file(output_data, prefix="seo_report"):
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Format timestamp for filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output/{prefix}_{timestamp}.md"

    # Write the result to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_data if isinstance(output_data, str) else str(output_data))

    print(f"\n✅ Output saved to: {filename}")

def load_agents_from_yaml(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    agents = {}
    for agent_def in data['agents']:
        tools = [tool_map[t] for t in agent_def.get('tools', [])]
        agents[agent_def['id']] = Agent(
            role=agent_def['role'],
            goal=agent_def['goal'],
            backstory=agent_def['backstory'],
            verbose=agent_def.get('verbose', False),
            tools=tools,
            llm=llm
        )
    return agents

def load_tasks_from_yaml(file_path, agents, input_data):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    tasks = {}
    for task_def in data['tasks']:
        description = task_def['description_template'].format(**input_data) if task_def.get('dynamic_input') else task_def['description']
        agent = agents[task_def['agent_id']]
        tasks[task_def['id']] = Task(
            description=description,
            agent=agent,
            expected_output=task_def['expected_output']
        )
    return tasks


def run_metadata_analysis(url_input):
    print(f"\n=== Starting Metadata Analysis for: {url_input} ===")
    url = extract_url(url_input)
    print("URL: ", url)
    # agents = load_agents_from_yaml("agents.yaml")
    tasks = load_tasks_from_yaml("tasks.yaml", agents, {"url": url, "user_input": url_input})

    crew = Crew(
        agents=[agents["meta_researcher"], agents["meta_writer"]],
        tasks=[tasks["metadata_analysis"], tasks["metadata_report"]],
        verbose=False,
        process="sequential"
    )
    result = crew.kickoff()
    # print("\n=== Metadata Analysis Report ===")
    # print(result)
    save_output_to_file(result, prefix="metadata_analysis")
    return result

def run_content_analysis(url_input):
    print(f"\n=== Starting Content Analysis for: {url_input} ===")
    url = extract_url(url_input)
    # agents = load_agents_from_yaml("agents.yaml")
    tasks = load_tasks_from_yaml("tasks.yaml", agents, {"url": url, "user_input": url_input})

    crew = Crew(
        agents=[agents["content_researcher"], agents["seo_writer"]],
        tasks=[tasks["content_analysis"], tasks["seo_report"]],
        verbose=False,
        process="sequential"
    )
    result = crew.kickoff()
    # print("\n=== Content Analysis Report with Recommendations ===")
    # print(result)
    save_output_to_file(result, prefix="content_analysis")
    return result

def run_both_analyses(url_input):
    print(f"\n=== Starting Complete SEO Analysis for: {url_input} ===")
    print("\n🔍 STEP 1: Metadata Analysis")
    metadata_result = run_metadata_analysis(url_input)
    print("\n" + "="*60)
    print("\n🔍 STEP 2: Content Analysis")
    content_result = run_content_analysis(url_input)

    return {
        "metadata_analysis": metadata_result,
        "content_analysis": content_result
    }

def run_plagiarism_analysis(input_text):
    # agents = load_agents_from_yaml("agents.yaml")
    tasks = load_tasks_from_yaml("tasks.yaml", agents, {"user_input": input_text,"url":""})

    # crew = Crew(agents=list(agents.values()), tasks=list(tasks.values()), verbose=False)

    # Select only the required agent and task
    selected_agents = [agents["plagiarism_checker"]]
    selected_tasks = [tasks["plagiarism_checker"]]
    
    crew = Crew(agents=selected_agents, tasks=selected_tasks, verbose=False)

    result = crew.kickoff()
    save_output_to_file(result, prefix="plagiarism_report")
    return result

def run_title_description(url_input):
    urls = extract_url(url_input)
    # print("url:", urls)
    # agents = load_agents_from_yaml("agents.yaml")
    tasks = load_tasks_from_yaml("tasks.yaml", agents, {"user_input": url_input, "url":urls})
    # crew = Crew(agents=agents, tasks=tasks, verbose=True)
    # crew = Crew(agents=list(agents.values()), tasks=list(tasks.values()), verbose=True)

    # Select only the required agent and task
    selected_agents = [agents["title_meta_checker"], agents["meta_writer"]]
    selected_tasks = [tasks["title_meta_checker"], tasks["report_write"]]
    
    crew = Crew(agents=selected_agents, tasks=selected_tasks, verbose=False, process="sequential")
    result = crew.kickoff()
    save_output_to_file(result, prefix="title_description")
    return result

agents = load_agents_from_yaml("agents.yaml")

def run_crew(custom_input):
    decision_prompt = f"""
You are deciding which analysis to perform based on the input.

Input: {custom_input}

Instructions:
- Respond with only one of the following options: ["plagiarism", "title_description", "metadata", "content", "both"]
- If the input is a URL, choose from: ["title_description", "metadata", "content", "both"]
- If the input is plain text (not a URL), choose only: "plagiarism"
- Respond with only one word, no explanations.
"""

    decision = llm.client.generate_content(decision_prompt).text.strip().lower()
    print("Decision:", decision)

    if decision == "title_description":
        return run_title_description(custom_input["text"])
    elif decision == "plagiarism":
        return run_plagiarism_analysis(custom_input["text"])
    elif decision == "metadata":
        return run_metadata_analysis(custom_input["text"])
    elif decision == "content":
        return run_content_analysis(custom_input["text"])
    elif decision == "both":
        return run_both_analyses(custom_input["text"])
    else:
        raise ValueError(f"Invalid LLM decision: {decision}")
