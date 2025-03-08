from crewai.flow.flow import Flow, listen, start, and_
from dotenv import load_dotenv
from litellm import completion
from flowagent.crew import Flowagent
from pydantic import BaseModel
import os
import asyncio
class News(BaseModel):
    news:str=""
class NewsFlow(Flow[News]):
    model = "gpt-4o-mini"

    @start()
    def generate_news_topic(self):
        print("Starting flow")
        # Each flow state automatically gets a unique ID
        print(f"Flow State ID: {self.state['id']}")

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Generate a topic with in the ai world which is currently trending , that should be in 1-4 words.",
                },
            ],
        )

        newstopic = response["choices"][0]["message"]["content"]
        # Store the city in our state
        self.state["city"] = newstopic
        print(f"Newstopic: {newstopic}")

        return newstopic

    @listen(generate_news_topic)
    def generate_news(self, newstopic):
        print("Generating news with crew")
        inputs={
            'topic':newstopic
        }

        result = Flowagent().crew().kickoff(inputs=inputs)
        output=result.raw
        # Store the fun fact in our state
        self.state.news = output
        return output
    @listen(generate_news)
    def save_news(self,news):
        print("Saving news")

        news_dir=os.path.join(os.path.dirname(__file__),"..","..","news")
        os.makedirs(news_dir,exist_ok=True)
        news_file_path=os.path.join(news_dir,"news.md")
        with open(news_file_path,"w") as f:
            f.write(news)
        print(f"News saved to:{news_file_path}")
    @listen(generate_news)
    def generate_best_news(self,input):
        print("Generating best news")
        # Each flow state automatically gets a unique ID
        

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Choose the most important news from the following",
                },
            ],
        )

        important_news = response["choices"][0]["message"]["content"]

        return important_news
    @listen(and_(generate_news_topic,generate_news,save_news,generate_best_news))
    def logger(self, result):
        print(f"Logger:{result}")
        print(f"*" * 100)
        print("News Complete!")

async def main():
    flow=NewsFlow()
    flow.plot("my_flot_plot")
    await flow.kickoff()
asyncio.run(main())