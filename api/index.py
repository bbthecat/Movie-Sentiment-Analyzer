from backend.app import app

# Vercel serverless function handler
def handler(request):
    return app(request.scope, request.receive, request.send)
