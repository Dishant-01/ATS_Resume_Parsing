# from flask import Flask, render_template, request
# import pandas as pd

# # Import your functions (process_document, calculate_keyword_matching_percentage, evaluate_resumes)
# from templates.resume_function import process_document, calculate_keyword_matching_percentage, evaluate_resumes

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('./templates/index.html')  # Display the main input form
#     # new_env\templates\result.html
# @app.route('/rank', methods=['POST'])
# def rank_resumes():
#     directory = './resumes'
#     skillset = request.form.getlist('skillset')  # Get skillset as a list
#     top_k = int(request.form['top_k'])  # Convert top_k to integer

#     top_resumes = evaluate_resumes(directory, skillset)
#     top_resumes = top_resumes[:top_k]  # Select top k resumes

#     df = pd.DataFrame(top_resumes)

#     return render_template('results.html', df=df.to_html())  # Pass DataFrame as HTML

# if __name__ == '__main__':
#     app.run(debug=True)  # Run the Flask application in debug mode


from flask import Flask, render_template, request, send_file
import os
import pandas as pd
# from Resume_function.resume_function import process_document, calculate_keyword_matching_percentage, evaluate_resumes  # Optional: Import from separate file
from Resume_function import *

app = Flask(__name__)

# Set a static directory for any CSS or JavaScript files (optional)
# app.config['STATIC_FOLDER'] = 'static'

# Define the directory containing resumes (replace with your actual path)
# RESUME_DIR = 'resumes'
RESUME_DIR = 'E:/projects/ATS-2/resumes'  # Static directory within the Flask environment

@app.route('/show_resume/<filename>')
def show_resume(filename):
    directory = RESUME_DIR  # Change to your actual directory
    file_path = os.path.join(directory, filename)
    return send_file(file_path, as_attachment=False)

# @app.route('/show_resume/<filename>')
# def show_resume(filename):
#     return render_template('show_resume.html', filename=filename)


@app.route('/', methods=['GET', 'POST'])
def evaluate():
    skillset = []  # Initialize empty skillset list
    top_resumes = []  # Initialize empty list for results
    error_message = None  # Initialize error message

    if request.method == 'POST':
        # Get user input from form
        # directory = os.path.join(app.static_folder, RESUME_DIR)  # Use static directory for resumes
        directory = RESUME_DIR
        num_top_resumes = request.form.get('top_k')
        skillset_input = request.form.get('skillset')
        # skillset = skillset_input.split(',') 
        # skillset = [keyword.lower() for keyword in skillset_input.split(',')]


        # Validate user input
        try:
            num_top_resumes = int(num_top_resumes)
            if num_top_resumes <= 0:
                raise ValueError("Number of top resumes must be a positive integer.")
            skillset = skillset_input.split(',')  # Convert comma-separated string to list
        except (ValueError, TypeError) as e:
            error_message = str(e)

        if not error_message:
            # Process resumes if no validation errors
            top_resumes = evaluate_resumes(directory, skillset)
            # top_resumes = top_resumes[""]

            # Create Pandas DataFrame for table display
            df = pd.DataFrame(top_resumes)
            # print(top_resumes)

    return render_template('index.html', skillset=','.join(skillset), top_resumes=top_resumes, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)




















