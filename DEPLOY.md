# 🚀 GitHub va Railway Deploy Qo'llanmasi

## 📋 Bosqichlar

### 1️⃣ GitHub Repository Yaratish

#### GitHub'da Repository Yaratish

1. [github.com](https://github.com) ga kiring
2. "+" → "New repository" bosing
3. Repository nomi: `aris-finance-bot`
4. Description: "Shaxsiy moliyaviy yordamchi Telegram bot"
5. Public yoki Private tanlang
6. "Create repository" bosing

#### Loyihani GitHub'ga Yuklash

```bash
# Loyiha papkasiga o'ting
cd C:\Users\user\Desktop\Aris_antigravity

# Git init (agar bo'lmasa)
git init

# .gitignore tekshirish (mavjud)
# .env, database/, venv/ ignore qilingan

# Fayllarni qo'shish
git add .

# Commit
git commit -m "Initial commit - ARIS Finance Bot v2.0"

# Remote qo'shish (YOUR_USERNAME ni o'zgartiring)
git remote add origin https://github.com/YOUR_USERNAME/aris-finance-bot.git

# Push
git branch -M main
git push -u origin main
```

**Muhim:** `.env` fayl GitHub'ga yuklanmaydi (`.gitignore` da)

---

### 2️⃣ Railway Deploy

#### Railway Account

1. [railway.app](https://railway.app) ga kiring
2. "Login with GitHub" bosing
3. GitHub account ulang

#### Yangi Project Yaratish

1. Dashboard'da "New Project" bosing
2. "Deploy from GitHub repo" tanlang
3. `aris-finance-bot` repository ni tanlang
4. Railway avtomatik deploy boshlaydi

#### Environment Variables Sozlash

1. Project Settings → Variables
2. Quyidagi o'zgaruvchilarni qo'shing:

```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GROQ_API_KEY_1=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY_2=gsk_yyyyyyyyyyyyyyyyyyyyyyyy
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_PATH=database/aris.db
```

3. "Add" bosing

#### Deploy Sozlamalari

**Settings → Deploy:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `python bot.py`
- Auto-deploy: ✅ Enabled

**Settings → Environment:**
- Python Version: 3.11.9 (avtomatik)

#### Deploy Monitoring

1. "Deployments" tab'ga o'ting
2. Loglarni ko'ring:
   ```
   Building...
   Installing dependencies...
   Starting bot...
   INFO:aiogram:Bot started
   ```

3. Muvaffaqiyatli bo'lsa: ✅ "Success"

---

### 3️⃣ Render Deploy (Alternativ)

#### Render Account

1. [render.com](https://render.com) ga kiring
2. GitHub bilan kirish

#### Web Service Yaratish

1. "New +" → "Web Service"
2. GitHub repository ulang
3. Sozlamalar:
   - Name: `aris-finance-bot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Instance Type: `Free`

#### Environment Variables

Settings → Environment:
```
BOT_TOKEN=...
GROQ_API_KEY_1=...
GROQ_API_KEY_2=...
GEMINI_API_KEY=...
DATABASE_PATH=database/aris.db
```

#### Deploy

1. "Create Web Service" bosing
2. Deploy jarayonini kuzating
3. Logs'da "Bot started" ko'ring

---

### 4️⃣ VPS Deploy (Ubuntu)

#### Server Tayyorlash

```bash
# SSH orqali serverga kirish
ssh user@your-server-ip

# Yangilash
sudo apt update && sudo apt upgrade -y

# Python 3.11 o'rnatish
sudo apt install python3.11 python3.11-venv git -y
```

#### Loyihani Yuklash

```bash
# Home directory
cd ~

# Git clone
git clone https://github.com/YOUR_USERNAME/aris-finance-bot.git
cd aris-finance-bot

# Virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Kutubxonalar
pip install -r requirements.txt
```

#### .env Yaratish

```bash
nano .env
```

Quyidagilarni kiriting:
```env
BOT_TOKEN=...
GROQ_API_KEY_1=...
GROQ_API_KEY_2=...
GEMINI_API_KEY=...
DATABASE_PATH=database/aris.db
```

Saqlash: `Ctrl+X`, `Y`, `Enter`

#### Systemd Service

```bash
sudo nano /etc/systemd/system/aris-bot.service
```

Fayl mazmuni:
```ini
[Unit]
Description=ARIS Finance Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/aris-finance-bot
Environment="PATH=/home/YOUR_USERNAME/aris-finance-bot/venv/bin"
ExecStart=/home/YOUR_USERNAME/aris-finance-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**YOUR_USERNAME ni o'zgartiring!**

#### Service Ishga Tushirish

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (avtomatik start)
sudo systemctl enable aris-bot

# Start
sudo systemctl start aris-bot

# Status
sudo systemctl status aris-bot
```

Muvaffaqiyatli bo'lsa:
```
● aris-bot.service - ARIS Finance Bot
   Active: active (running)
```

#### Loglarni Ko'rish

```bash
# Real-time logs
sudo journalctl -u aris-bot -f

# Oxirgi 100 qator
sudo journalctl -u aris-bot -n 100
```

#### Yangilash

```bash
cd ~/aris-finance-bot
git pull
sudo systemctl restart aris-bot
```

---

## 🔧 Muammolarni Hal Qilish

### Railway

**Deploy Failed:**
1. Logs'ni tekshiring
2. `requirements.txt` to'g'riligini tekshiring
3. Environment variables to'liqligini tekshiring

**Bot ishlamayapti:**
1. Variables'da `BOT_TOKEN` borligini tekshiring
2. Logs'da xatolarni ko'ring
3. Redeploy qiling

### Render

**Build Failed:**
1. Python versiyasini tekshiring (3.11+)
2. Dependencies'ni tekshiring
3. Logs'ni o'qing

**Database xatosi:**
1. `DATABASE_PATH` to'g'riligini tekshiring
2. Yozish huquqlari borligini tekshiring

### VPS

**Service ishlamayapti:**
```bash
# Status
sudo systemctl status aris-bot

# Restart
sudo systemctl restart aris-bot

# Logs
sudo journalctl -u aris-bot -n 50
```

**Port band:**
```bash
# Ishlab turgan botlarni topish
ps aux | grep bot.py

# O'chirish
kill PID_NUMBER
```

---

## 📊 Monitoring

### Railway

- Dashboard → Metrics
- CPU, Memory, Network ko'rish
- Logs real-time

### Render

- Dashboard → Logs
- Metrics tab
- Health checks

### VPS

```bash
# CPU va Memory
htop

# Disk
df -h

# Bot status
sudo systemctl status aris-bot
```

---

## 🔄 Yangilash

### Railway/Render

1. GitHub'ga push qiling:
   ```bash
   git add .
   git commit -m "Update"
   git push
   ```

2. Avtomatik deploy (agar yoqilgan bo'lsa)
3. Yoki manual deploy bosing

### VPS

```bash
cd ~/aris-finance-bot
git pull
sudo systemctl restart aris-bot
```

---

## 💡 Maslahatlar

1. **Backup:** Database'ni muntazam backup qiling
2. **Monitoring:** Uptime monitoring sozlang
3. **Logs:** Loglarni saqlang va tahlil qiling
4. **Security:** API kalitlarni xavfsiz saqlang
5. **Updates:** Botni muntazam yangilang

---

**Muvaffaqiyatli Deploy!** 🎉
