# Job Apply Bot

A Python bot to automate job applications on Instahyre and Hirist platforms.

## Features

- Apply to jobs automatically on Instahyre and Hirist
- Supports user profiles and credential management
- Search and apply based on skills, experience, and location

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/YOUR_USERNAME/job_apply_bot.git
cd job_apply_bot
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure credentials

- Copy the sample credentials file:

  ```sh
  cp config/credentials.sample.json config/credentials.json
  ```

- Edit `config/credentials.json` and add your email and password for each platform.

### 4. Run the bot

```sh
python main.py
```

## File Structure

```
job_apply_bot/
├── bots/
├── config/
│   ├── credentials.json
│   └── credentials.sample.json
├── main.py
├── requirements.txt
└── README.md
```

## Credentials File Format

See `config/credentials.sample.json` for the structure.  
**Never share your real credentials or commit them to GitHub!**

---

## License

MIT License