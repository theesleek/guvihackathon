"""
Test script for AI Voice Detection API
This script demonstrates how to test the API with sample requests.

Usage:
    pip install requests
    python test_api.py
"""

import base64
import json
import os

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not installed.")
    print("Install it with: pip install requests")
    exit(1)

# Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = "f_U5rvnxNUQ96Sv4xiIFZzOCVQBCNe7UTUbzyFb74O4"

# Headers
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
}


def test_root_endpoint():
    """Test the root endpoint"""
    print("\n" + "=" * 60)
    print("TEST 1: Root Endpoint")
    print("=" * 60)
    
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_detect_with_sample_audio():
    """Test /detect endpoint with a minimal synthetic audio sample"""
    print("\n" + "=" * 60)
    print("TEST 2: /detect Endpoint (with minimal test data)")
    print("=" * 60)
    
    # Create a minimal valid MP3 base64 string for testing
    # This is a very short silent MP3 file (1 second, 16kHz, mono)
    # In real usage, you would encode an actual MP3 file
    
    # For demonstration, we'll use a minimal valid base64 that represents
    # a tiny audio file. In production, replace this with actual MP3 base64.
    
    # NOTE: This is a placeholder. For real testing, you need an actual MP3 file.
    # To encode a real MP3 file, use:
    # with open("sample.mp3", "rb") as f:
    #     audio_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    # Minimal test payload (this will fail with "Invalid base64 audio data" 
    # but shows the API structure)
    payload = {
        "audio_base64": "dGVzdA==",  # This is just "test" encoded, not a real MP3
        "language": "en"
    }
    
    print(f"Request URL: {API_BASE_URL}/detect")
    print(f"Request Headers: {json.dumps(headers, indent=2)}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/detect",
            headers=headers,
            json=payload
        )
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code in [200, 400]  # 400 is expected for invalid audio
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_detect_with_real_mp3(mp3_file_path: str):
    """Test /detect endpoint with a real MP3 file"""
    print("\n" + "=" * 60)
    print(f"TEST 3: /detect Endpoint (with real MP3: {mp3_file_path})")
    print("=" * 60)
    
    if not os.path.exists(mp3_file_path):
        print(f"⚠️  File not found: {mp3_file_path}")
        print("   Skipping this test. Provide a valid MP3 file path to test.")
        return False
    
    # Encode MP3 to base64
    with open(mp3_file_path, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    
    payload = {
        "audio_base64": audio_base64,
        "language": "en"  # Change to "ta", "hi", "ml", or "te" for other languages
    }
    
    print(f"MP3 File: {mp3_file_path}")
    print(f"File Size: {len(audio_bytes)} bytes")
    print(f"Base64 Length: {len(audio_base64)} characters")
    print(f"Language: {payload['language']}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/detect",
            headers=headers,
            json=payload
        )
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"Result: {result['result']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print(f"Details: {json.dumps(result['details'], indent=2)}")
            return True
        else:
            print(f"❌ Error Response: {json.dumps(response.json(), indent=2)}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_invalid_api_key():
    """Test with invalid API key"""
    print("\n" + "=" * 60)
    print("TEST 4: Invalid API Key")
    print("=" * 60)
    
    invalid_headers = {
        "Content-Type": "application/json",
        "x-api-key": "invalid_key_12345",
    }
    
    payload = {
        "audio_base64": "dGVzdA==",
        "language": "en"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/detect",
        headers=invalid_headers,
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Should return 401 Unauthorized
    return response.status_code == 401


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("AI VOICE DETECTION API - TEST SUITE")
    print("=" * 60)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY[:20]}...")
    
    results = []
    
    # Test 1: Root endpoint
    results.append(("Root Endpoint", test_root_endpoint()))
    
    # Test 2: Detect with placeholder (will fail but shows structure)
    results.append(("Detect Endpoint (placeholder)", test_detect_with_sample_audio()))
    
    # Test 3: Detect with real MP3 (if file exists)
    # Uncomment and provide path to test with real audio:
    # results.append(("Detect Endpoint (real MP3)", test_detect_with_real_mp3("sample.mp3")))
    
    # Test 4: Invalid API key
    results.append(("Invalid API Key", test_invalid_api_key()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 60)
    print("To test with a real MP3 file:")
    print("1. Place an MP3 file in the project directory")
    print("2. Uncomment the test_detect_with_real_mp3 line in main()")
    print("3. Update the file path")
    print("=" * 60)


if __name__ == "__main__":
    main()

