from crewai import Task
from agents import meta_researcher, content_researcher, meta_writer, seo_writer
import re

def extract_url_from_input(url_or_input):
    """Extract URL from user input or return a default URL."""
    if url_or_input.startswith('http') or 'http' in url_or_input:
        # Extract URL if it's part of a larger string
        url_match = re.search(r'https?://[^\s]+', url_or_input)
        if url_match:
            return url_match.group()
        else:
            return url_or_input
    else:
        # If no URL provided, use a default URL
        return 'https://www.example.com'

# Task 1: Metadata Analysis
def create_metadata_analysis_task(url_or_input):
    """Create a task to fetch and analyze website metadata."""
    url = extract_url_from_input(url_or_input)
    
    return Task(
        description=f"""Extract and analyze metadata from the website: {url}
        
        Use the fetch_meta tool to extract:
        - Basic metadata (title, description, keywords)
        - Open Graph tags for social media
        - Twitter Card data
        - H1 tag information
        
        Return the complete JSON data from the fetch_meta tool.
        
        User request: {url_or_input}
        """,
        agent=meta_researcher,
        expected_output="Complete JSON data containing website metadata including title, description, keywords, Open Graph, and Twitter Card information."
    )

# Task 2: On-Page SEO Content Analysis
def create_content_analysis_task(url_or_input):
    """Create a task to analyze website content structure for on-page SEO."""
    url = extract_url_from_input(url_or_input)
    
    return Task(
        description=f"""Analyze the content structure and on-page SEO elements of the website: {url}
        
        Use the analyze_content tool to examine:
        - Content metrics (word count, readability)
        - Heading structure (H1-H6 distribution)
        - Image optimization (alt text coverage)
        - Link analysis (internal vs external)
        - Top keywords and keyword density
        
        Return the complete JSON data from the analyze_content tool.
        
        User request: {url_or_input}
        """,
        agent=content_researcher,
        expected_output="Complete JSON data containing content analysis including word count, heading structure, image metrics, link analysis, and keyword information."
    )

# Task 3: Metadata Report Writing
def create_metadata_report_task():
    """Create a brief report focused on metadata analysis."""
    return Task(
        description="""Based on the metadata JSON data provided, create a focused report on metadata optimization:
        
        **Report Structure:**
        1. **Title Tag Analysis**: Evaluate length, keywords, and optimization
        2. **Meta Description Review**: Check length, compelling copy, and CTR potential
        3. **Keywords Assessment**: Analyze keyword presence and relevance
        4. **Social Media Optimization**: Review Open Graph and Twitter Card setup
        5. **Quick Recommendations**: 3-5 actionable metadata improvements
        
        Keep the report concise and focused on metadata elements only.
        Include specific character counts and optimization scores where available.
        """,
        agent=meta_writer,
        expected_output="A concise, focused report on website metadata with specific recommendations for title tags, meta descriptions, and social media optimization."
    )

# Task 4: On-Page SEO Report with Recommendations
def create_seo_recommendations_task():
    """Create a detailed on-page SEO report with actionable recommendations."""
    return Task(
        description="""Based on the content analysis JSON data provided, create a comprehensive on-page SEO report with detailed recommendations:
        
        **Report Structure:**
        1. **Content Quality Assessment**: Word count, readability, and content depth
        2. **Heading Structure Analysis**: H1-H6 hierarchy and optimization opportunities
        3. **Image SEO Review**: Alt text coverage and image optimization recommendations
        4. **Internal Link Strategy**: Link distribution and internal linking opportunities
        5. **Keyword Optimization**: Top keywords analysis and keyword strategy recommendations
        6. **Technical On-Page Issues**: Identify and prioritize technical improvements
        7. **Action Plan**: Prioritized list of 10+ specific recommendations with implementation steps
        
        Provide detailed, actionable recommendations with priority levels (High/Medium/Low).
        Include specific metrics and benchmarks for improvements.
        """,
        agent=seo_writer,
        expected_output="A comprehensive on-page SEO report with detailed analysis and prioritized action plan containing specific, actionable recommendations for content optimization."
    )

# Functions to run individual workflows
def create_metadata_workflow_tasks(url_or_input):
    """Create tasks for metadata analysis workflow."""
    return [
        create_metadata_analysis_task(url_or_input),
        create_metadata_report_task()
    ]

def create_content_workflow_tasks(url_or_input):
    """Create tasks for content analysis workflow."""
    return [
        create_content_analysis_task(url_or_input),
        create_seo_recommendations_task()
    ]
