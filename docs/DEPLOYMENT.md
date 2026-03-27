# 🚀 Deploying Niva AI

Niva can be deployed to the cloud (e.g., Render, Heroku) or containerized via Docker.

## Option 1: Cloud Hosting (Render)
1. Push this repository to GitHub.
2. Connect your GitHub to [Render](https://render.com).
3. Select **Web Service** and use the `render.yaml` blueprint.
4. **Note**: In cloud mode, camera/mic access relies on the browser client. Ensure your users access the URL via HTTPS.

## Option 2: Docker (Local/Server)
```bash
docker build -t niva-ai .
docker run -p 8000:8000 niva-ai
```

## Option 3: Standard Portable Deployment
Simply copy the folder to any Windows machine with Python installed and run:
```powershell
python main.py
```
Niva will automatically handle the rest.

---

### ⚠️ Cloud Limitations
While Niva's *brain* can live in the cloud, its *senses* (Camera/Mic) are local. When hosted, the `www/` interface acts as the sensory input hub.
