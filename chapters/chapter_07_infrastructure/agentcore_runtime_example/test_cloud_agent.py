"""
Test the deployed Lambda function
"""

import boto3
import json

def test_lambda_function():
    """Test the Lambda function using boto3"""
    lambda_client = boto3.client('lambda')
    
    test_payload = {
        'prompt': 'Hello! What is 15 + 27?'
    }
    
    print("🧪 Testing Lambda function directly...")
    print(f"Payload: {test_payload}")
    
    try:
        response = lambda_client.invoke(
            FunctionName='strands-agent-simple',
            InvocationType='RequestResponse',
            Payload=json.dumps(test_payload)
        )
        
        # Read response
        payload = response['Payload'].read()
        result = json.loads(payload.decode('utf-8'))
        
        print(f"Status Code: {response['StatusCode']}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response['StatusCode'] == 200:
            print("✅ Lambda function test successful!")
            return True
        else:
            print("❌ Lambda function test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Lambda function: {e}")
        return False

def test_function_url():
    """Test the function URL"""
    import requests
    
    function_url = "https://72uoneuhhntcppeuwcpkprqczq0oveqh.lambda-url.us-east-1.on.aws/"
    
    test_payload = {
        'prompt': 'Hello! What is 10 * 5?'
    }
    
    print("\n🌐 Testing Function URL...")
    print(f"URL: {function_url}")
    print(f"Payload: {test_payload}")
    
    try:
        response = requests.post(
            function_url,
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Function URL test successful!")
            print(f"Agent Response: {result.get('response', 'N/A')}")
            return True
        else:
            print("❌ Function URL test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Function URL: {e}")
        return False

def check_logs():
    """Check CloudWatch logs"""
    logs_client = boto3.client('logs')
    
    log_group_name = '/aws/lambda/strands-agent-simple'
    
    print("\n📊 Checking CloudWatch logs...")
    
    try:
        # Get log streams
        response = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=5
        )
        
        if response['logStreams']:
            latest_stream = response['logStreams'][0]
            stream_name = latest_stream['logStreamName']
            
            # Get log events
            events_response = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=stream_name,
                limit=20
            )
            
            print(f"📝 Recent logs from {stream_name}:")
            for event in events_response['events'][-10:]:  # Show last 10 events
                print(f"  {event['message'].strip()}")
                
        else:
            print("No log streams found yet")
            
    except Exception as e:
        print(f"❌ Error checking logs: {e}")

if __name__ == "__main__":
    print("🧪 Testing Deployed Strands Agent")
    print("=" * 50)
    
    # Test direct Lambda invocation
    lambda_success = test_lambda_function()
    
    # Test Function URL
    url_success = test_function_url()
    
    # Check logs
    check_logs()
    
    print("\n" + "=" * 50)
    if lambda_success or url_success:
        print("🎉 At least one test method worked!")
    else:
        print("❌ All tests failed - check the logs above")
