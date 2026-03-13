// Configuration
let API_BASE_URL = window.location.origin; // Use same domain for API calls
let sessionId = null;
let isProcessing = false;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Hide backend URL config since we're using same domain
    const configSection = document.querySelector('section[class*="bg-yellow-50"]');
    if (configSection) {
        configSection.style.display = 'none';
    }
    document.getElementById('url-input').focus();
});

// API Functions
async function apiCall(action, data) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/index`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action, ...data })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Cannot connect to API. Please try again.');
        }
        throw error;
    }
}

// UI Helper Functions
function showLoading(text = 'Processing...') {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

function updateStatus(text, type = 'ready') {
    const indicator = document.getElementById('status-indicator');
    const colors = {
        ready: 'bg-yellow-400',
        success: 'bg-green-400',
        error: 'bg-red-400',
        processing: 'bg-blue-400'
    };
    
    indicator.innerHTML = `
        <span class="w-2 h-2 ${colors[type]} rounded-full animate-pulse"></span>
        <span class="text-sm">${text}</span>
    `;
}

function showIndexStatus(message, type = 'info') {
    const statusDiv = document.getElementById('index-status');
    const colors = {
        info: 'text-blue-300',
        success: 'text-green-300',
        error: 'text-red-300'
    };
    
    const bgColors = {
        info: 'bg-blue-500/20 border-blue-500/30',
        success: 'bg-green-500/20 border-green-500/30',
        error: 'bg-red-500/20 border-red-500/30'
    };
    
    statusDiv.className = `${colors[type]} glass-morphism rounded-xl px-4 py-3 border ${bgColors[type]} message-bubble text-center`;
    statusDiv.innerHTML = `
        <div class="flex items-center justify-center space-x-2">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span class="font-medium">${message}</span>
        </div>
    `;
    statusDiv.classList.remove('hidden');
}

// API Functions
async function apiCall(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Cannot connect to backend. Please check the backend URL and ensure it\'s running.');
        }
        throw error;
    }
}

// URL Indexing
async function indexUrls() {
    if (isProcessing) return;
    
    const urlInput = document.getElementById('url-input');
    const urls = urlInput.value.trim();
    
    if (!urls) {
        showIndexStatus('Please enter at least one URL', 'error');
        return;
    }

    isProcessing = true;
    const indexBtn = document.getElementById('index-btn');
    indexBtn.disabled = true;
    indexBtn.classList.add('opacity-50', 'cursor-not-allowed');
    
    showLoading('Indexing website content...');
    updateStatus('Indexing...', 'processing');
    
    try {
        const data = await apiCall('index', { urls });
        
        sessionId = data.session_id;
        showIndexStatus(data.message, 'success');
        updateStatus('Ready to chat', 'success');
        
        // Show chat section
        setTimeout(() => {
            document.getElementById('chat-section').classList.remove('hidden');
            document.getElementById('chat-section').classList.add('fade-in');
            document.getElementById('chat-input').focus();
        }, 500);
        
    } catch (error) {
        showIndexStatus(error.message, 'error');
        updateStatus('Error', 'error');
    } finally {
        hideLoading();
        isProcessing = false;
        indexBtn.disabled = false;
        indexBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// Chat Functions
function addMessage(content, isUser = false) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} message-bubble`;
    
    if (isUser) {
        messageDiv.innerHTML = `
            <div class="max-w-2xl">
                <div class="bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl px-6 py-4 shadow-lg">
                    <p class="text-white text-sm leading-relaxed">${content}</p>
                </div>
                <div class="flex items-center justify-end mt-2 space-x-2">
                    <span class="text-white/50 text-xs">You</span>
                    <i class="fas fa-user text-white/50 text-xs"></i>
                </div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="max-w-2xl">
                <div class="glass-morphism rounded-2xl px-6 py-4 border border-white/20">
                    <p class="text-white text-sm leading-relaxed">${content}</p>
                </div>
                <div class="flex items-center mt-2 space-x-2">
                    <div class="w-6 h-6 bg-gradient-to-br from-purple-400 to-pink-400 rounded-lg flex items-center justify-center">
                        <i class="fas fa-robot text-white text-xs"></i>
                    </div>
                    <span class="text-white/50 text-xs">AI Assistant</span>
                </div>
            </div>
        `;
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'flex justify-start message-bubble';
    typingDiv.innerHTML = `
        <div class="max-w-2xl">
            <div class="glass-morphism rounded-2xl px-6 py-4 border border-white/20">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div class="flex items-center mt-2 space-x-2">
                <div class="w-6 h-6 bg-gradient-to-br from-purple-400 to-pink-400 rounded-lg flex items-center justify-center">
                    <i class="fas fa-robot text-white text-xs"></i>
                </div>
                <span class="text-white/50 text-xs">AI Assistant</span>
            </div>
        </div>
    `;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

async function sendMessage() {
    if (isProcessing || !sessionId) return;
    
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    isProcessing = true;
    chatInput.value = '';
    
    // Add user message
    addMessage(message, true);
    
    // Show typing indicator
    showTypingIndicator();
    updateStatus('Thinking...', 'processing');
    
    try {
        const data = await apiCall('chat', {
            session_id: sessionId,
            query: message
        });
        
        removeTypingIndicator();
        addMessage(data.response);
        updateStatus('Ready to chat', 'success');
        
        if (!data.chat_active) {
            updateStatus('Session ended', 'error');
            document.getElementById('chat-input').disabled = true;
            document.getElementById('send-btn').disabled = true;
        }
        
    } catch (error) {
        removeTypingIndicator();
        addMessage('Error: ' + error.message, false);
        updateStatus('Error', 'error');
    } finally {
        isProcessing = false;
    }
}

async function resetChat() {
    if (isProcessing) return;
    
    isProcessing = true;
    showLoading('Resetting session...');
    
    try {
        if (sessionId) {
            await apiCall('reset', { session_id: sessionId });
        }
        
        sessionId = null;
        document.getElementById('chat-section').classList.add('hidden');
        document.getElementById('chat-messages').innerHTML = `
            <div class="text-center py-12">
                <div class="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-400 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <i class="fas fa-comments text-white text-3xl"></i>
                </div>
                <h3 class="text-2xl font-bold text-white mb-3">Ready to Chat</h3>
                <p class="text-white/70">Ask me anything about the websites we've analyzed</p>
            </div>
        `;
        document.getElementById('url-input').value = '';
        document.getElementById('index-status').classList.add('hidden');
        document.getElementById('chat-input').disabled = false;
        document.getElementById('send-btn').disabled = false;
        document.getElementById('chat-input').focus();
        
        updateStatus('Ready', 'ready');
    } catch (error) {
        console.error('Reset error:', error);
    } finally {
        hideLoading();
        isProcessing = false;
    }
}

// Connection test
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/index`, {
            method: 'GET',
            mode: 'cors'
        });
        
        if (response.ok) {
            updateStatus('Connected', 'success');
            return true;
        } else {
            updateStatus('API error', 'error');
            return false;
        }
    } catch (error) {
        updateStatus('No connection', 'error');
        return false;
    }
}

// Test connection on page load
testBackendConnection();
