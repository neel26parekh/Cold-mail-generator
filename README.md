# 📧 Cold Mail Generator

🔗 **Live Demo:** [https://cold-mail-generator-rf93.onrender.com](https://cold-mail-generator-rf93.onrender.com)

Cold email generator for services company using groq, langchain and streamlit. It allows users to input the URL of a company's careers page. The tool then extracts job listings from that page and generates personalized cold emails. These emails include relevant portfolio links sourced from a vector database, based on the specific job descriptions. 

![alt text](<Screenshot 2025-05-23 at 12.05.44 AM.png>)

## Architecture Diagram
![image](https://github.com/user-attachments/assets/930bf63e-f5e1-4980-93b8-2f51fa5fe9a1)


## Set-up
1. To get started we first need to get an API_KEY from here: https://console.groq.com/keys. Inside `.env` (create a new file at root if it doesn't exist) update the value of `GROQ_API_KEY` with the API_KEY you created. 

2. To get started, first install the dependencies using:
    ```commandline
     pip install -r requirements.txt
    ```
   
3. Run the FastAPI app:
   ```commandline
   uvicorn app.main:app --reload
   ```
   
4. Open your browser and navigate to `http://localhost:8000` to access the application.
   
