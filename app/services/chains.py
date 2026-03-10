import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="meta-llama/llama-4-scout-17b-16e-instruct")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
### JOB DESCRIPTION:
{job_description}

### INSTRUCTION:
I'm Neel Parekh — a Senior Machine Learning Engineer and AI Engineer. I specialize in building scalable, intelligent systems that connect data to business goals. With experience in delivering real-world AI and ML solutions, I’m confident in my ability to directly contribute to the responsibilities and vision outlined in this role.

Your job is to write a cold email to the client regarding the job mentioned above, describing Neel's capabilities in fulfilling their needs.  
Also highlight how his background in Data Science, ML, AI, GenAI, and MLOps directly applies to the role.  
Use a confident but conversational tone. Dont always write Data Scientist, use synonyms like ML Engineer, AI Engineer, GenAI Engineer, MLOps Engineer, etc. as per the job description.
Do not provide a preamble. 
This is my resume details 
use if needed:
Neel Parekh Email : mcparekh1937@gmail.com
GitHub: https://github.com/neel26parekh Mobile : +917874258086


Skills
• Mathematics: Linear Algebra, Calculus, Statistics & Probability
• Languages: Python, SQL
• Languages: Python, SQL, HTML/CSS
• Machine Learning: Supervised Learning, Random Forest, Decision Trees, Ensemble Methods, PCA
Data Science: Pandas, NumPy, Matplotlib, Seaborn, Feature Engineering, Exploratory Data Analysis
AI / LLM: LangChain, Large Language Models (Llama 3), Retrieval-Augmented Generation (RAG), Prompt
Engineering
MLOps & Tools: FastAPI, Docker, Git, GitHub, CI/CD (Vercel/Render), Streamlit
• Mathematics: Linear Algebra, Calculus, Statistics, Probability
Experience
• AI Engineer at Satvabit Surat
◦ Built end-to-end systems that integrate data ingestion, preprocessing, feature engineering, model training, evaluation, and deployment using AWS, FastAPI, and GitHub Actions.
◦ Designed scalable, automated production-ready MLOps pipelines.
• Capstone MLOps Project & ATS resume checker
◦ Demonstrated ability to design and implement highly scalable, automated ML systems using modern infra.

### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))