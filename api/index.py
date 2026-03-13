import json
import uuid
from main import index_urls, ask_question
import warnings

warnings.filterwarnings("ignore")

# Store manifests in memory (in production, consider Vercel KV or external storage)
manifests = {}

def handler(request):
    """Main API handler for all requests"""
    try:
        # Handle different HTTP methods and paths
        if request.method == 'GET':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': '''<!DOCTYPE html>
<html>
<head>
    <title>Chatbot API</title>
    <meta http-equiv="refresh" content="0; url=/">
</head>
<body>
    <h1>Chatbot API</h1>
    <p>Redirecting to main app...</p>
</body>
</html>'''
            }
        
        elif request.method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': ''
            }
        
        elif request.method == 'POST':
            # Parse request body
            try:
                body = json.loads(request.body) if request.body else {}
            except:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
            
            # Route based on action
            action = body.get('action', '')
            
            if action == 'index':
                return handle_index(body)
            elif action == 'chat':
                return handle_chat(body)
            elif action == 'reset':
                return handle_reset(body)
            else:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Invalid action'})
                }
        
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Method not allowed'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }

def handle_index(body):
    """Handle URL indexing"""
    try:
        urls = body.get('urls', '').strip()
        
        if not urls:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Please provide at least one URL'})
            }
        
        # Create unique session ID
        session_id = str(uuid.uuid4())
        
        # Index the URLs
        manifest = index_urls(urls)
        
        if not manifest.get('indexed_content'):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Failed to fetch content from the URLs'})
            }
        
        # Store manifest for this session
        manifests[session_id] = manifest
        
        num_pages = len(manifest.get('indexed_content', {}))
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'session_id': session_id,
                'message': f'Successfully indexed {num_pages} page(s)',
                'num_pages': num_pages
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def handle_chat(body):
    """Handle chat messages"""
    try:
        session_id = body.get('session_id')
        query = body.get('query', '').strip()
        
        if not session_id or session_id not in manifests:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Invalid or expired session'})
            }
        
        if not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Please provide a question'})
            }
        
        manifest = manifests[session_id]
        result = ask_question(manifest, query)
        
        # Update manifest in case chat_active changed
        manifests[session_id] = manifest
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': result['response'],
                'chat_active': result['chat_active']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def handle_reset(body):
    """Handle session reset"""
    try:
        session_id = body.get('session_id')
        
        if session_id in manifests:
            del manifests[session_id]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Session reset successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

# Vercel serverless function handler
def lambda_handler(event, context):
    """AWS Lambda compatible handler for Vercel"""
    class MockRequest:
        def __init__(self, event):
            self.method = event.get('httpMethod', 'GET')
            self.body = event.get('body', '')
            self.headers = event.get('headers', {})
    
    request = MockRequest(event)
    result = handler(request)
    
    return {
        'statusCode': result['statusCode'],
        'headers': result['headers'],
        'body': result['body']
    }
