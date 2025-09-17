# ☁️ Streamlit Cloud Deployment Guide

## 🚀 Deploy Your AI Search Engine to Streamlit Cloud

This guide will help you deploy your AI Search Engine to Streamlit Cloud for a permanent live demo.

## 📋 Prerequisites

1. **GitHub Repository**: Your code is already on GitHub at [https://github.com/YASWANTHthottempudi/SearchEnging_langchain](https://github.com/YASWANTHthottempudi/SearchEnging_langchain)
2. **Groq API Key**: Get a free API key from [console.groq.com](https://console.groq.com/)
3. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io/)

## 🚀 Step-by-Step Deployment

### Step 1: Access Streamlit Cloud
1. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click **"New app"**

### Step 2: Configure Your App
1. **Repository**: Select `YASWANTHthottempudi/SearchEnging_langchain`
2. **Branch**: Select `main`
3. **Main file path**: Enter `app.py`
4. **App URL**: Choose a custom URL like `yaswanth-search-engine`

### Step 3: Add Environment Variables
In the **"Secrets"** section, add:
```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

### Step 4: Deploy
1. Click **"Deploy!"**
2. Wait for the deployment to complete (usually 2-3 minutes)
3. Your app will be live at: `https://yaswanth-search-engine.streamlit.app`

## 🔧 Configuration Details

### App Configuration
- **Repository**: `YASWANTHthottempudi/SearchEnging_langchain`
- **Branch**: `main`
- **Main file**: `app.py`
- **Python version**: 3.12 (automatically detected)

### Environment Variables
```toml
# Add these in Streamlit Cloud secrets
GROQ_API_KEY = "gsk_your_actual_api_key_here"
```

### Requirements
Streamlit Cloud will automatically install dependencies from `requirements.txt`:
- streamlit>=1.49.0
- langchain-groq>=0.3.0
- langchain-community>=0.3.0
- And all other dependencies...

## 🌐 Live Demo URLs

After deployment, your app will be available at:
- **Primary URL**: `https://yaswanth-search-engine.streamlit.app`
- **Alternative URL**: `https://share.streamlit.io/YASWANTHthottempudi/SearchEnging_langchain/main`

## 🔒 Security Features

### ✅ API Key Protection
- API keys are stored securely in Streamlit Cloud secrets
- No API keys in your source code
- Environment variables are encrypted

### ✅ Repository Security
- `.env` file is excluded from repository
- `.gitignore` protects sensitive files
- Only necessary files are deployed

## 🎯 Features Available in Live Demo

### ✅ Core Features
- **Multi-source search** (Wikipedia, ArXiv, Web)
- **AI-powered responses** with Groq
- **Modern UI** with custom styling
- **Search history** and analytics
- **Export functionality**

### ✅ User Experience
- **Responsive design** for all devices
- **Real-time search** with streaming responses
- **Interactive configuration** options
- **Professional branding** with your name

## 🚨 Troubleshooting

### Common Issues

1. **App won't start**
   - Check that `app.py` is the main file
   - Verify all dependencies are in `requirements.txt`
   - Check Streamlit Cloud logs for errors

2. **API key not working**
   - Ensure the API key is correctly added to secrets
   - Verify the key starts with `gsk_`
   - Check that the key is active on Groq console

3. **Import errors**
   - All dependencies should be in `requirements.txt`
   - Check for version conflicts
   - Verify Python version compatibility

### Getting Help
- **Streamlit Cloud Docs**: [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **GitHub Issues**: Create an issue in your repository
- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)

## 📊 Deployment Benefits

### ✅ Professional Portfolio
- **Live demo** accessible to anyone
- **Professional URL** for sharing
- **Always available** (24/7 uptime)
- **Automatic updates** when you push to GitHub

### ✅ Easy Sharing
- **Share with employers** and colleagues
- **Include in resume** and portfolio
- **Demo during interviews**
- **Showcase your skills** in real-time

## 🔄 Updating Your App

To update your live demo:
1. **Make changes** to your local code
2. **Commit and push** to GitHub
3. **Streamlit Cloud** automatically redeploys
4. **Changes go live** in 2-3 minutes

## 🎉 Success!

Once deployed, your AI Search Engine will be:
- ✅ **Live and accessible** to anyone
- ✅ **Professional and polished**
- ✅ **Ready for your portfolio**
- ✅ **Automatically updated** with your changes

---

**Deploy now**: [https://share.streamlit.io/](https://share.streamlit.io/)  
**Repository**: [https://github.com/YASWANTHthottempudi/SearchEnging_langchain](https://github.com/YASWANTHthottempudi/SearchEnging_langchain)
