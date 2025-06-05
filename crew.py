from crewai import Crew
from tasks import (
    create_metadata_workflow_tasks, 
    create_content_workflow_tasks,
    create_metadata_analysis_task,
    create_content_analysis_task,
    create_metadata_report_task,
    create_seo_recommendations_task
)
from agents import meta_researcher, content_researcher, meta_writer, seo_writer

def run_metadata_analysis(url_input="https://www.example.com"):
    """Run metadata analysis workflow - fetches metadata and creates brief report."""
    print(f"\n=== Starting Metadata Analysis for: {url_input} ===")
    
    # Get tasks for metadata workflow
    tasks = create_metadata_workflow_tasks(url_input)
    
    # Create crew for metadata analysis
    crew = Crew(
        agents=[meta_researcher, meta_writer],
        tasks=tasks,
        verbose=True,
        process="sequential"
    )
    
    # Run the crew
    result = crew.kickoff()
    print("\n=== Metadata Analysis Report ===")
    print(result)
    return result

def run_content_analysis(url_input="https://www.example.com"):
    """Run on-page SEO content analysis workflow - analyzes content and provides recommendations."""
    print(f"\n=== Starting Content Analysis for: {url_input} ===")
    
    # Get tasks for content workflow
    tasks = create_content_workflow_tasks(url_input)
    
    # Create crew for content analysis
    crew = Crew(
        agents=[content_researcher, seo_writer],
        tasks=tasks,
        verbose=True,
        process="sequential"
    )
    
    # Run the crew
    result = crew.kickoff()
    print("\n=== Content Analysis Report with Recommendations ===")
    print(result)
    return result

def run_both_analyses(url_input="https://www.example.com"):
    """Run both metadata and content analysis workflows separately."""
    print(f"\n=== Starting Complete SEO Analysis for: {url_input} ===")
    
    # Run metadata analysis first
    print("\n🔍 STEP 1: Metadata Analysis")
    metadata_result = run_metadata_analysis(url_input)
    
    print("\n" + "="*60)
    
    # Run content analysis second
    print("\n🔍 STEP 2: Content Analysis")
    content_result = run_content_analysis(url_input)
    
    return {
        "metadata_analysis": metadata_result,
        "content_analysis": content_result
    }

# Backward compatibility - keep the original function name
def run_crew(custom_input="https://www.example.com"):
    """Run both analyses for backward compatibility."""
    return run_both_analyses(custom_input)
