# 🚀 Azure Deployment - Quick Reference

## ✅ Files Ready for Azure

Your application is now configured for Azure App Service deployment:

### ✓ Backend Configuration
- `app.py` - Updated to serve React frontend in production
- `requirements-azure.txt` - Production dependencies with Gunicorn
- `startup.sh` - Azure startup script
- `runtime.txt` - Python 3.11 runtime specification
- `.deployment` - Azure build configuration

### ✓ Frontend Ready
- React app will be built and served by Flask
- All routes handled correctly
- Static files optimized for production

## 🎯 Two Deployment Options

### Option 1: Simple Local Testing First

```powershell
# Quick setup
.\quick-setup.ps1

# Run backend
python app.py

# In new terminal, run frontend
cd frontend
npm install
npm start
```

Visit: http://localhost:3000

### Option 2: Deploy to Azure App Service

```powershell
# Step 1: Build for production
.\build-for-azure.ps1

# Step 2: Login to Azure
az login

# Step 3: Create resources (one time)
az group create --name cimb-antiscam-rg --location southeastasia

az appservice plan create --name cimb-antiscam-plan --resource-group cimb-antiscam-rg --sku F1 --is-linux

az webapp create --resource-group cimb-antiscam-rg --plan cimb-antiscam-plan --name cimb-antiscam-dashboard --runtime "PYTHON:3.11"

# Step 4: Configure startup
az webapp config set --resource-group cimb-antiscam-rg --name cimb-antiscam-dashboard --startup-file "startup.sh"

# Step 5: Deploy
az webapp up --name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg --runtime "PYTHON:3.11"
```

Your app will be live at: `https://cimb-antiscam-dashboard.azurewebsites.net`

## 📋 Pre-Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js installed
- [ ] Azure CLI installed (`az --version`)
- [ ] Logged into Azure (`az login`)
- [ ] Frontend built (`.\build-for-azure.ps1`)
- [ ] Sample data generated (`python generate_sample_data.py`)

## 🎨 What Gets Deployed

```
Azure App Service
├── Backend (Flask + Gunicorn)
│   ├── API endpoints (/api/*)
│   ├── ML fraud detection (with mock fallback)
│   └── Azure OpenAI integration (with mock fallback)
└── Frontend (React - Static Build)
    ├── Dashboard UI
    ├── File upload
    ├── Transaction table
    └── Fraud analysis modal
```

## 💡 Key Features

✅ **Works in Mock Mode** - No API keys needed for demo  
✅ **Production Ready** - Gunicorn + optimized build  
✅ **Secure** - Environment variables for secrets  
✅ **Scalable** - Easy to upgrade tier  
✅ **Cost Effective** - Free tier available  

## 🎓 For Your Hackathon

### Local Demo
1. Run `.\quick-setup.ps1`
2. Start both servers
3. Demo on localhost

### Cloud Demo
1. Run `.\build-for-azure.ps1`
2. Deploy to Azure
3. Share live URL with judges

## 📞 Need Help?

- **Local testing issues**: Run `.\quick-setup.ps1`
- **Azure deployment**: Check `AZURE_DEPLOYMENT.md`
- **Build problems**: Verify Node.js and Python versions

## 🏆 Success Tips

1. **Test locally first** before deploying to Azure
2. **Use mock mode** for reliable demos (no API dependencies)
3. **Keep the free tier** for hackathon (no costs)
4. **Have sample data ready** to show fraud detection
5. **Prepare talking points** about the architecture

---

**Current Status:** ✅ All files configured and ready!

**Next Step:** Choose local testing OR Azure deployment above.
