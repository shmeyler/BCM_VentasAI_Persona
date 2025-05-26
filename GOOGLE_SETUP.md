# Google Cloud Platform Configuration for BCM VentasAI

## Setting up Google Slides Export

To enable Google Slides export functionality, you need to configure Google Cloud Platform credentials:

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your Project ID

### 2. Enable Google Slides API
1. Go to **APIs & Services** > **Library**
2. Search for "Google Slides API"
3. Click **Enable**
4. Also enable "Google Drive API" for file creation

### 3. Create Service Account Credentials
1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **Service Account**
3. Fill in service account details
4. Click **Create and Continue**
5. Grant **Editor** role (or create custom role with Slides/Drive permissions)
6. Click **Done**

### 4. Generate Key File
1. Click on your newly created service account
2. Go to **Keys** tab
3. Click **Add Key** > **Create New Key**
4. Select **JSON** format
5. Download the JSON key file

### 5. Configure BCM VentasAI
1. Create a file called `google-credentials.json` in the backend directory
2. Copy the contents of your downloaded JSON key file
3. Restart the backend service

### 6. Environment Variables (Optional)
You can also set the credentials via environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/google-credentials.json"
```

### Example credentials.json structure:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "service-account@your-project.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40your-project.iam.gserviceaccount.com"
}
```

### Security Notes:
- Never commit credentials files to version control
- Use environment variables in production
- Rotate service account keys regularly
- Grant minimal required permissions

### Testing the Integration:
Once configured, the Google Slides export option will create presentations directly in your Google Drive and provide shareable links.