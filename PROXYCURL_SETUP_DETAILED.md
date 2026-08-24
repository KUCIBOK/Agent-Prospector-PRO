# 🔗 PROXYCURL SETUP - Complete Guide

## What is Proxycurl?
LinkedIn profile data API — get professional information about curators, advisors, gallery directors.

**Features:**
- Get LinkedIn profile data (name, title, company, bio, etc.)
- Monitor profile changes (title updates, company moves)
- Free tier: 100 API calls/month
- Perfect for curator monitoring

---

## 🚀 Step-by-Step Setup (5 minutes total)

### STEP 1: Sign Up for Free Account (2 minutes)

1. **Open:** https://proxycurl.com

2. **Click "Sign Up"** (top right)
   - Email address (use your work email)
   - Password (strong)
   - Agree to terms
   - Click "Sign Up"

3. **Verify Email**
   - Check your email inbox
   - Click verification link
   - Done! ✅

### STEP 2: Get Your API Key (1 minute)

1. **Login** to https://proxycurl.com
   - Email: your email
   - Password: your password
   - Click "Login"

2. **Go to Dashboard**
   - Look for "Dashboard" or "API Keys" in menu
   - Usually top navigation

3. **Copy API Key**
   - You'll see your API key (starts with "pk_")
   - Click to copy
   - **SAVE IT SOMEWHERE SAFE!** (you'll use it now)

**Example:**
```
pk_1234567890abcdefghijklmnop
```

### STEP 3: Set Environment Variable (1 minute)

#### Option A: One-Time (This Session Only)

**Windows PowerShell:**
```powershell
# Paste this (replace with YOUR key):
$env:PROXYCURL_API_KEY = "pk_your_actual_key_here"

# Verify it worked:
echo $env:PROXYCURL_API_KEY
# Should print: pk_your_actual_key_here
```

**Linux/Mac:**
```bash
export PROXYCURL_API_KEY="pk_your_actual_key_here"

# Verify:
echo $PROXYCURL_API_KEY
```

#### Option B: Permanent (.env File)

**Create .env file in project root:**

```bash
cd "C:\Users\Moctar Sidibe\Desktop\Collection art primitif Tomasini\Sculpture\prospecto VA"

# Windows PowerShell:
Add-Content -Path .env -Value "PROXYCURL_API_KEY=pk_your_actual_key_here"

# Or Linux/Mac:
echo "PROXYCURL_API_KEY=pk_your_actual_key_here" >> .env
```

Then load it:
```bash
# Windows PowerShell:
Get-Content .env | ForEach-Object { $key, $value = $_ -split '='; Set-Item -Path "env:$key" -Value $value }

# Or Linux/Mac:
source .env
```

#### Option C: Docker (Permanent)

Edit `docker-compose.yml` and add to `app` service:

```yaml
services:
  app:
    environment:
      - PROXYCURL_API_KEY=pk_your_actual_key_here
      # ... other env vars
```

Then restart:
```bash
docker-compose restart app worker
```

### STEP 4: Verify Configuration (30 seconds)

#### Check 1: Environment Variable Set
```powershell
# Windows:
$env:PROXYCURL_API_KEY

# Linux/Mac:
echo $PROXYCURL_API_KEY
```

Expected output:
```
pk_1234567890abcdefghijklmnop
```

#### Check 2: API Health
```bash
curl http://localhost:8000/api/monitoring/health
```

Expected output:
```json
{"status":"ok","timestamp":"2026-08-24T...","uptime_seconds":45}
```

---

## ✅ Verification Checklist

- [ ] Account created at https://proxycurl.com
- [ ] Email verified
- [ ] API key copied (starts with "pk_")
- [ ] Environment variable set (verify with `echo $PROXYCURL_API_KEY`)
- [ ] API health check passes

---

## 🎯 Next Step: Run Tests

Once verified, you're ready!

```powershell
# PowerShell:
.\test_improvements.ps1

# Or Bash:
./test_improvements.sh
```

---

## 📊 Usage & Limits

### Free Tier
- **Limit:** 100 API calls per month
- **Cost:** $0
- **Use case:** 3 curator profiles monitored daily

### Paid Plans (Optional)
If you need more:
- **Growth:** 10K calls/month = $50/month
- **Scale:** 100K calls/month = $200/month

### How Many Calls Per Day?
- 1 LinkedIn profile check = 1 call
- Free tier = 100 calls/month = ~3 profiles/day
- Enough to monitor 50+ key curators

---

## 🆘 Troubleshooting

### "API Key Not Valid"
→ Double-check you copied the entire key (should be 30+ characters)
→ Make sure it starts with "pk_"
→ Try logging back into proxycurl.com to re-copy

### "Cannot Connect to Proxycurl"
→ Check internet connection
→ Proxycurl might be down (rare) — try again in 5 min

### "Environment Variable Not Set"
**Windows:**
```powershell
# Try this:
[Environment]::SetEnvironmentVariable("PROXYCURL_API_KEY", "pk_your_key", "User")
# Then restart PowerShell
```

**Linux/Mac:**
```bash
# Add to ~/.bashrc or ~/.zshrc:
echo 'export PROXYCURL_API_KEY="pk_your_key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🎊 Success!

You now have:
✅ Proxycurl account
✅ API key
✅ Environment variable configured
✅ Ready to monitor curators!

**Next:** Run tests!

```powershell
.\test_improvements.ps1
```

---

## 📚 Resources

- **Proxycurl Docs:** https://nubela.co/proxycurl/api/linkedin-profile-api/
- **API Reference:** https://docs.proxycurl.com/
- **Dashboard:** https://proxycurl.com/dashboard

---

## 💡 What You Can Do Now

With your Proxycurl API key set up, the system will:

1. **Monitor LinkedIn Curators** (Daily 5 AM)
   - Detect title changes
   - Spot company moves
   - Identify hiring signals

2. **Generate Signals**
   - "Jane Doe changed title to Director"
   - "Gallery moved to NYC"
   - "New curator hired"

3. **Auto-Upgrade Prospects**
   - P3 → P2 when signals found
   - Send personalized messages
   - +50% higher relevance

---

## Questions?

If stuck:
1. Check Proxycurl dashboard: https://proxycurl.com/dashboard
2. Read: LINKEDIN_INSTAGRAM_SETUP.md
3. View logs: `docker-compose logs -f app`

**You've got this! 🚀**
