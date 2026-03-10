# Cold Mail Generator - Deployment Guide

Since this project has been fully modernized with a Python backend (FastAPI) and an HTML frontend, you can deploy it live on the internet so recruiters can test it directly!

Because the application uses `ChromaDB` (which downloads a ~90MB ML model) and web scraping, we recommend using a cloud provider that gives backend compute, like **Render** or **Railway**.

## Deployment Steps (using Render.com)

Render is great because it has a completely free tier and can automatically deploy your code whenever you push to GitHub.

1. **Push your code to your GitHub Account**
   Make sure all your code is successfully sitting in your own GitHub repository (`github.com/neel26parekh/...`).

2. **Create a Render Account**
   Go to [Render.com](https://render.com) and sign up using your GitHub account.

3. **Create a New Web Service**
   - In the Render Dashboard, click **New +** and select **Web Service**.
   - Connect your GitHub account and select your `cold_mail_generator` repository.

4. **Configure the Service Requirements**
   - **Name**: `cold-mail-generator` (or whatever you like)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Set the Environment Variables**
   Expand the **Advanced** tier setting on the same page. Click **Add Environment Variable** and add the keys from your local `.env` file!
   - Key: `GROQ_API_KEY` | Value: `your_actual_key`
   - Key: `SENDER_EMAIL` | Value: `your_email@gmail.com`
   - Key: `GMAIL_APP_PASSWORD` | Value: `your_app_password`

6. **Deploy!**
   Click the **Create Web Service** button at the bottom. Render will spin up a server, install your Python packages, and give you a live HTTPS URL (e.g. `cold-mail-generator.onrender.com`) that you can put straight onto your CV!

---
*Note: Since Render's free tier spins down after 15 minutes of inactivity, the VERY FIRST time you open the website each day, it might take 1-2 minutes to "wake up" and download the AI model. Subsequent requests will be instant.*
