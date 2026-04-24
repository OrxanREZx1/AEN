# Deploying AEN to Railway (with SQLite)

This guide explains how to deploy the AEN Django project to Railway using a persistent SQLite database instead of switching to PostgreSQL.

## 1. Prerequisites
- Ensure your code is pushed to a GitHub repository.
- Ensure you have a Railway account (https://railway.app).

## 2. Create the Railway Project
1. Log in to your Railway dashboard.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your AEN repository.
4. Railway will automatically detect the Python environment and build it using the `requirements.txt` and `Procfile`.

## 3. Add a Persistent Volume (Crucial for SQLite)
Since Railway containers are ephemeral (they reset on every deploy), we must mount a Volume to keep our SQLite database safe.

1. Go to your new Railway service's **Settings** tab.
2. Scroll down to **Volumes**.
3. Click **Add Volume**.
4. Set the **Mount Path** to `/app/data`.

## 4. Set Environment Variables
Go to your service's **Variables** tab and add the following keys. 

**Core Application Variables:**
- `SQLITE_PATH`: `/app/data/db.sqlite3`  *(This forces Django to save the DB inside your safe volume)*
- `SECRET_KEY`: `your-strong-random-production-secret-key-here`
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `your-app-name.up.railway.app` *(Replace with your actual Railway public domain)*
- `CSRF_TRUSTED_ORIGINS`: `https://your-app-name.up.railway.app` *(Must match your public domain)*

**Feedback System Email Variables (Optional):**
- `EMAIL_HOST`: `smtp.gmail.com`
- `EMAIL_PORT`: `587`
- `EMAIL_USE_TLS`: `True`
- `EMAIL_HOST_USER`: `your_email@gmail.com`
- `EMAIL_HOST_PASSWORD`: `your_gmail_app_password`
- `DEFAULT_FROM_EMAIL`: `your_email@gmail.com`
- `FEEDBACK_RECEIVER_EMAIL`: `academicexchangenetwork@gmail.com`

**WhatsApp Variables:**
- `WHATSAPP_CHANNEL_URL`: `https://whatsapp.com/channel/0029Vb76VSzEFeXkl3Eyyq26`

## 5. Generate a Public Domain
1. Go to the **Settings** tab of your service.
2. Under **Networking**, click **Generate Domain** (or add your custom domain).
3. *Make sure the generated domain matches what you put in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.*

## 6. Run Migrations and Collect Static Files
Once the deployment finishes building, you need to set up your database tables and static assets.

1. In Railway, open your service.
2. Click the **>_ Terminal** tab.
3. Run the following commands:
   ```bash
   # Create tables in your mounted volume database
   python manage.py migrate

   # Bundle CSS/JS for WhiteNoise to serve
   python manage.py collectstatic --noinput

   # (Optional) Create an admin superuser
   python manage.py createsuperuser
   ```

## 7. Verification
- Open your Railway public domain URL.
- The landing page should render with all styles intact.
- Submit a test feedback to verify SQLite is writing successfully.
- Go to `/en/admin/` to verify login functionality.
