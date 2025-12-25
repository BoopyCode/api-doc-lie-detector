#!/usr/bin/env python3
"""API Lie Detector - Because docs lie more than politicians during election season"""

import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

def check_endpoint(url: str, expected_status: int = 200) -> Dict[str, Any]:
    """Checks if an endpoint exists and returns what it promised (or lies about)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LieDetector/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            actual_status = response.status
            content_type = response.headers.get('Content-Type', 'unknown')
            
            # Try to parse JSON if it claims to be JSON
            body = response.read().decode('utf-8', errors='ignore')
            is_json = False
            if 'application/json' in content_type:
                try:
                    json.loads(body)
                    is_json = True
                except:
                    pass
            
            return {
                'url': url,
                'expected_status': expected_status,
                'actual_status': actual_status,
                'content_type': content_type,
                'is_json': is_json,
                'alive': True,
                'truthful': actual_status == expected_status,
                'note': 'Endpoint exists!' if actual_status == expected_status else f'Lied about status! Said {expected_status}, gave {actual_status}'
            }
    except urllib.error.HTTPError as e:
        return {
            'url': url,
            'expected_status': expected_status,
            'actual_status': e.code,
            'alive': False,
            'truthful': False,
            'note': f'HTTP Error {e.code}: {e.reason} - Classic ghost endpoint'
        }
    except Exception as e:
        return {
            'url': url,
            'expected_status': expected_status,
            'actual_status': 'N/A',
            'alive': False,
            'truthful': False,
            'note': f'Connection failed: {str(e)} - Docs said it would work, lol'
        }

def main():
    """Main function - because every script needs one, like every API needs auth."""
    if len(sys.argv) < 2:
        print('Usage: python api_lie_detector.py <url> [expected_status]')
        print('Example: python api_lie_detector.py https://api.example.com/users 200')
        sys.exit(1)
    
    url = sys.argv[1]
    expected_status = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    
    print(f'\n🔍 Interrogating: {url}')
    print(f'📄 Docs claim: HTTP {expected_status}')
    print('-' * 50)
    
    result = check_endpoint(url, expected_status)
    
    # Verdict with dramatic flair
    if result['truthful']:
        print('✅ TRUTHFUL! Endpoint exists as documented (shocking!)')
    else:
        print('❌ LIAR LIAR! Docs on fire!')
    
    print(f'\nDetails:')
    for key, value in result.items():
        if key != 'url':  # Already printed
            print(f'  {key}: {value}')
    
    # Bonus snark
    if not result['alive']:
        print('\n💀 This endpoint is deader than the last framework you loved.')
    elif result['is_json']:
        print('\n📦 At least it returns JSON. Small victories!')

if __name__ == '__main__':
    main()
