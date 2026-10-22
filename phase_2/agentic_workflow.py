# agentic_workflow.py

import sys
import os
import numpy as np
from dotenv import load_dotenv

# Add phase_1 and current directory to sys.path so Python can find workflow_agents
current_dir = os.path.dirname(os.path.abspath(__file__))
phase_1_dir = os.path.abspath(os.path.join(current_dir, "..", "phase_1"))
sys.path.insert(0, phase_1_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, "/workspace/cd14525-agentic-workflows-classroom/project/starter/phase_1")

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from workflow_agents.base_agents import (
    ActionPlanningAgent,
    KnowledgeAugmentedPromptAgent,
    EvaluationAgent,
    RoutingAgent
)

# Load environment variables
load_dotenv()

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
spec_file_path = os.path.join(os.path.dirname(__file__), "Product-Spec-Email-Router.txt")
if not os.path.exists(spec_file_path):
    spec_file_path = "Product-Spec-Email-Router.txt"

with open(spec_file_path, "r", encoding="utf-8") as f:
    product_spec = f.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(
    openai_api_key=openai_api_key,
    knowledge=knowledge_action_planning
)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    + product_spec
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager,
    knowledge=knowledge_product_manager
)

# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent.
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
evaluation_criteria_product_manager = (
    "The answer should be user stories that follow the structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager_eval,
    evaluation_criteria=evaluation_criteria_product_manager,
    worker_agent=product_manager_knowledge_agent,
    max_interactions=3
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = (
    "Features of a product are defined by organizing similar user stories into cohesive groups based on the product specification.\n"
    "Each feature MUST be formatted with these exact four labels:\n"
    "Feature Name: [clear, concise title]\n"
    "Description: [brief explanation of what the feature does and its purpose]\n"
    "Key Functionality: [specific capabilities or actions provided]\n"
    "User Benefit: [how this feature creates value for the user]\n\n"
    "Product Specification:\n"
    + product_spec
)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager,
    knowledge=knowledge_program_manager
)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent
evaluation_criteria_program_manager = (
    "The answer must define product features where every single feature strictly uses these exact labels:\n"
    "Feature Name:\n"
    "Description:\n"
    "Key Functionality:\n"
    "User Benefit:\n"
    "If any feature is missing any of these four exact labels, reject it."
)
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria=evaluation_criteria_program_manager,
    worker_agent=program_manager_knowledge_agent,
    max_interactions=3
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = (
    "Development tasks are defined by identifying what needs to be built to implement each user story for the product described below.\n"
    "Each task MUST strictly use this exact structure with these exact labels:\n"
    "Task ID: [e.g. TASK-001]\n"
    "Task Title: [brief description]\n"
    "Related User Story: [reference to parent user story]\n"
    "Description: [detailed explanation of technical work]\n"
    "Acceptance Criteria: [specific requirements for completion]\n"
    "Estimated Effort: [time or complexity]\n"
    "Dependencies: [any predecessor tasks or None]\n\n"
    "Product Specification:\n"
    + product_spec
)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer
)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent
evaluation_criteria_dev_engineer = (
    "The answer should be tasks following this exact structure with these exact labels:\n"
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first\n"
    "Every task must start with the exact label 'Task ID:'. If any task uses 'Task 1' without 'Task ID:', reject it."
)
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria=evaluation_criteria_dev_engineer,
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=3
)

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent
def product_manager_support_function(query):
    eval_result = product_manager_evaluation_agent.evaluate(query)
    return eval_result["final_response"]

def program_manager_support_function(query):
    eval_result = program_manager_evaluation_agent.evaluate(query)
    return eval_result["final_response"]

def development_engineer_support_function(query):
    eval_result = development_engineer_evaluation_agent.evaluate(query)
    return eval_result["final_response"]

# Routing Agent
# TODO: 10 - Instantiate a routing_agent.
agents = [
    {
        "name": "Product Manager",
        "description": "Define and write user stories for the product specification",
        "func": product_manager_support_function
    },
    {
        "name": "Program Manager",
        "description": "Define product features by grouping related user stories",
        "func": program_manager_support_function
    },
    {
        "name": "Development Engineer",
        "description": "Define development tasks and engineering work for the product",
        "func": development_engineer_support_function
    }
]

routing_agent = RoutingAgent(openai_api_key=openai_api_key, agents=agents)

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# Phrased to request the full development plan covering user stories, features, and tasks
workflow_prompt = (
    "Create a comprehensive development plan for this product. "
    "First define the user stories, then define the product features by grouping the stories, "
    "and finally define the engineering development tasks required to build the product."
)
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
extracted_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
print(f"Extracted Steps:\n{extracted_steps}")

completed_steps = []
context_so_far = ""

for i, step in enumerate(extracted_steps):
    print(f"\n==========================================")
    print(f"Executing Step {i+1}: {step}")
    print(f"==========================================")
    
    # 1. Route based on the pure step text so embeddings match the correct role
    input_emb = routing_agent.get_embedding(step)
    best_agent = None
    best_score = -1

    for agent in routing_agent.agents:
        agent_emb = routing_agent.get_embedding(agent["description"])
        similarity = np.dot(input_emb, agent_emb) / (np.linalg.norm(input_emb) * np.linalg.norm(agent_emb))
        print(f"Agent '{agent['name']}' similarity: {similarity:.3f}")
        if similarity > best_score:
            best_score = similarity
            best_agent = agent

    print(f"[Router] Best agent: {best_agent['name']} (score={best_score:.3f})")

    # 2. Pass the step and accumulated context to the selected agent's function
    step_query = step
    if context_so_far:
        step_query = f"{step}\n\nContext and outputs from previous steps:\n{context_so_far}"

    step_result = best_agent["func"](step_query)
    completed_steps.append({"step": step, "result": step_result})
    context_so_far += f"\n\n--- Output from Step {i+1} ({step}) ---\n{step_result}"
    
    print(f"\nCompleted Step {i+1} Result:\n{step_result}")

print("\n\n**************************************************")
print("*** FINAL WORKFLOW OUTPUT ***")
print("**************************************************")
if completed_steps:
    for item in completed_steps:
        print(f"\n### {item['step']} ###\n{item['result']}")
else:
    print("No steps were executed.")