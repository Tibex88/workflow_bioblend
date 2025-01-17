from bioblend.galaxy import GalaxyInstance
import json
import sys
import time
import os
import pprint
from dotenv import load_dotenv

load_dotenv()

# Retrieve variables
GALAXY_URL = os.getenv("galaxy_url")
GALAXY_API_KEY = os.getenv("galaxy_key")

gi = GalaxyInstance(url=GALAXY_URL, key=GALAXY_API_KEY)

def install_tool(tool):
    tool_shed_url = f"https://{tool['tool_shed']}"
    print(f"Installing tool: {tool['name']} from {tool_shed_url}...")

    # Install the tool
    try:
        gi.toolShed.install_repository_revision(
            tool_shed_url=tool_shed_url,
            name=tool['name'],
            owner=tool['owner'],
            changeset_revision=tool['changeset_revision'],
            install_tool_dependencies=True,
            install_repository_dependencies=True,
            install_resolver_dependencies=True,
        )
        print(f"Installation initiated for tool: {tool['name']}")
    except Exception as e:
        print(f"Error installing tool {tool['name']}: {e}")

def check_tool_status(tool_name):
    # Check installed tools
    installed_tools = gi.tools.get_tools()
    print("installed_tools: ",installed_tools["tool_shed_repository"])
    exit()
    for tool in installed_tools:
        # print("installed_tools: ",tool["name"], tool_name)
        if tool["name"] == tool_name:
            return tool["status"]
    return "Not Installed"

def install_tools_from_workflow(workflow_file):
    with open(workflow_file, 'r') as f:
        workflow = json.load(f)

    tools = [
        step["tool_shed_repository"]
        for step in workflow["steps"].values()
        if "tool_shed_repository" in step
    ]

    for tool in tools:
        print("tool name: ",tool["name"])
        install_tool(tool)
        while True:
            status = check_tool_status(tool["name"])
            if status == "Installed":
                print(f"Tool {tool['name']} installed successfully.")
                break
            elif status == "Error":
                print(f"Error installing tool {tool['name']}.")
                break
            else:
                print(f"Waiting for {tool['name']} to be installed...")
                time.sleep(10)

if __name__ == "__main__":
    workflow_file = "SnapATAC2.ga"  # Path to the workflow JSON file
    install_tools_from_workflow(workflow_file)
