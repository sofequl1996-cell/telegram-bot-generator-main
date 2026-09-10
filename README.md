# 🤖 Telegram Bot Generator - সম্পূর্ণ সংস্করণ

একটি শক্তিশালী Telegram বট যা স্বয়ংক্রিয়ভাবে স্টুডেন্ট অ্যাকাউন্ট জেনারেশন করে এবং বিশ্ববিদ্যালয়ের ইমেইল ফরম্যাট সাপোর্ট করে।

## ✨ বৈশিষ্ট্য

- ✅ **Telegram বট ইন্টিগ্রেশন** - সম্পূর্ণ কমান্ড সাপোর্ট
- ✅ **স্টুডেন্ট অ্যাকাউন্ট জেনারেশন** - বিভিন্ন বিশ্ববিদ্যালয় সাপোর্ট
- ✅ **২০টি ডেমো ইমেইল** - বাংলাদেশ (10) + USA (10)
- ✅ **ইমেল যাচাইকরণ সিস্টেম** - স্বয়ংক্রিয় ভেরিফিকেশন
- ✅ **Flask Admin Panel** - সম্পূর্ণ ড্যাশবোর্ড
- ✅ **Database মডেল** - SQLAlchemy সহ
- ✅ **API এন্ডপয়েন্ট** - RESTful API
- ✅ **Docker সাপোর্ট** - সহজ ডিপ্লয়মেন্ট

## 📋 প্রয়োজনীয়তা

- Python 3.8+
- PostgreSQL 12+ (অথবা SQLite বিকাশের জন্য)
- Redis 6+ (ঐচ্ছিক)
- Docker & Docker Compose (ঐচ্ছিক)

## 🚀 দ্রুত শুরু

### 1️⃣ রিপোজিটরি ক্লোন করুন

```bash
git clone https://github.com/sofequl1996-cell/telegram-bot-generator-main.git
cd telegram-bot-generator-main
```

### 2️⃣ পরিবেশ সেটআপ করুন

```bash
cp .env.example .env
# .env ফাইল সম্পাদনা করুন এবং আপনার তথ্য যোগ করুন
```

### 3️⃣ নির্ভরতা ইনস্টল করুন

```bash
pip install -r requirements.txt
```

### 4️⃣ ডাটাবেস ইনিশিয়ালাইজ করুন

```bash
python -c "from database.db import init_db; init_db()"
```

### 5️⃣ বট চালু করুন

```bash
python bot/main.py
```

### 6️⃣ Admin Panel চালু করুন (নতুন টার্মিনালে)

```bash
python admin/app.py
```

Admin প্যানেল অ্যাক্সেস করুন: `http://localhost:5000`

## 🐳 Docker দিয়ে চালান

```bash
docker-compose up -d
```

সব সেবা তাৎক্ষণিকভাবে শুরু হবে:
- বট: স্বয়ংক্রিয়ভাবে শুরু
- Admin Panel: http://localhost:5000
- PostgreSQL: localhost:5432

## 📁 সম্পূর্ণ প্রকল্প কাঠামো

```
telegram-bot-generator-main/
│
├── 🤖 bot/                           # Telegram বট কোড
│   ├── main.py                       # প্রধান বট শুরু ও কনফিগ
│   ├── handlers.py                   # কমান্ড হ্যান্ডলার (start, help, etc)
│   ├── keyboards.py                  # কাস্টম কীবোর্ড UI
│   └── __init__.py
│
├── 💾 database/                      # ডাটাবেস কনফিগ
│   ├── db.py                         # SQLAlchemy ইঞ্জিন ও সেটআপ
│   ├── models.py                     # User, Account, EmailLog মডেল
│   └── __init__.py
│
├── 🔧 services/                      # ব্যবসায়িক লজিক
│   ├── user_manager.py               # ইউজার ম্যানেজমেন্ট
│   ├── account_generator.py          # 20টি ডেমো ইমেইল জেনারেটর
│   ├── email_service.py              # ইমেইল পাঠানো ও লগিং
│   └── __init__.py
│
├── 🎛️ admin/                         # Flask Admin Panel
│   ├── app.py                        # Flask মূল অ্যাপ্লিকেশন
│   ├── auth.py                       # লগইন ও প্রমাণীকরণ
│   ├── routes.py                     # API রুট ও পেজ
│   ├── templates/                    # HTML টেমপ্লেট
│   │   ├── base.html                 # বেস টেমপ্লেট
│   │   ├── login.html                # লগইন পেজ
│   │   ├── dashboard.html            # ড্যাশবোর্ড + Demo Emails
│   │   └── users.html                # ইউজার ম্যানেজমেন্ট
│   └── __init__.py
│
├── ⚙️ config.py                       # সব কনফিগারেশন
├── 📦 requirements.txt                # Python ডিপেন্ডেন্সি
├── 🐳 docker-compose.yml             # Docker কনফিগারেশন
├── 📜 Dockerfile                     # বট এর Dockerfile
├── 📜 Dockerfile.admin              # Admin Panel এর Dockerfile
├── 🔑 .env.example                   # এনভায়রনমেন্ট ভেরিয়েবল উদাহরণ
├── .gitignore                        # Git ইগনোর ফাইল
└── README.md                         # এই ফাইল
```

