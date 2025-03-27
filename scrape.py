from crewai import Agent, Task, Crew, Process
from custom_tools.selenium_tool import SeleniumScrapingTool
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# # Initialize the Chrome driver
# service = Service('chromedriver.exe')
# options = webdriver.ChromeOptions()
# options.add_argument("disable-infobars")  # to prevent the infobars popups to interfere with the script
# options.add_argument("start-maximized")  # some webpages may change the content depending on the size of the window so we access the maximized version of the browser
# options.add_argument("disable-dev-shm-usage")  # to avoid issues while interacting with the browser on a linux computer and replit is a linux computer
# options.add_argument("no-sandbox")  # to disable sandbox in the browser
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_argument("disable-blink-features=AutomationControlled")
# options.add_argument("--incognito")

# driver = webdriver.Chrome(service=service, options=options)

# Initialize the tool
selenium_tool = SeleniumScrapingTool(
    name="Interact and scrape dynamic websites",
    description="A tool that can be used to interact with and scrape content from dynamic websites.",
    # driver=driver,
)

# Define an agent that uses the tool
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Extract and analyze information from dynamic websites",
    backstory="""You are an expert web scraper who specializes in extracting 
    content from dynamic websites that require browser automation. You have 
    extensive knowledge of CSS selectors and can identify the right selectors 
    to target specific content on any website.""",
    tools=[selenium_tool],
    verbose=True,
)

# Create a task for the agent
scrape_task = Task(
    description="""
    Perform the following tasks from the website at {website_url}:
    
    1. Wait for 5 seconds for the page to load
    2. Click on the Contact Sales option
    3. Wait for 5 seconds for the page to load
    4. Extract the following information from the page:
        - The text of the points
    
    Compile this information into a structured format with each article's details grouped together.
    """,
    expected_output="A structured list of articles with their headlines, publication dates, and authors.",
    agent=web_scraper_agent,
)

# Run the task
crew = Crew(
    agents=[web_scraper_agent],
    tasks=[scrape_task],
    verbose=True,
    process=Process.sequential,
    output_log_file='crew.txt',
)

result = crew.kickoff(inputs={"website_url": "https://www.orangehrm.com/"})