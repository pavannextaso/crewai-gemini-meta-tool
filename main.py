import argparse
from crew import run_crew, run_metadata_analysis, run_content_analysis, run_both_analyses
from tools.simple_meta_extractor import extract_title_description

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CrewAI SEO Analysis Tools")
    parser.add_argument(
        "--input", "-i", 
        type=str, 
        help="Website URL to analyze"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Use interactive mode to enter input"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["metadata", "content", "both", "extract"],
        default="both",
        help="Analysis mode: metadata (brief metadata report), content (on-page SEO with recommendations), both (default), or extract (just title and description)"
    )
    
    args = parser.parse_args()
    
    # Get the URL input
    if args.interactive:
        custom_input = input("Enter website URL to analyze: ")
    elif args.input:
        custom_input = args.input
    else:
        # Default behavior - prompt for input
        custom_input = input("Enter website URL to analyze: ")
    
    print(f"Analyzing website: {custom_input}")
    print(f"Analysis mode: {args.mode}")
    
    # Run the appropriate analysis based on mode
    if args.mode == "metadata":
        print("\n🏷️  Running Metadata Analysis Only")
        print("This will fetch metadata and create a brief report on title tags, descriptions, and social media optimization.")
        result = run_metadata_analysis(custom_input)
        
    elif args.mode == "content":
        print("\n📄 Running Content Analysis Only")
        print("This will analyze on-page SEO content structure and provide detailed recommendations.")
        result = run_content_analysis(custom_input)
        
    elif args.mode == "extract":
        print("\n🎯 Extracting Title and Description Only")
        print("This will quickly extract just the title and meta description.")
        
        # Extract URL from input if needed
        import re
        if custom_input.startswith('http') or 'http' in custom_input:
            url_match = re.search(r'https?://[^\s]+', custom_input)
            if url_match:
                url = url_match.group()
            else:
                url = custom_input
        else:
            url = 'https://www.example.com'
        
        result = extract_title_description(url)
        print("\n=== Title and Description Extraction ===")
        print(result)
        
    else:  # both
        print("\n🔍 Running Complete SEO Analysis")
        print("This will run both metadata analysis and content analysis with recommendations.")
        result = run_both_analyses(custom_input)
    
    print("\n✅ Analysis completed!")
