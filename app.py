from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import random
from dotenv import load_dotenv
import requests
from openai import AzureOpenAI
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ML_API_ENDPOINT = os.getenv('ML_API_ENDPOINT')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')

# Batch processing configuration
BATCH_SIZE = 50  # Process 50 transactions at a time
MAX_CONCURRENT_REQUESTS = 10  # Max concurrent API calls

# Check which services are available
ML_API_AVAILABLE = bool(ML_API_ENDPOINT)
OPENAI_AVAILABLE = bool(AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY)


def get_mock_fraud_prediction(transaction):
    """Generate mock fraud prediction"""
    # Simple rule-based mock: flag if amount > 5000 or login attempts > 3
    amount = transaction.get('TransactionAmount', 0)
    login_attempts = transaction.get('LoginAttempts', 0)
    
    is_fraud = int(amount > 5000 or login_attempts > 3)
    
    # Generate mock fraud score
    if is_fraud:
        fraud_score = random.uniform(0.65, 0.95)
    else:
        fraud_score = random.uniform(0.05, 0.45)
    
    return {
        'fraud_or_not': is_fraud,
        'fraud_score': round(fraud_score, 4)
    }


def call_ml_api(transaction):
    """Call ML API or return mock data"""
    if not ML_API_ENDPOINT:
        return get_mock_fraud_prediction(transaction)
    
    try:
        response = requests.post(
            ML_API_ENDPOINT,
            json={
                'TransactionAmount': transaction.get('TransactionAmount'),
                'TransactionDuration': transaction.get('TransactionDuration'),
                'LoginAttempts': transaction.get('LoginAttempts'),
                'AccountBalance': transaction.get('AccountBalance'),
                'CustomerAge': transaction.get('CustomerAge')
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        # Map the API response to our expected format
        return {
            'fraud_or_not': int(result.get('fraud_prediction', 0)),
            'fraud_score': float(result.get('fraud_score', 0))
        }
    except Exception as e:
        print(f"ML API Error: {e}. Using mock data.")
        return get_mock_fraud_prediction(transaction)


async def call_ml_api_async(session, transaction):
    """Async version of ML API call"""
    if not ML_API_ENDPOINT:
        return get_mock_fraud_prediction(transaction)
    
    try:
        payload = {
            'TransactionAmount': transaction.get('TransactionAmount'),
            'TransactionDuration': transaction.get('TransactionDuration'),
            'LoginAttempts': transaction.get('LoginAttempts'),
            'AccountBalance': transaction.get('AccountBalance'),
            'CustomerAge': transaction.get('CustomerAge')
        }
        
        async with session.post(ML_API_ENDPOINT, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
            result = await response.json()
            return {
                'fraud_or_not': int(result.get('fraud_prediction', 0)),
                'fraud_score': float(result.get('fraud_score', 0))
            }
    except Exception as e:
        print(f"ML API Error for transaction: {e}")
        return get_mock_fraud_prediction(transaction)


async def process_transactions_batch(transactions):
    """Process transactions in batches asynchronously"""
    results = []
    
    async with aiohttp.ClientSession() as session:
        # Process in batches to avoid overwhelming the API
        for i in range(0, len(transactions), BATCH_SIZE):
            batch = transactions[i:i + BATCH_SIZE]
            print(f"Processing batch {i//BATCH_SIZE + 1}/{(len(transactions)-1)//BATCH_SIZE + 1} ({len(batch)} transactions)")
            
            # Create tasks for concurrent requests (limited by MAX_CONCURRENT_REQUESTS)
            tasks = []
            for j in range(0, len(batch), MAX_CONCURRENT_REQUESTS):
                sub_batch = batch[j:j + MAX_CONCURRENT_REQUESTS]
                batch_tasks = [call_ml_api_async(session, txn) for txn in sub_batch]
                tasks.extend(batch_tasks)
                
                # Wait for this sub-batch to complete before starting next
                if len(tasks) >= MAX_CONCURRENT_REQUESTS:
                    batch_results = await asyncio.gather(*tasks)
                    results.extend(batch_results)
                    tasks = []
            
            # Process any remaining tasks in the batch
            if tasks:
                batch_results = await asyncio.gather(*tasks)
                results.extend(batch_results)
    
    return results


def run_async_processing(transactions):
    """Run async processing in a synchronous context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(process_transactions_batch(transactions))
    finally:
        loop.close()


def get_mock_explanation(transaction):
    """Generate mock fraud explanation"""
    reasons = []
    
    amount = transaction.get('TransactionAmount', 0)
    duration = transaction.get('TransactionDuration', 0)
    login_attempts = transaction.get('LoginAttempts', 0)
    balance = transaction.get('AccountBalance', 0)
    age = transaction.get('CustomerAge', 0)
    
    if amount > 5000:
        reasons.append(f"Unusually high transaction amount of RM{amount:,.2f}")
    
    if login_attempts > 3:
        reasons.append(f"Excessive login attempts ({login_attempts}) indicating potential account compromise")
    
    if duration < 10:
        reasons.append(f"Very short transaction duration ({duration}s) suggesting automated behavior")
    
    if amount > balance * 0.8:
        reasons.append(f"Transaction amount represents {(amount/balance)*100:.1f}% of account balance")
    
    if age < 25 or age > 70:
        reasons.append(f"Customer age ({age}) falls in higher risk demographic")
    
    if not reasons:
        reasons.append("Multiple risk indicators combined to flag this transaction")
    
    explanation = "🚨 **Fraud Alert Analysis**\n\n"
    explanation += "This transaction has been flagged due to the following risk factors:\n\n"
    
    for i, reason in enumerate(reasons, 1):
        explanation += f"{i}. {reason}\n"
    
    explanation += f"\n**Risk Score:** {transaction.get('fraud_score', 0):.2%}\n"
    explanation += "\n**Recommendation:** Review transaction details and verify customer identity before processing."
    
    return explanation


def call_azure_openai(transaction):
    """Call Azure OpenAI for explanation or return mock"""
    if not OPENAI_AVAILABLE:
        print("⚠️ Using mock explanation (OpenAI not configured)")
        return {
            'explanation': get_mock_explanation(transaction),
            'used_openai': False,
            'error': 'OpenAI not configured'
        }
    
    try:
        print(f"🤖 Calling Azure OpenAI at {AZURE_OPENAI_ENDPOINT}")
        print(f"   Deployment: {AZURE_OPENAI_DEPLOYMENT}")
        
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            api_version="2024-08-01-preview"
        )
        
        prompt = f"""As a fraud detection expert, analyze this transaction and explain why it might be fraudulent:

Transaction Details:
- Amount: RM{transaction.get('TransactionAmount', 0):,.2f}
- Duration: {transaction.get('TransactionDuration', 0)} seconds
- Login Attempts: {transaction.get('LoginAttempts', 0)}
- Account Balance: RM{transaction.get('AccountBalance', 0):,.2f}
- Customer Age: {transaction.get('CustomerAge', 0)}
- Fraud Score: {transaction.get('fraud_score', 0):.2%}

Provide a clear, concise explanation of the fraud indicators and recommend next steps. For example:

🚨 Fraud Alert Analysis

This transaction has been flagged due to the following risk factors:

Excessive login attempts (4) indicating potential account compromise
Customer age (79) falls in higher risk demographic
Risk Score: 88.35%

Recommendation: Review transaction details and verify customer identity before processing."""

        print(f"   Sending request...")
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a fraud detection expert helping to explain suspicious transactions."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2000
        )
        
        result = response.choices[0].message.content
        print(f"✅ Got response: {len(result)} characters")
        return {
            'explanation': result,
            'used_openai': True,
            'error': None
        }
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"❌ Azure OpenAI Error: {error_msg}")
        import traceback
        traceback.print_exc()
        print("   Using mock explanation as fallback")
        return {
            'explanation': get_mock_explanation(transaction),
            'used_openai': False,
            'error': error_msg
        }


@app.route('/api/status', methods=['GET'])
def status():
    """API status endpoint"""
    return jsonify({
        'status': 'online',
        'ml_api_configured': ML_API_AVAILABLE,
        'openai_configured': OPENAI_AVAILABLE,
        'debug_info': {
            'endpoint_set': bool(AZURE_OPENAI_ENDPOINT),
            'endpoint_value': f"{AZURE_OPENAI_ENDPOINT[:30]}..." if AZURE_OPENAI_ENDPOINT else None,
            'key_set': bool(AZURE_OPENAI_KEY),
            'key_length': len(AZURE_OPENAI_KEY) if AZURE_OPENAI_KEY else 0,
            'deployment': AZURE_OPENAI_DEPLOYMENT
        }
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process Excel or CSV file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        return jsonify({'error': 'File must be Excel (.xlsx, .xls) or CSV (.csv) format'}), 400
    
    try:
        # Read Excel or CSV file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Check for required columns
        required_columns = ['TransactionAmount', 'TransactionDuration', 
                          'LoginAttempts', 'AccountBalance', 'CustomerAge']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }), 400
        
        # Process transactions
        results = []
        fraudulent_transactions = []
        
        # Prepare all transactions
        transactions_to_process = []
        for idx, row in df.iterrows():
            transaction = {
                'id': idx,
                'TransactionAmount': float(row['TransactionAmount']),
                'TransactionDuration': float(row['TransactionDuration']),
                'LoginAttempts': int(row['LoginAttempts']),
                'AccountBalance': float(row['AccountBalance']),
                'CustomerAge': int(row['CustomerAge'])
            }
            
            # Include AccountID if it exists (for grouping suspicious accounts)
            if 'AccountID' in df.columns:
                transaction['AccountID'] = str(row['AccountID'])
            
            # Include TransactionID if it exists in the uploaded file
            if 'TransactionID' in df.columns:
                transaction['TransactionID'] = str(row['TransactionID'])
            else:
                transaction['TransactionID'] = f'TXN{str(idx + 1).zfill(4)}'
            
            transactions_to_process.append(transaction)
        
        # Process all transactions asynchronously in batches
        print(f"Processing {len(transactions_to_process)} transactions...")
        if ML_API_ENDPOINT and len(transactions_to_process) > 10:
            # Use async batch processing for better performance
            predictions = run_async_processing(transactions_to_process)
        else:
            # Use synchronous processing for small batches or mock mode
            predictions = [call_ml_api(txn) for txn in transactions_to_process]
        
        # Combine transactions with predictions
        for transaction, prediction in zip(transactions_to_process, predictions):
            transaction['fraud_or_not'] = prediction['fraud_or_not']
            transaction['fraud_score'] = prediction['fraud_score']
            
            results.append(transaction)
            
            if transaction['fraud_or_not'] == 1:
                fraudulent_transactions.append(transaction)
        
        print(f"✓ Processed {len(results)} transactions, found {len(fraudulent_transactions)} fraudulent")
        
        return jsonify({
            'total_transactions': len(results),
            'fraudulent_count': len(fraudulent_transactions),
            'fraudulent_transactions': fraudulent_transactions,
            'ml_mock_mode': not ML_API_AVAILABLE
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/api/explain', methods=['POST'])
def explain_fraud():
    """Get fraud explanation from Azure OpenAI"""
    print("📝 /api/explain endpoint called")
    data = request.json
    print(f"   Transaction data: {data}")
    
    if not data:
        print("❌ No transaction data provided")
        return jsonify({'error': 'No transaction data provided'}), 400
    
    try:
        print("   Calling call_azure_openai()...")
        result = call_azure_openai(data)
        print(f"   Got result: used_openai={result.get('used_openai')}, error={result.get('error')}")
        
        return jsonify({
            'explanation': result['explanation'],
            'openai_mock_mode': not result['used_openai'],
            'used_openai': result['used_openai'],
            'error': result.get('error')
        })
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"❌ Exception in explain_fraud: {error_msg}")
        return jsonify({'error': f'Error generating explanation: {error_msg}'}), 500


@app.route('/')
def serve_frontend():
    """Serve React frontend"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🚀 Starting Anti-Scam Dashboard API...")
    print(f"📊 Mock Mode: {'ENABLED' if not ML_API_ENDPOINT else 'DISABLED'}")
    print(f"🤖 ML API: {'Not Configured' if not ML_API_ENDPOINT else f'Configured at {ML_API_ENDPOINT}'}")
    print(f"🧠 Azure OpenAI: {'Not Configured' if not (AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY) else 'Configured'}")
    print(f"🌐 Port: {port}")
    print(f"⚡ Async Processing: Enabled (Batch size: {BATCH_SIZE}, Max concurrent: {MAX_CONCURRENT_REQUESTS})")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
