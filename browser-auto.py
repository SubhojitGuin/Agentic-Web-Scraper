from pydantic import BaseModel
from typing import List, Any
from browser_use import Controller, Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from langchain_openai import ChatOpenAI
import os

# Define the output format as a Pydantic model
class Post(BaseModel):
	# post_title: str
	# post_url: str
	# num_comments: int
	# hours_since_post: int
	headline: str
	description: str
	


class Posts(BaseModel):
	posts: List[Post]
	error: str


controller = Controller(output_model=Posts)


sensitive_data = {
    "fullname": os.getenv("FULLNAME"),
    "ph_number": os.getenv("PH_NUMBER")
}

async def main():
	task = """Go to `https://www.orangehrm.com/` and click on the Contact button and enter the fullname and ph_number and collect the points description from the page. 
	If you do not find the option, return the error message in `error` and stop the navigation."""
	model = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')
	agent = Agent(task=task, llm=model, controller=controller, sensitive_data=sensitive_data)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed: Posts = Posts.model_validate_json(result)

		for post in parsed.posts:
			print('\n--------------------------------')
			print(f'Headline:          {post.headline}')
			print(f'Description:      {post.description}')
			# print(f'Title:            {post.post_title}')
			# print(f'URL:              {post.post_url}')
			# print(f'Comments:         {post.num_comments}')
			# print(f'Hours since post: {post.hours_since_post}')
		
		print(f"Error:         {parsed.error}")
	
	else:
		print('No result')


if __name__ == '__main__':
	asyncio.run(main())