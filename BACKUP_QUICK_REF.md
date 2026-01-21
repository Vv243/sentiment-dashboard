# Quick Reference - Backup System

## 🚀 Quick Commands

### Generate Demo Data
```bash
# Basic - balanced sentiment
curl -X POST "http://localhost:8000/api/v1/collection/generate-demo-data/TSLA"

# Bullish market (70% positive)
curl -X POST "http://localhost:8000/api/v1/collection/generate-demo-data/TSLA?scenario=bullish"

# Bearish market (70% negative)
curl -X POST "http://localhost:8000/api/v1/collection/generate-demo-data/TSLA?scenario=bearish"

# Custom count
curl -X POST "http://localhost:8000/api/v1/collection/generate-demo-data/TSLA?count=200"
```

### Collect with Auto-Fallback
```bash
# Tries Reddit → Twitter → Synthetic
curl -X POST "http://localhost:8000/api/v1/collection/collect-now/TSLA"

# Disable fallback (real data only)
curl -X POST "http://localhost:8000/api/v1/collection/collect-now/TSLA?use_synthetic_fallback=false"
```

### Test Backup System
```bash
cd backend
python test_backup_system.py
```

---

## 📊 Market Scenarios

| Scenario | Positive | Negative | Neutral | Use Case |
|----------|----------|----------|---------|----------|
| `balanced` | 35% | 35% | 30% | Normal market |
| `bullish` | 70% | 10% | 20% | Strong uptrend |
| `bearish` | 10% | 70% | 20% | Downtrend |
| `volatile` | 40% | 40% | 20% | Mixed opinions |
| `stable` | 30% | 30% | 40% | Low activity |

---

## 🎬 Pre-Demo Setup (5 minutes)

```bash
# 1. Generate data for popular tickers
for ticker in TSLA AAPL NVDA AMD MSFT GME; do
  curl -X POST "http://localhost:8000/api/v1/collection/generate-demo-data/$ticker?count=100"
done

# 2. Verify data exists
curl "http://localhost:8000/api/v1/sentiment/TSLA"

# 3. Check trending
curl "http://localhost:8000/api/v1/collection/trending"

# 4. Ready for demo! Open http://localhost:3000
```

---

## 🔧 Configuration

### Backend `.env`
```env
# Enable synthetic fallback (default: true)
USE_SYNTHETIC_FALLBACK=true
```

### Customize Templates
Edit: `backend/app/services/synthetic_data.py`

```python
POSITIVE_TEMPLATES = [
    "Add your own templates for {ticker} here",
    # ...
]
```

---

## ✅ Verification Checklist

- [ ] Backend running: `http://localhost:8000/docs`
- [ ] Generate test data: `curl -X POST .../generate-demo-data/TEST`
- [ ] Check data saved: `curl http://localhost:8000/api/v1/sentiment/TEST`
- [ ] Frontend displays: `http://localhost:3000`
- [ ] Source indicator shows "synthetic" when using demo data

---

## 🎯 When to Use What

| Situation | Command | Why |
|-----------|---------|-----|
| Normal use | `collect-now` | Auto-fallback handles everything |
| Demo prep | `generate-demo-data` | Consistent, controlled data |
| Testing | `generate-demo-data?scenario=X` | Test different conditions |
| Development | `generate-demo-data` | No API keys needed |
| Production | `collect-now` with Reddit creds | Real data preferred |

---

## 🐛 Troubleshooting

**"No module named 'app'"**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**"Synthetic data not working"**
```bash
# Test the generator
python test_backup_system.py
```

**"Data not appearing in dashboard"**
```bash
# Check if data was saved
curl "http://localhost:8000/api/v1/sentiment/TICKER"

# Check MongoDB
mongosh sentiment_db
db.sentiment_records.countDocuments()
```

---

## 💡 Pro Tips

1. **Always generate demo data before interviews** - ensures consistency
2. **Use different scenarios** - shows you handle edge cases
3. **Mention it in interviews** - "intelligent fallback system"
4. **Keep it transparent** - label synthetic data in UI
5. **Test both modes** - real and synthetic

---

## 📱 Quick Test

```python
# Python quick test
import requests

# Generate data
r = requests.post("http://localhost:8000/api/v1/collection/generate-demo-data/TSLA")
print(r.json())

# Get sentiment
r = requests.get("http://localhost:8000/api/v1/sentiment/TSLA")
print(r.json()['current_sentiment']['label'])
```

---

## 📞 Need Help?

- Check: `BACKUP_PLAN.md` (full documentation)
- Run: `python test_backup_system.py` (tests)
- API Docs: `http://localhost:8000/docs`

---

**Remember**: Your app ALWAYS works, even without API credentials! 🎉
