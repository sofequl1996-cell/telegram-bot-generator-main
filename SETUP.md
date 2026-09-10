# 🚀 সম্পূর্ণ সেটআপ গাইড - শুরু থেকে শেষ পর্যন্ত

এই গাইডটি সম্পূর্ণভাবে নতুনদের জন্য লেখা। প্রতিটি ধাপ সহজভাবে ব্যাখ্যা করা হয়েছে।

---

## 📋 বিষয়বস্তু
1. [পূর্ব-প্রয়োজনীয়তা ইনস্টল করুন](#1-পূর্ব-প্রয়োজনীয়তা-ইনস্টল-করুন)
2. [প্রজেক্ট ডাউনলোড করুন](#2-প্রজেক্ট-ডাউনলোড-করুন)
3. [প্রজেক্ট ফোল্ডার খুলুন](#3-প্রজেক্ট-ফোল্ডার-খুলুন)
4. [এনভায়রনমেন্ট ফাইল সেটআপ করুন](#4-এনভায়রনমেন্ট-ফাইল-সেটআপ-করুন)
5. [ডাটাবেস সেটআপ করুন](#5-ডাটাবেস-সেটআপ-করুন)
6. [প্রজেক্ট চালান](#6-প্রজেক্ট-চালান)
7. [সবকিছু পরীক্ষা করুন](#7-সবকিছু-পরীক্ষা-করুন)

---

## 1️⃣ পূর্ব-প্রয়োজনীয়তা ইনস্টল করুন

আপনার কম্পিউটারে নিম্নলিখিত জিনিসগুলি ইনস্টল করতে হবে:

### ✅ Python ইনস্টল করুন (3.8 বা তার উপরে)

**Windows:**
1. https://www.python.org/ এ যান
2. "Download Python 3.11" বোতাম ক্লিক করুন
3. ইনস্টলার চালান
4. **গুরুত্বপূর্ণ:** "Add Python to PATH" চেক করুন
5. "Install Now" ক্লিক করুন
6. সম্পন্ন হওয়া পর্যন্ত অপেক্ষা করুন

**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

**যাচাই করুন:**
```bash
python --version
# অথবা
python3 --version
```

আপনি যদি একটি সংস্করণ নম্বর দেখেন (উদাহরণ: Python 3.11.0), তাহলে সফল! ✅

---

### ✅ Git ইনস্টল করুন

**Windows:**
1. https://git-scm.com/download/win এ যান
2. ডাউনলোড করুন এবং ইনস্টলার চালান
3. সব ডিফল্ট অপশন নিয়ে "Next" ক্লিক করুন

**Mac:**
```bash
brew install git
```

**Linux (Ubuntu):**
```bash
sudo apt-get install git
```

**যাচাই করুন:**
```bash
git --version
```

---

### ✅ PostgreSQL ইনস্টল করুন (ডাটাবেসের জন্য)

**Windows:**
1. https://www.postgresql.org/download/windows/ এ যান
2. সর্বশেষ সংস্করণ ডাউনলোড করুন
3. ইনস্টলার চালান
4. পাসওয়ার্ড মনে রাখুন (উদাহরণ: `postgres`)
5. পোর্ট `5432` রাখুন (ডিফল্ট)

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

---

### ✅ Visual Studio Code ইনস্টল করুন (কোড এডিটর)

1. https://code.visualstudio.com/ এ যান
2. আপনার অপারেটিং সিস্টেমের জন্য ডাউনলোড করুন
3. ইনস্টলার চালান

---

## 2️⃣ প্রজেক্ট ডাউনলোড করুন

### ধাপ A: GitHub থেকে ডাউনলোড করুন

একটি ফোল্ডার বেছে নিন যেখানে আপনি প্রজেক্ট রাখতে চান (উদাহরণ: `Desktop` বা `Documents`)

**Windows:**
1. কমান্ড প্রম্পট খুলুন (Win + R, টাইপ করুন `cmd`, এন্টার চাপুন)
2. নিম্নলিখিত কমান্ড টাইপ করুন:

```bash
cd Desktop
git clone https://github.com/sofequl1996-cell/telegram-bot-generator-main.git
cd telegram-bot-generator-main
```

**Mac/Linux:**
```bash
cd ~/Desktop
git clone https://github.com/sofequl1996-cell/telegram-bot-generator-main.git
cd telegram-bot-generator-main
```

**ব্যাখ্যা:**
- `cd Desktop` = Desktop এ যান
- `git clone ...` = প্রজেক্ট ডাউনলোড করুন
- `cd telegram-bot-...` = প্রজেক্ট ফোল্ডারে প্রবেশ করুন

---

## 3️⃣ প্রজেক্ট ফোল্ডার খুলুন

### Visual Studio Code দিয়ে খুলুন

**Windows:**
1. কমান্ড প্রম্পটে টাইপ করুন:
```bash
code .
```

**Mac/Linux:**
```bash
code .
```

**অথবা ম্যানুয়ালি:**
1. Visual Studio Code খুলুন
2. File → Open Folder
3. `telegram-bot-generator-main` ফোল্ডার নির্বাচন করুন

আপনি এখন প্রজেক্ট স্ট্রাকচার দেখতে পাবেন। 🎉

---

## 4️⃣ এনভায়রনমেন্ট ফাইল সেটআপ করুন

### কী হল এনভায়রনমেন্ট ফাইল?

এনভায়রনমেন্ট ফাইল (`.env`) একটি বিশেষ ফাইল যেখানে আপনার গোপনীয় তথ্য রাখা হয়, যেমন:
- Telegram বট টোকেন
- ডাটাবেস পাসওয়ার্ড
- ইমেইল পাসওয়ার্ড
- ইত্যাদি

### ধাপ ১: প্রজেক্টে `.env` ফাইল তৈরি করুন

**VS Code এ:**
1. প্রজেক্ট রুটে ডান ক্লিক করুন
2. "New File" ক্লিক করুন
3. নাম দিন: `.env`
4. এন্টার চাপুন

### ধাপ ২: `.env` ফাইলে নিম্নলিখিত কন্টেন্ট যোগ করুন

```env
# 🤖 TELEGRAM BOT সেটিংস
TELEGRAM_BOT_TOKEN=আপনার_বট_টোকেন_এখানে
# বট টোকেন পেতে: @BotFather কে Telegram এ মেসেজ করুন

# 💾 DATABASE সেটিংস
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/telegram_bot_db
# ব্যাখ্যা:
# postgres = ইউজারনেম
# postgres = পাসওয়ার্ড
# localhost:5432 = সার্ভার ঠিকানা
# telegram_bot_db = ডাটাবেস নাম

# 📧 EMAIL সেটিংস (Gmail ব্যবহার করছেন?)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
# নোট: পাসওয়ার্ড নয়, App Password ব্যবহার করুন
# যাবেন: https://myaccount.google.com/apppasswords

# 🎛️ ADMIN PANEL সেটিংস
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=pbkdf2:sha256$...  # ডিফল্ট পাসওয়ার্ড: admin123
API_TOKEN=your_secure_api_token_here

# 🔧 APPLICATION সেটিংস
DEBUG=True          # উন্নয়নের সময় True রাখুন
ENVIRONMENT=development
SECRET_KEY=your_secret_key_12345

# 🔌 DATABASE নির্বাচন (বিকাশের জন্য SQLite ব্যবহার করতে পারেন)
# DATABASE_URL=sqlite:///./bot.db
```

### ধাপ ৩: গোপনীয় তথ্য যোগ করুন

#### Telegram বট টোকেন পান:
1. Telegram খুলুন
2. `@BotFather` অনুসন্ধান করুন
3. `/newbot` টাইপ করুন এবং অনুসরণ করুন
4. আপনি একটি টোকেন পাবেন, এটি `.env` এ যোগ করুন

#### Gmail App Password পান:
1. https://myaccount.google.com/ এ যান
2. "Security" ক্লিক করুন
3. "App passwords" খুঁজুন
4. একটি নতুন App password তৈরি করুন
5. `.env` এ যোগ করুন

---

## 5️⃣ ডাটাবেস সেটআপ করুন

### ধাপ ১: PostgreSQL চালু করুন

**Windows:**
1. Services এ PostgreSQL চালু আছে কিনা চেক করুন
2. বা: "SQL Shell (psql)" খুলুন

**Mac:**
```bash
brew services start postgresql
```

**Linux:**
```bash
sudo service postgresql start
```

### ধাপ ২: ডাটাবেস তৈরি করুন

**Windows (SQL Shell খুলুন):**
```sql
CREATE DATABASE telegram_bot_db;
```

**Mac/Linux (Terminal):**
```bash
psql -U postgres -c "CREATE DATABASE telegram_bot_db;"
```

### ধাপ ৩: Python ডিপেন্ডেন্সি ইনস্টল করুন

VS Code Terminal খুলুন (Ctrl + ` অথবা View → Terminal):

```bash
# সবার জন্য একই কমান্ড
pip install -r requirements.txt
```

এটি সব প্রয়োজনীয় Python লাইব্রেরি ইনস্টল করবে।

### ধাপ ৪: ডাটাবেস ইনিশিয়ালাইজ করুন

Terminal এ:

```bash
python -c "from database.db import init_db; init_db()"
```

অথবা:

```bash
python
```

তারপর:

```python
from database.db import init_db
init_db()
exit()
```

**সফল হলে:** কোনো ত্রুটি দেখা যাবে না। ✅

---

## 6️⃣ প্রজেক্ট চালান

### শুরু করুন - বট চালান

**Terminal ১ খুলুন (Bot চালানোর জন্য):**

```bash
python bot/main.py
```

**আশা করুন:** বার্তা যেমন: `Bot started successfully!`

ধাপে ধাপে কী ঘটছে:
1. Python `bot/main.py` ফাইল চালায়
2. বট Telegram সার্ভারের সাথে সংযোগ করে
3. বট এখন আপনার কমান্ড শোনার জন্য প্রস্তুত

### শুরু করুন - Admin Panel চালান

**একটি নতুন Terminal ২ খুলুন:**

```bash
python admin/app.py
```

**আশা করুন:** বার্তা যেমন:
```
 * Running on http://127.0.0.1:5000
```

---

## 7️⃣ সবকিছু পরীক্ষা করুন

### 🤖 Telegram বট পরীক্ষা করুন

1. Telegram খুলুন
2. আপনার বটকে খুঁজুন (বট নাম: আপনি BotFather এ যা রেখেছেন)
3. `/start` লিখুন এবং পাঠান
4. আপনি একটি স্বাগত বার্তা পাবেন ✅

**সব কমান্ড:**
- `/start` - বট শুরু করুন
- `/help` - সাহায্য পান
- `/account` - অ্যাকাউন্ট তৈরি করুন
- `/status` - অবস্থা দেখুন

### 🎛️ Admin Panel পরীক্ষা করুন

1. ওয়েব ব্রাউজার খুলুন
2. যান: `http://localhost:5000`
3. লগইন করুন:
   - **Username:** `admin`
   - **Password:** `admin123`

4. ড্যাশবোর্ডে নিম্নলিখিত দেখতে পাবেন:
   - 📊 ইউজার সংখ্যা
   - 📧 ডেমো ইমেইল (20টি)
   - 💾 ডাটাবেস তথ্য

---

## 🆘 সমস্যা সমাধান

### ❌ সমস্যা: "No module named 'telegram'"

**সমাধান:**
```bash
pip install python-telegram-bot
```

### ❌ সমস্যা: "Connection refused" ডাটাবেসের জন্য

**সমাধান:**
1. PostgreSQL চালু আছে কিনা চেক করুন
2. `.env` এ DATABASE_URL সঠিক কিনা চেক করুন
3. বিকাশের জন্য SQLite ব্যবহার করুন:

```env
DATABASE_URL=sqlite:///./bot.db
```

### ❌ সমস্যা: "Error 404" Admin Panel এ

**সমাধান:**
1. Admin Panel সার্ভার চলছে কিনা চেক করুন
2. Terminal এ কোনো ত্রুটি আছে কিনা দেখুন
3. পুনরায় চালান: `python admin/app.py`

### ❌ সমস্যা: বট সাড়া দিচ্ছে না

**সমাধান:**
1. TELEGRAM_BOT_TOKEN সঠিক কিনা চেক করুন
2. ইন্টারনেট সংযোগ চেক করুন
3. Terminal এ ত্রুটি বার্তা দেখুন
4. বট পুনরায় চালান: `python bot/main.py`

---

## 📁 প্রজেক্ট ফোল্ডার গঠন ব্যাখ্যা

```
telegram-bot-generator-main/
│
├── bot/                    # 🤖 Telegram বট কোড
│   ├── main.py            # বট শুরু করার স্ক্রিপ্ট
│   ├── handlers.py        # কমান্ড হ্যান্ডলার
│   └── keyboards.py       # বাটন এবং মেনু
│
├── database/              # 💾 ডাটাবেস সেটআপ
│   ├── db.py             # ডাটাবেস কানেকশন
│   └── models.py         # ডাটা স্ট্রাকচার
│
├── services/              # 🔧 কার্যকারিতা
│   ├── user_manager.py   # ইউজার ব্যবস্থাপনা
│   ├── account_generator.py  # ইমেইল জেনারেটর
│   └── email_service.py  # ইমেইল পাঠানো
│
├── admin/                 # 🎛️ Admin প্যানেল (ওয়েব)
│   ├── app.py            # Admin ওয়েব সার্ভার
│   ├── auth.py           # লগইন সিস্টেম
│   └── templates/        # HTML পেজ
│
├── .env                   # 🔐 আপনার গোপনীয় তথ্য
├── requirements.txt       # 📦 প্রয়োজনীয় লাইব্রেরি
├── config.py             # ⚙️ সেটিংস
└── README.md             # 📖 ডকুমেন্টেশন
```

---

## 🎯 পরবর্তী পদক্ষেপ

### এখন আপনি যা করতে পারেন:

1. **বট কাস্টমাইজ করুন:**
   - `bot/handlers.py` সম্পাদনা করুন
   - নতুন কমান্ড যোগ করুন
   - বার্তা পরিবর্তন করুন

2. **ডাটাবেস ব্যবহার করুন:**
   - ইউজার ডেটা সংরক্ষণ করুন
   - অ্যাকাউন্ট তৈরি করুন
   - লগ রেকর্ড করুন

3. **ইমেইল পাঠান:**
   - স্বয়ংক্রিয় যাচাইকরণ ইমেইল
   - ব্যবহারকারীদের বিজ্ঞপ্তি পাঠান

4. **Admin Panel আপগ্রেড করুন:**
   - নতুন পেজ যোগ করুন
   - বৈশিষ্ট্য যোগ করুন
   - ডিজাইন উন্নত করুন

---

## 📚 দরকারী সংস্থান

- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Python ডকুমেন্টেশন:** https://docs.python.org/3/
- **Flask (Web):** https://flask.palletsprojects.com/
- **SQLAlchemy (ডাটাবেস):** https://www.sqlalchemy.org/

---

## 💡 টিপস এবং কৌশল

### ডিবাগিং মোড চালু করুন
```bash
export DEBUG=True  # Mac/Linux
set DEBUG=True     # Windows
```

### Terminal এ ডাটাবেস দেখুন
```bash
psql -U postgres -d telegram_bot_db
\dt  # সব টেবিল দেখুন
SELECT * FROM users;  # ইউজার দেখুন
\q  # বেরিয়ে আসুন
```

### লগ ফাইল চেক করুন
```bash
tail -f bot.log
```

### পোর্ট পরিবর্তন করুন
```bash
# Admin Panel পোর্ট পরিবর্তন
python admin/app.py --port 8000
```

---

## ✅ সেটআপ সম্পন্ন!

🎉 অভিনন্দন! আপনার প্রজেক্ট এখন চলছে।

### চেকলিস্ট:
- ✅ Python ইনস্টল করা হয়েছে
- ✅ প্রজেক্ট ডাউনলোড করা হয়েছে
- ✅ .env ফাইল সেটআপ করা হয়েছে
- ✅ ডাটাবেস তৈরি করা হয়েছে
- ✅ ডিপেন্ডেন্সি ইনস্টল করা হয়েছে
- ✅ বট চলছে
- ✅ Admin Panel চলছে

---

## 📞 সাহায্য প্রয়োজন?

যদি আপনি কোনো সমস্যার সম্মুখীন হন:

1. **GitHub Issues এ প্রশ্ন করুন:**
   https://github.com/sofequl1996-cell/telegram-bot-generator-main/issues

2. **Discord সার্ভারে যোগ দিন:**
   (যদি উপলব্ধ হয়)

3. **Email করুন:**
   sofequl1996@gmail.com

---

**সুখী কোডিং!** 🚀💻

**সর্বশেষ আপডেট:** 2026-09-10
**সংস্করণ:** 1.0.0
