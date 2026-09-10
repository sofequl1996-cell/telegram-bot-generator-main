# 🤖 Telegram Account Generator Bot

একটি শক্তিশালী Telegram বট যা স্বয়ংক্রিয়ভাবে Google, Gmail এবং অন্যান্য পরিষেবায় অ্যাকাউন্ট তৈরি করে।

## ✨ বৈশিষ্ট্য

- ✅ স্বয়ংক্রিয় অ্যাকাউন্ট জেনারেশন
- ✅ একাধিক পরিকল্পনা সমর্থন (বিনামূল্যে, প্রিমিয়াম, এন্টারপ্রাইজ)
- ✅ ইমেল যাচাইকরণ সিস্টেম
- ✅ রিয়েল-টাইম পেমেন্ট প্রক্রিয়াকরণ
- ✅ শক্তিশালী প্রশাসন প্যানেল
- ✅ ব্যবহারকারী ব্যবস্থাপনা এবং পরিসংখ্যান
- ✅ ডাটাবেস লগিং এবং নিরীক্ষা ট্রেইল

## 📋 প্রয়োজনীয়তা

- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Docker & Docker Compose (ঐচ্ছিক)

## 🚀 দ্রুত শুরু

### 1. রিপোজিটরি ক্লোন করুন

```bash
git clone https://github.com/yourusername/telegram-bot-generator.git
cd telegram-bot-generator
```

### 2. পরিবেশ সেটআপ করুন

```bash
cp .env.example .env
# .env ফাইল সম্পাদনা করুন এবং আপনার মূল্যবান তথ্য যোগ করুন
```

### 3. নির্ভরতা ইনস্টল করুন

```bash
pip install -r requirements.txt
```

### 4. ডাটাবেস মাইগ্রেশন চালান

```bash
python -m database.db
```

### 5. বট চালু করুন

```bash
python bot/main.py
```

### 6. প্রশাসন প্যানেল চালু করুন

```bash
python admin/app.py
```

প্যানেল অ্যাক্সেস করুন: `http://localhost:5000`

## 🐳 Docker দিয়ে চালান

```bash
docker-compose up -d
```

## 📁 প্রকল্প কাঠামো

```
telegram-bot-generator/
├── bot/                    # Telegram বট কোড
│   ├── main.py            # প্রধান বট প্রবেশ পয়েন্ট
│   ├── handlers.py        # কমান্ড হ্যান্ডলার
│   └── keyboards.py       # কাস্টম কীবোর্ড
├── admin/                 # Flask প্রশাসন প্যানেল
│   ├── app.py            # Flask অ্যাপ্লিকেশন
│   ├── templates/        # HTML টেমপ্লেট
│   └── static/           # CSS এবং JS ফাইল
├── services/             # ব্যবসায়িক লজিক
│   ├── user_manager.py   # ব্যবহারকারী ব্যবস্থাপনা
│   ├── account_generator.py  # অ্যাকাউন্ট জেনারেশন
│   └── email_service.py  # ইমেল পাঠানো
├── database/            # ডাটাবেস কনফিগারেশন
│   ├── db.py           # ডাটাবেস সেটআপ
│   └── models.py       # SQLAlchemy মডেল
├── config.py           # কনফিগারেশন
├── .env.example        # পরিবেশ ভেরিয়েবল উদাহরণ
├── requirements.txt    # Python নির্ভরতা
├── docker-compose.yml  # Docker কনফিগারেশন
└── README.md          # এই ফাইল
```

## ⚙️ কনফিগারেশন

### .env ফাইলে প্রয়োজনীয় ভেরিয়েবল:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHANNEL_ID=your_channel_id

# ডাটাবেস
DATABASE_URL=postgresql://user:password@localhost/bot_db

# ইমেল
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_password

# প্রশাসন
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_password
FLASK_SECRET_KEY=your_secret_key

# পেমেন্ট (ঐচ্ছিক)
STRIPE_API_KEY=your_stripe_key
STRIPE_SECRET_KEY=your_stripe_secret
```

## 📚 API ডকুমেন্টেশন

### অ্যাকাউন্ট জেনারেশন

```bash
POST /api/accounts/generate
Content-Type: application/json

{
  "user_id": 123,
  "plan": "premium"
}
```

### ব্যবহারকারী পরিসংখ্যান

```bash
GET /api/users/{user_id}/stats
```

### প্রশাসক লগ

```bash
GET /api/logs?limit=100
```

## 🔐 নিরাপত্তা

- সমস্ত পাসওয়ার্ড bcrypt দিয়ে হ্যাশ করা হয়
- JWT টোকেন-ভিত্তিক প্রমাণীকরণ
- HTTPS/TLS এনক্রিপশন সমর্থিত
- ডাটাবেস সংযোগ পুল করা
- SQL ইনজেকশন সুরক্ষা

## 📊 পরিসংখ্যান

প্রশাসন প্যানেল নিম্নলিখিত মেট্রিক্স প্রদান করে:

- মোট ব্যবহারকারী সংখ্যা
- জেনারেট করা অ্যাকাউন্ট
- সম্পূর্ণ লেনদেন
- পরিকল্পনা বিতরণ
- ব্যবহারকারী কার্যকলাপ লগ

## 🐛 সমস্যা সমাধান

### বট সংযোগ করছে না?
```bash
# আপনার TOKEN যাচাই করুন
echo $TELEGRAM_BOT_TOKEN

# বট লগ চেক করুন
docker logs telegram-bot
```

### ডাটাবেস ত্রুটি?
```bash
# ডাটাবেস অবস্থা চেক করুন
docker-compose ps

# ডাটাবেস লগ দেখুন
docker-compose logs postgres
```

## 📝 লাইসেন্স

এই প্রকল্প MIT লাইসেন্সের অধীন - বিস্তারিত জন্য LICENSE ফাইল দেখুন।

## 👥 অবদানকারী

অবদান স্বাগত! অনুগ্রহ করে একটি ইস্যু খুলুন বা একটি পুল রিকোয়েস্ট জমা দিন।

## 📞 সহায়তা

সমস্যা পেয়েছেন? 
- [Issues](https://github.com/yourusername/telegram-bot-generator/issues) খুলুন
- [আলোচনা](https://github.com/yourusername/telegram-bot-generator/discussions) শুরু করুন
- আমাদের সাথে যোগাযোগ করুন

## 🙏 ধন্যবাদ

এই প্রকল্পটি ব্যবহার করার জন্য আপনাকে ধন্যবাদ। সুখী কোডিং! 🚀