# Website Q&A Chatbot - Web UI

A professional web interface for your URL-based chatbot backend.

## Features

- **Modern UI**: Clean, responsive design using Tailwind CSS
- **URL Input**: Easy-to-use interface for entering multiple URLs
- **Real-time Chat**: Interactive chat interface with typing indicators
- **Session Management**: Maintains conversation context
- **Error Handling**: Comprehensive error messages and loading states
- **Mobile Responsive**: Works on all device sizes

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the web server**:
   ```bash
   python app.py
   ```

3. **Open your browser**:
   Navigate to `http://localhost:5000`

## How to Use

1. **Index Websites**:
   - Enter one or more URLs (comma-separated) in the input field
   - Click "Index" to process the websites
   - Wait for the indexing to complete

2. **Chat with Content**:
   - Once indexing is complete, the chat interface will appear
   - Ask questions about the website content
   - The bot will provide answers based on the indexed information

3. **Start New Session**:
   - Click "New Session" to reset and index different websites

## API Endpoints

### POST `/api/index`
Index website URLs
```json
{
  "urls": "https://example.com, https://another-site.com"
}
```

### POST `/api/chat`
Send a chat message
```json
{
  "session_id": "uuid",
  "query": "What is this website about?"
}
```

### POST `/api/reset`
Reset a session
```json
{
  "session_id": "uuid"
}
```

## Technical Details

- **Backend**: Flask web server with CORS support
- **Frontend**: HTML5, CSS3, JavaScript with Tailwind CSS
- **Icons**: Font Awesome
- **Session Storage**: In-memory (for production, consider Redis or database)
- **Responsive Design**: Mobile-first approach

## File Structure

```
Opencode_chatbot/
├── app.py                 # Flask web server
├── main.py               # Original chatbot logic
├── templates/
│   └── index.html        # Web UI template
├── requirements.txt      # Updated dependencies
└── README_WEB_UI.md      # This file
```

## Production Considerations

For production deployment:

1. Use a proper session store (Redis, database)
2. Implement user authentication
3. Add rate limiting
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Set up proper logging and monitoring
6. Configure HTTPS

## Troubleshooting

- **Port already in use**: Change the port in `app.py`
- **CORS issues**: Ensure `flask-cors` is installed
- **Indexing fails**: Check URLs are accessible and valid
- **Chat not working**: Verify the session was created successfully
