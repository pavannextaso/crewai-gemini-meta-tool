from crew import run_crew

if __name__ == "__main__":

    # To run plagiarism
    # input_data = {"text": "Photosynthesis is the process by which green plants make their food. can you tell me where the text is present on other websites."}
    # input_data = {"text": "provide me title and descriptions of these urls https://www.smallcase.com/lists/multibagger-penny-stocks/"}

    # input_data = {"text": "Provide me meta data report for these urls https://www.smallcase.com/lists/multibagger-penny-stocks/ and https://nextlabs.io"}
    # input_data = {"text": "Provide me content report for these urls https://www.smallcase.com/lists/multibagger-penny-stocks/ and https://nextlabs.io"}
    # input_data = {"text": "provide me title, descriptions of these urls https://www.smallcase.com/lists/multibagger-penny-stocks/ and https://nextlabs.io"}
    
    input_data = {"text": "Provide me content report for these urls https://www.smallcase.com/lists/multibagger-penny-stocks/"}

    
    result = run_crew(input_data)
    print("\n=== Final Results ===")
    print("Results: ",result)
    print("\n✅ Analysis completed!")
