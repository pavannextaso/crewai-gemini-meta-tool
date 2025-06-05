from crewai import Agent
from llm import get_gemini_llm
from tools.meta_fetcher import fetch_meta
from tools.content_analyzer import analyze_content

llm = get_gemini_llm()

# Agent for metadata analysis
meta_researcher = Agent(
    role="Metadata Analyst",
    goal="Extract and analyze website metadata for basic SEO information",
    backstory="Specialist in extracting website metadata including title tags, meta descriptions, Open Graph, and Twitter Card data.",
    tools=[fetch_meta],
    verbose=True,
    llm=llm
)

# Agent for on-page SEO content analysis
content_researcher = Agent(
    role="On-Page SEO Analyst",
    goal="Analyze website content structure and provide SEO recommendations",
    backstory="Expert in on-page SEO analysis including content structure, headings, keywords, images, and internal linking strategies.",
    tools=[analyze_content],
    verbose=True,
    llm=llm
)

# Agent for metadata reports
meta_writer = Agent(
    role="Metadata Report Writer",
    goal="Create brief, focused reports on website metadata",
    backstory="Skilled in writing concise metadata analysis reports focusing on title tags, descriptions, and social media optimization.",
    verbose=True,
    llm=llm
)

# Agent for on-page SEO reports with recommendations
seo_writer = Agent(
    role="SEO Recommendations Writer",
    goal="Create detailed on-page SEO reports with actionable recommendations",
    backstory="Expert in translating technical SEO data into actionable recommendations for content optimization, structure improvements, and ranking enhancements.",
    verbose=True,
    llm=llm
)
