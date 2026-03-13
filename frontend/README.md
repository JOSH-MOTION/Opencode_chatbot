# 🚀 Chatbot Frontend - Vercel Deployment

A professional web UI for your URL-based chatbot, optimized for Vercel deployment.

## 🌟 Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Backend Config**: Easy backend URL configuration
- **Real-time Chat**: Interactive chat with typing indicators
- **Mobile Responsive**: Works perfectly on all devices
- **CORS Ready**: Handles cross-origin requests
- **Local Storage**: Saves backend URL preferences

## 📁 Project Structure

```
frontend/
├── index.html          # Main HTML file
├── app.js             # JavaScript application logic
├── vercel.json        # Vercel configuration
├── package.json       # Node.js dependencies
└── README.md          # This file
```

## 🚀 Deployment Steps

### 1. Deploy Backend First
Deploy your Flask backend to Railway, Render, or similar service:
- Get your backend URL (e.g., `https://your-app.railway.app`)

### 2. Deploy Frontend to Vercel

**Option A: Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel --prod
```

**Option B: Vercel Dashboard**
1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repo
5. Set environment variable `BACKEND_URL`
6. Click "Deploy"

### 3. Configure Environment Variables
In Vercel dashboard:
- Go to Settings → Environment Variables
- Add `BACKEND_URL` = `https://your-backend-url.railway.app`

## ⚙️ Configuration

### Backend URL
The frontend automatically:
- Uses the `BACKEND_URL` environment variable if set
- Falls back to `http://localhost:5000` for development
- Allows manual configuration in the UI
- Saves preference in local storage

### CORS Setup
Ensure your Flask backend has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

## 🔧 Local Development

1. **Start Backend**:
```bash
cd ..  # Go to root
uv run python app.py
```

2. **Start Frontend**:
```bash
cd frontend
vercel dev
```

3. Open `http://localhost:3000`

## 🌐 API Endpoints

The frontend communicates with these backend endpoints:

- `POST /api/index` - Index website URLs
- `POST /api/chat` - Send chat messages
- `POST /api/reset` - Reset session
- `GET /` - Health check

## 📱 Mobile Optimization

- Responsive design works on all screen sizes
- Touch-friendly interface
- Optimized for mobile browsers

## 🔒 Security Notes

- Backend URL is configurable but validated
- No sensitive data stored in frontend
- CORS protection from backend side
- Environment variables for production

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Check backend URL is correct
- Ensure backend is running and accessible
- Verify CORS is enabled on backend

### "CORS errors"
- Add `flask-cors` to backend
- Ensure backend allows your frontend domain

### "Deployment failed"
- Check all files are in `frontend/` directory
- Verify `vercel.json` configuration
- Check environment variables

## 🔄 Updates

To update the frontend:
1. Make changes to files
2. Commit to GitHub
3. Vercel auto-deploys on push

## 🎯 Production Tips

1. **Backend**: Use Railway/Render for production
2. **Frontend**: Vercel handles everything automatically
3. **Custom Domain**: Configure in Vercel dashboard
4. **Analytics**: Add Vercel Analytics for insights

## 📞 Support

If you need help:
- Check backend logs for API errors
- Verify network connectivity
- Test with local backend first
