# 🎙️ Voice Agent Testing Guide

## 🚀 **Quick Start**

### **Option 1: Automated Start (Easiest)**
1. Double-click `START_ALL.bat`
2. Three windows will open showing logs
3. Wait 10 seconds for everything to start
4. Go to Step 3 below

### **Option 2: Manual Start**

Open 3 separate command prompts:

**Terminal 1 - Backend API:**
```bash
cd C:\Users\lyndo\Documents\src\cerebras-hackathon-prep\rapidolingo\backend
python main.py
```

**Terminal 2 - LiveKit Agent Worker:**
```bash
cd C:\Users\lyndo\Documents\src\cerebras-hackathon-prep\rapidolingo\backend
python simple_agent.py dev
```

**Terminal 3 - Frontend:**
```bash
cd C:\Users\lyndo\Documents\src\cerebras-hackathon-prep\rapidolingo\frontend
npm run dev
```

---

## 🧪 **Step 3: Test the Voice Agent**

### **1. Open the App**
- Navigate to: http://localhost:3000

### **2. Sign In**
- Use your existing account or create new one

### **3. Complete Onboarding** (if new user)
- Enter your name
- Select Spanish level
- Choose learning goal

### **4. Go to Dashboard**
- You should see 8 lesson cards

### **5. Start Restaurant Lesson**
- Click the "Restaurant Conversation" card
- Click "Start Lesson"

### **6. Allow Microphone**
- Browser will ask for microphone permission
- Click "Allow"

### **7. Wait for Connection**
- You'll see "Connecting to your tutor..."
- Then the voice interface will load
- You should see voice visualizer bars

### **8. Listen for Greeting**
- The agent (María) should say:
  - "¡Hola! Welcome to our restaurant. I'm María, your server. What can I get for you today?"

### **9. Speak Spanish!**
- Try saying: "Hola, quiero una pizza"
- Or: "Hello, I want to order food"
- The agent should respond in a mix of Spanish and English

---

## ✅ **What Should Happen**

### **Agent Worker Window:**
You should see logs like:
```
[WORKER] Starting LiveKit agent worker...
[WORKER] This will connect to LiveKit Cloud and wait for rooms
[INFO] Configuration loaded successfully
[INFO] Cerebras API Key: csk-...
[INFO] Cartesia API Key: sk_car_...
[INFO] LiveKit URL: wss://wemakedevshackathontest-...
[AGENT] Starting agent for room: rapidolingo_restaurant_...
[AGENT] Connected to room: rapidolingo_restaurant_...
[AGENT] Voice assistant created successfully
[AGENT] Assistant started and listening...
[AGENT] Greeting sent
```

### **Frontend:**
- Voice visualizer animates
- Response time shows "<100ms"
- Audio plays through speakers
- You can speak and agent responds

---

## ⚠️ **Troubleshooting**

### **Problem: "Module not found" error in frontend**
**Solution:**
```bash
cd frontend
npm install @livekit/components-react @livekit/components-styles
rm -rf .next
npm run dev
```

### **Problem: Agent doesn't connect**
**Check:**
1. Is agent worker window showing "Connected to room"?
2. Is backend API running (http://localhost:8000)?
3. Are all API keys set in config.py?

**Solution:**
```bash
cd backend
# Check config.py has all keys
python -c "import config; print('Config OK')"
```

### **Problem: No audio/voice**
**Check:**
1. Microphone permission granted?
2. Speakers/headphones connected?
3. Agent worker showing greeting sent?

**Try:**
- Refresh the page
- Try different browser (Chrome works best)
- Check browser console for errors (F12)

### **Problem: Agent says "mock_token_for_mvp"**
**This means LiveKit credentials aren't loading.**

**Solution:**
```bash
cd backend
# Make sure config.py exists and has:
# - LIVEKIT_URL
# - LIVEKIT_API_KEY
# - LIVEKIT_API_SECRET
```

---

## 🎯 **Success Criteria**

You know it's working when:
- ✅ Agent worker shows "Assistant started and listening"
- ✅ You hear María say the greeting
- ✅ Voice visualizer responds to your speech
- ✅ Agent responds to your Spanish/English
- ✅ Conversation feels natural (<100ms latency)

---

## 📝 **What to Show in Demo**

Once working, demonstrate:
1. **Full user flow** - signup to conversation
2. **Voice interaction** - actual Spanish conversation
3. **Response speed** - point out <100ms metric
4. **Natural dialogue** - agent teaching Spanish naturally
5. **Code architecture** - show simple_agent.py

---

## 🐛 **Common Issues**

### **Error: "CEREBRAS_API_KEY not set"**
- Check config.py exists in backend/
- Check CEREBRAS_API_KEY is defined
- Try: `python -c "import os; print(os.getenv('CEREBRAS_API_KEY'))"`

### **Error: "CARTESIA_API_KEY not set"**
- Same as above for CARTESIA_API_KEY

### **Frontend stuck on "Connecting to your tutor..."**
- Check backend logs for errors
- Check Network tab in browser (F12 → Network)
- Make sure POST to /api/session/start succeeded

### **Agent connects but no voice**
- Check agent worker logs for errors
- Try saying something - it takes 2-3 seconds first time
- Check if Cartesia TTS/STT initialized properly

---

## 📊 **Monitoring**

### **Backend API (Terminal 1):**
Look for:
- `POST /api/session/start 200` (session created)
- No 500 errors

### **Agent Worker (Terminal 2):**
Look for:
- `[AGENT] Starting agent for room: rapidolingo_...`
- `[AGENT] Connected to room`
- `[AGENT] Assistant started and listening`
- `[AGENT] Greeting sent`

### **Frontend (Terminal 3):**
Look for:
- `✓ Compiled /tutoring in X ms`
- No "Module not found" errors
- No Clerk errors

---

## 🎬 **Recording the Demo**

Once it works:
1. **Screen record** the full interaction
2. **Show your face** if possible (builds trust)
3. **Narrate** what you're doing
4. **Point out** the <100ms response time
5. **Explain** the Cerebras integration
6. **Show code** briefly (agents, backend API)

---

## 🚨 **If Nothing Works**

**Fallback Plan:**
1. Demo the UI without voice
2. Show the code architecture
3. Explain what WOULD happen
4. Show agent worker connecting (logs)
5. Emphasize the Cerebras <100ms advantage

**The architecture and code quality are impressive even without live voice!**

---

## 💪 **You Got This!**

Remember:
- This is ambitious (voice + AI + real-time)
- The attempt shows skill
- The architecture alone is hackathon-worthy
- Even partial success is impressive

**Good luck! 🚀**

