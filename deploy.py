#!/usr/bin/env python3
"""
Deploy Music Chord Maker to AI-builders.space platform
"""
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://space.ai-builders.com/backend"
API_TOKEN = os.getenv("AI_BUILDER_TOKEN")

if not API_TOKEN:
    print("❌ Error: AI_BUILDER_TOKEN not set in environment")
    print()
    print("Please set it using one of these methods:")
    print("1. Create a .env file: echo 'AI_BUILDER_TOKEN=your_token' > .env")
    print("2. Export as environment variable: export AI_BUILDER_TOKEN=your_token")
    print()
    print("You can get your token from the AI-builders-coach MCP or your instructor.")
    sys.exit(1)

# Deployment configuration
DEPLOYMENT_CONFIG = {
    "repo_url": "https://github.com/YiyangLi/music-chord-maker",
    "service_name": "music-chord-maker",
    "branch": "main",
    "port": 8000
}

def deploy():
    """Deploy the service"""
    url = f"{API_BASE_URL}/v1/deployments"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print(f"Deploying {DEPLOYMENT_CONFIG['service_name']}...")
    print(f"Repository: {DEPLOYMENT_CONFIG['repo_url']}")
    print(f"Branch: {DEPLOYMENT_CONFIG['branch']}")
    print()
    
    try:
        response = requests.post(url, json=DEPLOYMENT_CONFIG, headers=headers)
        
        if response.status_code == 202:
            data = response.json()
            print("✅ Deployment queued successfully!")
            print()
            print(f"Service Name: {data.get('service_name')}")
            print(f"Status: {data.get('status')}")
            print(f"Public URL: {data.get('public_url', 'Will be available after deployment')}")
            print()
            print("Deployment will take 5-10 minutes to complete.")
            print(f"Check status at: {API_BASE_URL}/v1/deployments/{DEPLOYMENT_CONFIG['service_name']}")
            print()
            if data.get('message'):
                print("Message:", data.get('message'))
        elif response.status_code == 200:
            # Sometimes the API returns 200 with deployment list
            data = response.json()
            if 'deployments' in data and len(data['deployments']) > 0:
                deployment = data['deployments'][0]
                print("✅ Deployment already exists and is active!")
                print()
                print(f"Service Name: {deployment.get('service_name')}")
                print(f"Status: {deployment.get('status')}")
                print(f"Public URL: {deployment.get('public_url', 'Not available')}")
                print(f"Last Deployed: {deployment.get('last_deployed_at', 'Unknown')}")
                print()
                if deployment.get('message'):
                    print("Message:", deployment.get('message'))
            else:
                print(f"⚠️ Unexpected response format (status {response.status_code})")
                print("Response:", response.text[:500])
        else:
            print(f"❌ Deployment failed with status {response.status_code}")
            print("Response:", response.text)
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    print("Details:", error_data['detail'])
            except:
                pass
    except Exception as e:
        print(f"❌ Error deploying: {e}")

def check_status(service_name):
    """Check deployment status"""
    url = f"{API_BASE_URL}/v1/deployments/{service_name}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Deployment Status for '{service_name}':")
            print(f"Status: {data.get('status')}")
            print(f"Public URL: {data.get('public_url', 'Not available yet')}")
            print(f"Last Deployed: {data.get('last_deployed_at', 'Never')}")
            if data.get('message'):
                print(f"Message: {data.get('message')}")
        else:
            print(f"❌ Failed to check status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error checking status: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        check_status("music-chord-maker")
    else:
        deploy()
        print("\n💡 Tip: Run 'python deploy.py status' to check deployment status")

