from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import agentstack

@CrewBase
class Deepr1Crew():
    """deepr1 crew"""

    @agent
    def web_scrapper(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scrapper'],
            tools=[*agentstack.tools['firecrawl']], # add tools here or use `agentstack tools add <tool_name>
            verbose=True,
        )

    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer'],
            tools=[*agentstack.tools['firecrawl']], # add tools here or use `agentstack tools add <tool_name>
            verbose=True,
        )

    @task
    def web_scrapper_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_scrapper_task'],
        )

    @task
    def summarizer_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarizer_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Test crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            
            verbose=True,
        )