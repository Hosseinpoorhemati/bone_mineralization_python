# 🚀 Deploy to Streamlit Cloud - Step-by-Step Guide

This guide will help you deploy the Bone Mineralization simulator to Streamlit Cloud in 10 minutes.

## Prerequisites

- GitHub account (free at [github.com](https://github.com))
- Streamlit Community Cloud account (free at [streamlit.io/cloud](https://share.streamlit.io))

## Step 1: Create a GitHub Repository

### Option A: Create a NEW repository (Recommended)

1. Go to [github.com/new](https://github.com/new)
2. Enter repository name: `bone_mineralization_python`
3. Description: "Bone Mineralization Integrated Model - Interactive Python App"
4. Select **Public** (so anyone can access)
5. Check "Add a README file"
6. Click **Create repository**

### Option B: Fork Existing Repository

If there's already a repository, just fork it to your account.

## Step 2: Upload Project Files to GitHub

### Option A: Using Git (Recommended)

```bash
# Navigate to your local project directory
cd /Users/hosseinp/bone

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Bone mineralization simulator"

# Add remote repository (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/bone_mineralization_python.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Web Interface

1. Go to your repository on GitHub
2. Click "Add file" → "Upload files"
3. Drag and drop these files:
   - `app_single.py` (main app)
   - `bone_mineralization.py` (library)
   - `requirements.txt` (dependencies)
   - `.gitignore` (git ignore file)
   - `.streamlit/config.toml` (Streamlit config)
   - `README.md` or `GitHub_README.md` (documentation)

4. Click "Commit changes"

## Step 3: Prepare for Streamlit Cloud

Make sure you have these files in your repository:

### ✅ Required Files

**`app_single.py`** (or rename to `streamlit_app.py`)
- This is your main app file
- Streamlit Cloud will run this

**`requirements.txt`**
```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
streamlit>=1.20.0
```

**`.streamlit/config.toml`**
- Already created with optimal settings

**`.gitignore`**
- Already created to exclude unnecessary files

### ✅ Optional but Recommended

**`README.md`** or **`GitHub_README.md`**
- Explain your project
- Include the deployment badge

**`.streamlit/secrets.toml`**
- Only needed if you have API keys (not needed for this project)

## Step 4: Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account
   - Click "Log in with GitHub"
   - Authorize Streamlit to access your repositories

3. **Click "New app"**

4. **Fill in the deployment details:**
   - **Repository:** Select your repository from the dropdown
     - (e.g., `USERNAME/bone_mineralization_python`)
   - **Branch:** Select `main`
   - **Main file path:** Enter `app_single.py`

5. **Click "Deploy"**

Done! Streamlit Cloud will:
- Install dependencies from requirements.txt
- Run your app
- Generate a public URL

## Step 5: Access Your App

After deployment (usually 1-2 minutes):

1. You'll see a URL like: `https://bone-mineralization.streamlit.app`
2. Your app is live!
3. Share this URL with anyone to let them test

## Sharing Your App

### Public URL
Everyone with the link can access your app:
```
https://bone-mineralization.streamlit.app
```

### Direct Links to Sections
Users can also jump to specific sections:
```
https://bone-mineralization.streamlit.app?page=1
```

### Embed in Website
Add this to your website:
```html
<iframe src="https://bone-mineralization.streamlit.app" style="width:100%;height:800px;"></iframe>
```

### Share on Social Media
```
🦴 Try my Bone Mineralization Simulator!
No installation needed - runs in browser:
https://bone-mineralization.streamlit.app

Based on: Poorhemati & Komarova (2024)
```

## Troubleshooting

### App doesn't deploy
**Problem:** Deployment fails
**Solution:** 
- Check `requirements.txt` is in root directory
- Verify `app_single.py` filename is correct
- Check GitHub shows all files uploaded

### App runs slowly
**Problem:** Takes a long time to load
**Solution:**
- Streamlit Cloud instances are small
- First load takes ~30 seconds (normal)
- Subsequent loads are faster

### Port or permission errors
**Problem:** Error about ports or permissions
**Solution:**
- Make sure you're using relative paths in code
- Don't hardcode port numbers
- No file writing outside temp directory

### Missing module errors
**Problem:** "ModuleNotFoundError"
**Solution:**
- Add missing package to `requirements.txt`
- Redeploy (automatically reinstalls)

## Make Changes After Deployment

### Update Your App

1. **Make changes locally:**
```bash
# Edit app_single.py or bone_mineralization.py
# Test locally: streamlit run app_single.py
```

2. **Push to GitHub:**
```bash
git add .
git commit -m "Updated: [describe changes]"
git push
```

3. **Streamlit Cloud automatically redeploys!**
   - Usually deploys within 1 minute
   - No manual action needed

## Advanced: Custom Domain

(Optional - requires Streamlit Pro)

If you have a custom domain, you can:
1. Set up CNAME records to point to Streamlit
2. Configure in Streamlit Cloud settings
3. Access at your custom URL

## Monitoring & Analytics

In Streamlit Cloud dashboard, you can see:
- App view count
- User activity
- Performance metrics
- Error logs

## File Structure for Deployment

```
bone_mineralization_python/
├── app_single.py              ← Main app (required)
├── bone_mineralization.py     ← Library (required)
├── requirements.txt           ← Dependencies (required)
├── .gitignore                ← Git ignore
├── .streamlit/
│   ├── config.toml           ← Streamlit config
│   └── secrets.toml          ← (Optional) API keys
├── README.md                 ← Documentation
├── GitHub_README.md          ← GitHub docs
├── DEPLOY_TO_STREAMLIT_CLOUD.md  ← This file
└── other_docs/
    ├── FEATURES_COMPLETE.md
    ├── SINGLE_PAGE_LAYOUT.md
    └── ...
```

## Example: Complete Deployment

```bash
# 1. Create repo on GitHub (already done)

# 2. Clone to local machine
git clone https://github.com/yourusername/bone_mineralization_python.git
cd bone_mineralization_python

# 3. Add project files (already done)
# (all files already in /Users/hosseinp/bone)

# 4. Initialize git
git init
git add .
git commit -m "Initial commit: Full bone mineralization app"

# 5. Add remote
git remote add origin https://github.com/yourusername/bone_mineralization_python.git
git branch -M main
git push -u origin main

# 6. Go to share.streamlit.io
# Click "New app" → Select repo → `app_single.py` → Deploy

# 7. Share the URL!
# https://bone-mineralization.streamlit.app
```

## Cost

Streamlit Cloud is **completely free** for public apps!

- ✅ Free deployments
- ✅ Free hosting (up to 3 apps)
- ✅ Unlimited viewers
- ✅ Automatic scaling

## Security Note

Since this is a public app:
- ✅ No sensitive data is stored
- ✅ No user data is collected
- ✅ All computation is done client-side
- ✅ Safe for public use

## Next Steps

1. **Deploy now** using this guide (10 minutes)
2. **Share the URL** with collaborators
3. **Get feedback** on usability
4. **Make improvements** based on feedback
5. **Iterate** - each push automatically redeploys

## Need Help?

### Streamlit Documentation
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Community Forum](https://discuss.streamlit.io)

### GitHub Help
- [GitHub Docs](https://docs.github.com)
- [GitHub Community](https://github.community)

### This Project
- Check GitHub Issues
- Email: hossein.poorhemati@mail.mcgill.ca

## Summary

✅ You now have:
- Public, shareable app
- Automatic updates from GitHub
- Zero cost
- No server management
- Accessible worldwide

🎉 **Deploy now and share with the world!**

---

**Estimated Time:** 10-15 minutes
**Difficulty:** ⭐⭐ (Easy)
**Cost:** Free
**Result:** Production-ready web app