## 📊 ডেমো ডাটা - ২০ টি স্টুডেন্ট ইমেইল

### 🇧🇩 বাংলাদেশের বিশ্ববিদ্যালয় (১০টি)

| # | ইমেইল | বিশ্ববিদ্যালয় |
|----|--------|-----------------|
| 1 | `rahim@buet.ac.bd` | BUET - বুয়েট |
| 2 | `rahim.1803045@kuet.ac.bd` | KUET - রোল ফরম্যাট |
| 3 | `rahim.std@du.ac.bd` | ঢাকা বিশ্ববিদ্যালয় |
| 4 | `rahim.220101@ku.ac.bd` | খুলনা বিশ্ববিদ্যালয় |
| 5 | `rahim.cmt@duet.ac.bd` | DUET - ডিপার্টমেন্ট ফরম্যাট |
| 6 | `rahim.stud@sust.edu` | SUST |
| 7 | `rahim.1234@ru.ac.bd` | রাজশাহী বিশ্ববিদ্যালয় |
| 8 | `rahim@iut-dhaka.edu` | IUT |
| 9 | `rahim.student@nsu.edu` | NSU |
| 10 | `rahim.cse@bracu.ac.bd` | BRAC বিশ্ববিদ্যালয় |

### 🇺🇸 আমেরিকার বিশ্ববিদ্যালয় (১০টি)

| # | ইমেইল | বিশ্ববিদ্যালয় |
|----|--------|-----------------|
| 1 | `rahim@harvard.edu` | Harvard University |
| 2 | `rahim.std@stanford.edu` | Stanford University |
| 3 | `rahim123@mit.edu` | MIT |
| 4 | `r.rahim@berkeley.edu` | UC Berkeley |
| 5 | `rahim.student@columbia.edu` | Columbia University |
| 6 | `rahim_std@nyu.edu` | New York University |
| 7 | `rahim@ucla.edu` | UCLA |
| 8 | `rahim.26@yale.edu` | Yale University |
| 9 | `rahim.stud@princeton.edu` | Princeton University |
| 10 | `rahim@cornell.edu` | Cornell University |

## 🔐 Admin Panel লগইন

**Demo শংসাপত্র:**
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **নোট:** প্রোডাকশনে এটি পরিবর্তন করুন!

## ⚙️ কনফিগারেশন

### .env ফাইল সেটআপ

```env
# 🤖 Telegram
TELEGRAM_BOT_TOKEN=আপনার_বট_টোকেন
TELEGRAM_API_ID=আপনার_API_ID
TELEGRAM_API_HASH=আপনার_API_HASH

# 💾 Database
DATABASE_URL=postgresql://user:password@localhost:5432/telegram_bot_db
# বা SQLite বিকাশের জন্য:
# DATABASE_URL=sqlite:///./bot.db

# 📧 Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# 🎛️ Admin Panel
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=hash_of_your_password
API_TOKEN=your_secure_api_token
SECRET_KEY=your_flask_secret_key

# 🔧 Application
DEBUG=False
ENVIRONMENT=production
```

## 📚 API ডকুমেন্টেশন

### Admin API এন্ডপয়েন্ট

#### 1. ডেমো ইমেইল লিস্ট পান
```bash
GET /admin/api/demo-emails
Authorization: Bearer YOUR_API_TOKEN
```

**Response:**
```json
{
  "BD": [
    {
      "email": "rahim@buet.ac.bd",
      "university": "BUET",
      "university_full": "Bangladesh University of Engineering and Technology",
      "domain": "buet.ac.bd",
      "country": "Bangladesh 🇧🇩"
    }
  ],
  "US": [...]
}
```

#### 2. সব ইউজার পান
```bash
GET /admin/api/users
Authorization: Bearer YOUR_API_TOKEN
```

#### 3. সব অ্যাকাউন্ট পান
```bash
GET /admin/api/accounts
Authorization: Bearer YOUR_API_TOKEN
```

#### 4. ইমেইল লগ পান
```bash
GET /admin/api/email-logs
Authorization: Bearer YOUR_API_TOKEN
```

## 🎮 Telegram বট কমান্ড

