# Azure App Service Deployment Guide

## 🚀 Quick Deploy to Azure

### Prerequisites
- Azure account ([Create free account](https://azure.microsoft.com/free/))
- Azure CLI installed ([Install guide](https://docs.microsoft.com/cli/azure/install-azure-cli))
- Git installed

### Step 1: Build for Production

Run the build script:
```powershell
.\build-for-azure.ps1
```

This will:
- Build the React frontend
- Create optimized production files
- Verify all deployment files exist

### Step 2: Create Azure Resources

Login to Azure:
```bash
az login
```

Create a resource group:
```bash
az group create --name cimb-antiscam-rg --location southeastasia
```

Create an App Service plan (Free tier):
```bash
az appservice plan create --name cimb-antiscam-plan --resource-group cimb-antiscam-rg --sku F1 --is-linux
```

Create the web app (Python 3.11):
```bash
az webapp create --resource-group cimb-antiscam-rg --plan cimb-antiscam-plan --name cimb-antiscam-dashboard --runtime "PYTHON:3.11"
```

### Step 3: Configure Environment Variables

Set your API keys (optional - app works with mock data):
```bash
az webapp config appsettings set --resource-group cimb-antiscam-rg --name cimb-antiscam-dashboard --settings ML_API_ENDPOINT="your_ml_endpoint" AZURE_OPENAI_ENDPOINT="your_openai_endpoint" AZURE_OPENAI_KEY="your_openai_key" AZURE_OPENAI_DEPLOYMENT="gpt-4" FLASK_ENV="production"
```

Configure startup command:
```bash
az webapp config set --resource-group cimb-antiscam-rg --name cimb-antiscam-dashboard --startup-file "startup.sh"
```

### Step 4: Deploy the Application

#### Option A: Deploy from Local Git

Initialize git (if not already):
```bash
git init
git add .
git commit -m "Initial commit for Azure deployment"
```

Get Azure Git URL:
```bash
az webapp deployment source config-local-git --name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg
```

Add Azure remote and push:
```bash
git remote add azure <Git-URL-from-previous-command>
git push azure main
```

#### Option B: Deploy from GitHub

Connect your GitHub repository:
```bash
az webapp deployment source config --name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg --repo-url https://github.com/yourusername/anti-scam --branch main --manual-integration
```

#### Option C: Deploy using VS Code

1. Install Azure App Service extension
2. Sign in to Azure
3. Right-click your app folder
4. Select "Deploy to Web App..."
5. Choose your subscription and web app

### Step 5: Verify Deployment

Open your app:
```bash
az webapp browse --name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg
```

Or visit: `https://cimb-antiscam-dashboard.azurewebsites.net`

Check logs:
```bash
az webapp log tail --name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg
```

## 📊 Post-Deployment

### Test the Application
1. Visit your app URL
2. Upload the sample Excel file
3. Verify fraud detection works
4. Check that explanations are generated

### Configure Custom Domain (Optional)
```bash
az webapp config hostname add --webapp-name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg --hostname www.yourdomain.com
```

### Enable HTTPS (Automatic)
Azure App Service provides free SSL certificate automatically.

### Scale Up (Optional)

Upgrade to a better tier for production:
```bash
az appservice plan update --name cimb-antiscam-plan --resource-group cimb-antiscam-rg --sku B1
```

### Monitor Performance

View metrics in Azure Portal:
- Go to Azure Portal > App Services > cimb-antiscam-dashboard
- Check "Metrics" for CPU, memory, requests
- Enable "Application Insights" for detailed monitoring

## 🔧 Configuration Files

### requirements-azure.txt
Python dependencies including Gunicorn for production server.

### startup.sh
Azure startup script that:
- Installs Python dependencies
- Starts Gunicorn web server

### runtime.txt
Specifies Python 3.11 runtime.

### .deployment
Azure deployment configuration.

## 🎯 Environment Variables

Set in Azure Portal or via CLI:

| Variable | Required | Description |
|----------|----------|-------------|
| `ML_API_ENDPOINT` | No | Your ML model API URL |
| `AZURE_OPENAI_ENDPOINT` | No | Azure OpenAI endpoint |
| `AZURE_OPENAI_KEY` | No | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | No | Model deployment name (default: gpt-4) |
| `FLASK_ENV` | Yes | Set to "production" |
| `PORT` | Auto | Azure sets this automatically |

**Note:** If API variables are not set, the app automatically uses mock data.

## 📱 Application Architecture on Azure

```
Internet
    │
    ↓
Azure Load Balancer
    │
    ↓
Azure App Service (Linux)
    ├── Python 3.11 Runtime
    ├── Gunicorn (WSGI Server)
    ├── Flask Backend (API)
    └── React Frontend (Static Files)
```

## 💰 Cost Estimation

### Free Tier (F1)
- **Cost:** FREE
- **Specs:** 1 GB RAM, 1 GB Storage
- **Limits:** 60 CPU minutes/day
- **Best for:** Demo, hackathon, development

### Basic Tier (B1)
- **Cost:** ~$13/month
- **Specs:** 1.75 GB RAM, 10 GB Storage
- **Limits:** No daily limits
- **Best for:** Small production apps

### Standard Tier (S1)
- **Cost:** ~$70/month
- **Specs:** 1.75 GB RAM, 50 GB Storage
- **Features:** Auto-scaling, staging slots
- **Best for:** Production apps with scaling needs

## 🔒 Security Best Practices

1. **Store secrets in Azure Key Vault:**
   ```bash
   az keyvault create --name cimb-antiscam-kv --resource-group cimb-antiscam-rg --location southeastasia
   ```

2. **Enable managed identity:**
   ```bash
   az webapp identity assign --name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg
   ```

3. **Restrict access with IP filtering** (Azure Portal → Networking)

4. **Enable diagnostic logging** for security monitoring

## 🐛 Troubleshooting

### Application won't start
- Check logs: `az webapp log tail --name cimb-antiscam-dashboard --resource-group cimb-antiscam-rg`
- Verify startup.sh has execute permissions
- Check Python version matches runtime.txt

### 404 errors on frontend routes
- Ensure app.py has catch-all route for React Router
- Verify frontend build folder exists

### API calls failing
- Check CORS configuration
- Verify environment variables are set correctly
- Test API endpoints: `/api/status`, `/api/upload`

### High memory usage
- Upgrade to B1 or higher tier
- Optimize pandas operations
- Consider caching results

## 📚 Additional Resources

- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Python on Azure App Service](https://docs.microsoft.com/azure/app-service/quickstart-python)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)
- [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)

## 🎓 Demo Tips

For hackathon demos:
1. Use the Free (F1) tier - it's perfect for demos
2. Keep mock mode enabled - no API keys needed
3. Prepare sample data in advance
4. Test the full flow before presenting
5. Have the Azure Portal open to show live metrics

---

Need help? Check the logs or consult Azure documentation!
