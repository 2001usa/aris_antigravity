# 🛑 Botni To'xtatish

## Lokal Bot (Kompyuterda)

Agar `python bot.py` bilan ishga tushirgan bo'lsangiz:

**Windows (CMD/PowerShell):**
```
Ctrl + C
```

**Yoki process'ni topib o'chirish:**
```powershell
# Bot process'ni topish
Get-Process python

# O'chirish (PID ni almashtiring)
Stop-Process -Id PID_NUMBER
```

---

## Railway'dagi Bot

### Vaqtinchalik To'xtatish

1. **Railway Dashboard** ga kiring
2. Project'ni oching
3. **Settings** tab
4. **"Pause Deployment"** yoki **"Stop"** tugmasini bosing

### Butunlay O'chirish

1. Railway Dashboard
2. Project Settings
3. **"Delete Service"** yoki **"Delete Project"**

### Restart (Qayta Ishga Tushirish)

1. Railway Dashboard
2. **Deployments** tab
3. **"Restart"** tugmasini bosing

---

## Render'dagi Bot

1. Render Dashboard
2. Service'ni tanlang
3. **"Suspend"** tugmasini bosing

---

## VPS'dagi Bot

```bash
# Service'ni to'xtatish
sudo systemctl stop aris-bot

# O'chirish (avtomatik ishga tushmaydi)
sudo systemctl disable aris-bot

# Status tekshirish
sudo systemctl status aris-bot
```

---

Qaysi botni to'xtatmoqchisiz?
