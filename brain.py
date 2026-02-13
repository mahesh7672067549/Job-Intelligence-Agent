from google import genai

# Use your working API key
client = genai.Client(api_key="AIzaSyAAbR6q9Wmqvb5kz5nxW-XwHHuFxSRjge8")

def filter_jobs(raw_job_list):
    """
    This function acts as the 'Analyst'. 
    It takes a messy list of jobs and returns only the ones suitable for you.
    """
    # We explicitly tell the AI to include the link in the final response
    prompt = f"""
    I am a student with an Integrated M.Tech in Software Engineering. 
    My skills: Java, SQL, Python. I am looking for 'Fresher' or 'Intern' roles.
    
    Here is a list of job titles and their links:
    {raw_job_list}
    
    Task: Identify the jobs that are 100% suitable for a fresher with my skills.
    - Ignore anything that says 'Senior', 'Lead', 'Manager', or '5+ years'.
    - Ignore non-tech roles.
    
    Return the output as a numbered list with:
    1. The exact Job Title.
    2. The EXACT Link provided (DO NOT EXCLUDE THE LINK).
    3. A 5-word reason why it fits.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error in Brain: {e}"