| কমান্ড | ফাংশন | বর্ণনা |
|--------|---------|---------|
| `/start` | শুরু করুন | বট চালু করুন এবং মেনু দেখুন |
| `/help` | সাহায্য | সব কমান্ড তালিকা দেখুন |
| `/account` | অ্যাকাউন্ট তৈরি করুন | নতুন অ্যাকাউন্ট তৈরি করুন |
| `/status` | অবস্থা দেখুন | আপনার অ্যাকাউন্ট অবস্থা চেক করুন |

## 📊 ড্যাশবোর্ড মেট্রিক্স

Admin Panel নিম্নলিখিত তথ্য প্রদান করে:

- 📈 **মোট ইউজার** - রেজিস্টারড ব্যবহারকারী সংখ্যা
- 🔐 **মোট অ্যাকাউন্ট** - জেনারেট করা অ্যাকাউন্ট
- ✅ **ভেরিফাইড ইউজার** - ইমেইল ভেরিফাইড ব্যবহারকারী
- 📧 **পাঠানো ইমেইল** - সফল ইমেইল
- 🇧🇩 **বাংলাদেশ ডেমো** - 10টি ইমেইল
- 🇺🇸 **USA ডেমো** - 10টি ইমেইল

## 🔒 নিরাপত্তা বৈশিষ্ট্য

- 🔐 **Bcrypt পাসওয়ার্ড হ্যাশিং**
- 🔑 **JWT টোকেন প্রমাণীকরণ**
- 🔒 **HTTPS/TLS এনক্রিপশন**
- 🛡️ **SQL ইনজেকশন প্রোটেকশন** (SQLAlchemy ORM)
- 📝 **Audit Logs** - সব কার্যকলাপ রেকর্ড
- 🚫 **Rate Limiting** - API রেট লিমিটিং

## 🐛 সমস্যা সমাধান

### ❌ বট সংযোগ করছে না?

```bash
# TOKEN যাচাই করুন
echo $TELEGRAM_BOT_TOKEN

# বট লগ চেক করুন
python bot/main.py  # ডাইরেক্ট চালান লগ দেখতে

# Docker এ:
docker logs telegram-bot-container
```

### ❌ ডাটাবেস ত্রুটি?

```bash
# ডাটাবেস অবস্থা চেক করুন
docker-compose ps

# ডাটাবেস লগ দেখুন
docker-compose logs postgres

# ডাটাবেস পুনরায় ইনিশিয়ালাইজ করুন
python -c "from database.db import init_db; init_db()"
```

### ❌ Admin Panel লোড হচ্ছে না?

```bash
# Flask চালান debug মোডে
export FLASK_ENV=development
export FLASK_DEBUG=1
python admin/app.py
```

### ❌ ইমেইল পাঠানো হচ্ছে না?

```bash
# .env এ SMTP সেটিংস চেক করুন
# Gmail ব্যবহার করলে: App Password ব্যবহার করুন (না পাসওয়ার্ড)
# ডাটাবেসে EmailLog টেবিল চেক করুন
```

## 📦 ডিপেন্ডেন্সি

### মূল প্যাকেজ:
- `python-telegram-bot` - Telegram Bot API
- `flask` - Web Framework
- `sqlalchemy` - ORM
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variables

দেখুন `requirements.txt` সম্পূর্ণ তালিকার জন্য।

## 🚀 উৎপাদনে ডিপ্লয়মেন্ট

### Heroku এ ডিপ্লয়:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set TELEGRAM_BOT_TOKEN=your_token
git push heroku main
```

### DigitalOcean এ:
```bash
# Droplet তৈরি করুন
# Docker স্থাপন করুন
docker-compose -f docker-compose.yml up -d
```

## 📝 লাইসেন্স

এই প্রকল্প **MIT লাইসেন্সের** অধীন - বিস্তারিত জন্য LICENSE ফাইল দেখুন।

## 👥 অবদানকারী

অবদান স্বাগত! অনুগ্রহ করে:
1. Fork করুন
2. Feature Branch তৈরি করুন (`git checkout -b feature/AmazingFeature`)
3. Commit করুন (`git commit -m 'Add AmazingFeature'`)
4. Push করুন (`git push origin feature/AmazingFeature`)
5. Pull Request খুলুন

## 📞 সহায়তা

সমস্যা বা প্রশ্ন থাকলে:
- [GitHub Issues](https://github.com/sofequl1996-cell/telegram-bot-generator-main/issues) খুলুন
- [Discussions](https://github.com/sofequl1996-cell/telegram-bot-generator-main/discussions) শুরু করুন
- ইমেইল করুন: sofequl1996@gmail.com

## 🙏 ধন্যবাদ

এই প্রকল্প ব্যবহার করার জন্য আপনাকে ধন্যবাদ! 🚀

**সুখী কোডিং!** 💻✨

---

**সর্বশেষ আপডেট:** 2026-09-10
**সংস্করণ:** 1.0.0
**লেখক:** sofequl1996-cell
