import os
import regex as re
from pypdf import PdfReader
import docx2txt




def process_document(file_path):
    if file_path.lower().endswith('.pdf'):
        # Read PDF file
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()
    elif file_path.lower().endswith('.docx'):
        # Read DOCX file
        full_text = docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX files are supported.")
    return full_text.lower()


def calculate_keyword_matching_percentage(keywords, resume_text):
    # Convert keywords to lowercase
    # keywords = keywords.split(',')
    # keywords = [keyword.lower() for keyword in keywords] - #do not touch
    # keywords = [item.strip("'") for item in keywords] #input
    # keywords = [item.strip('" ') for item in keywords] #input
    # keywords = [item.strip("[]' ") for item in keywords]  #do not touch
    # keywords = [keyword.lower() for keyword in keywords]  #do not touch
    keywords = [keyword.lower().strip("[]' ") for keyword in keywords]
    print('keywords', keywords) #working complete
    # Tokenize the resume text
    # resume_tokens = set(resume_text.lower().split())
    resume_tokens = set(token.lower().strip() for token in resume_text.split())
    # print('resume tokens', resume_tokens) #working  complete
    
    # Find mutual keywords (multi-word phrases)
    mutual_keywords = set()
    for keyword in keywords:
        # keyword_words = keyword.split()
        # print('keyword_words', )
        # Check if all words in the keyword are present in the resume
        if all(word in resume_tokens for word in keyword.split()):
            mutual_keywords.add(keyword) # logic working completely
        # if any(word in resume_tokens for word in keyword.split()):
        #     mutual_keywords.add(keyword)
        # if keyword in resume_tokens:
        #     mutual_keywords.add(keyword)
        # if all(word in resume_tokens for word in keyword.split()):
        #     mutual_keywords.add(keyword)


    # Calculate percentage of overlap
    if len(keywords) == 0:
        return 0, mutual_keywords, set()
    matching_percentage = (len(mutual_keywords) / len(keywords)) * 100

    # Find non-matching keywords
    # non_matching_keywords = set(keywords).difference(mutual_keywords)
    non_matching_keywords = set(keywords).difference(mutual_keywords)
    print('non_matchingg', non_matching_keywords)


    return matching_percentage, mutual_keywords, non_matching_keywords


def evaluate_resumes(directory, skillset):
    # print('inside evaluate function')
    # print('directory',directory)
    # print(os.listdir(directory)) # all 3 lines are working
    

    # List to store the results
    results = []
    # directory = os.path.join('new_env\static',directory)
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        # if filename.endswith('.txt'):  # Assuming resumes are in .txt format
        file_path = os.path.join(directory, filename)
        if filename.lower().endswith(('.pdf', '.docx')):
            # print('Inside directory after checking file type extracting')
            # resume_text = process_document(filename)
            # Read the resume file
            # with open(os.path.join(directory, filename), 'r') as file:
            #     resume_text = file.read()
            resume_text = process_document(str((os.path.join(directory, filename))))
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", resume_text)
            # Calculate the matching percentage
            matching_percentage, mutual_keywords, non_matching_keywords = calculate_keyword_matching_percentage(skillset, resume_text)
            # print(matching_percentage,mutual_keywords)
            # print('checkingggggggggg',matching_percentage,mutual_keywords, non_matching_keywords)

            # Append the result to the list
            results.append({
                'filename': filename,
                'matching_percentage': matching_percentage,
                'matching_keywords': mutual_keywords,
                'non_matching_keywords': non_matching_keywords,
                'emails': emails,
                'file_path':file_path,
            })
            # print('keywords',keywords)
            print('matching keywords', mutual_keywords)
    # Sort the results based on matching percentage in descending order
    sorted_results = sorted(results, key=lambda x: x['matching_percentage'], reverse=True)

    # Return the top 3 results
    return sorted_results[:5]
# if __name__ == "__main__":
#     evaluate_resumes('resumes',['Manpower Planning','TAT or Turnaround time','Success factor', 
#                                'Onboarding','Induction', 'Talent  Acquisition', 'Recruitment'])