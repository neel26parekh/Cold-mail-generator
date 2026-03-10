# app/main.py

import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langchain_community.document_loaders import WebBaseLoader

# Local imports from the services module
from app.services.chains import Chain
from app.services.portfolio import Portfolio
from app.services.utils import clean_text
from app.services.email_sender import EmailSender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cold Mail Generator")
templates = Jinja2Templates(directory="app/templates")

chain = Chain()
portfolio = Portfolio()
email_sender = EmailSender()

class InputData(BaseModel):
    url: str

class EmailData(BaseModel):
    recipient_email: str
    subject: str
    body: str

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    logger.info("Serving the home page.")
    return templates.TemplateResponse(request, "index.html")

@app.post("/send_email")
def send_email_endpoint(data: EmailData):
    try:
        logger.info(f"Received request to send email to: {data.recipient_email}")
        success = email_sender.send_email(
            recipient_email=data.recipient_email,
            subject=data.subject,
            body=data.body
        )
        if success:
            return {"status": "success", "message": "Email sent successfully."}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email.")
            
    except ValueError as ve:
        # Catch misconfiguration errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_email")
def generate_email(data: InputData):
    try:
        logger.info(f"Received request to generate email for URL: {data.url}")
        
        # Load and clean page content
        loader = WebBaseLoader([data.url])
        page_data = loader.load().pop().page_content
        logger.info(f"Raw HTML length: {len(page_data)}")
        
        cleaned = clean_text(page_data)
        logger.info(f"Cleaned text length: {len(cleaned)}")
        logger.info(f"Cleaned text snippet: {cleaned[:500]}")
        
        logger.info("Successfully loaded and cleaned page data from the provided URL.")
        
        # Load portfolio and extract jobs
        portfolio.load_portfolio()
        jobs = chain.extract_jobs(cleaned)
        
        if not jobs:
            logger.warning("No job postings found on the provided page.")
        else:
            logger.info(f"Extracted {len(jobs)} job(s) from the page.")
        
        result = []
        for index, job in enumerate(jobs):
            skills = job.get('skills', [])
            logger.info(f"Analyzing Job #{index + 1} with skills: {skills}")
            
            # Query relevant portfolio links based on identified skills
            links = portfolio.query_links(skills)
            
            # Write the cold mail
            email = chain.write_mail(job, links)
            result.append({"email": email})
            
        logger.info(f"Successfully generated {len(result)} emails.")
        return {"emails": result}
    
    except Exception as e:
        logger.error(f"Error during email generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
