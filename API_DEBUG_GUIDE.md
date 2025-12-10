# Qwen2-VL API Call Flow - Debug Guide

## Current Code Flow

### 1. **API Endpoint** (line 32)
```
URL: https://api-inference.huggingface.co/models/Qwen/Qwen2-VL-2B-Instruct
Method: POST
```

### 2. **Request Format** (lines 145-183: `createRequestJson()`)

The code creates this JSON structure:
```json
{
  "inputs": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Look at this drawing..."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,<base64_data>"
          }
        }
      ]
    }
  ],
  "parameters": {
    "max_new_tokens": 500,
    "temperature": 0.7
  }
}
```

### 3. **HTTP Headers** (lines 90-93)
```
Content-Type: application/json
Authorization: Bearer <api_key>
```

### 4. **Network Request** (line 96)
```cpp
m_currentReply = m_networkManager->post(request, data);
```

### 5. **Response Handling** (lines 185-317: `onNetworkReplyFinished()`)

## Potential Problems

### Problem 1: **Wrong Request Format** ⚠️ MOST LIKELY

The Hugging Face Inference API for vision-language models might NOT accept the OpenAI-style messages format. 

**What Hugging Face Inference API actually expects:**
- For text generation: `{"inputs": "text string"}`
- For vision models: The format might be different

**Check:** The Qwen2-VL model might need:
```json
{
  "inputs": {
    "text": "prompt text",
    "image": "base64_image_data"
  }
}
```

OR it might need a different endpoint entirely.

### Problem 2: **API Endpoint Issue**

The endpoint `https://api-inference.huggingface.co/models/Qwen/Qwen2-VL-2B-Instruct` might:
- Not support vision inputs via Inference API
- Require a different endpoint (like `/v1/chat/completions` if using OpenAI-compatible API)
- Need the model to be loaded first (503 error)

### Problem 3: **Response Never Arrives**

If `onNetworkReplyFinished()` is never called, it means:
- The request is hanging (network issue)
- The server is not responding
- SSL/TLS handshake failed
- Firewall blocking the connection

### Problem 4: **API Key Issue**

- API key might be invalid
- API key might not have correct permissions
- API key format might be wrong

## How to Debug

### Step 1: Check if Request is Sent
Add this debug output in `analyzeSketch()`:
```cpp
qDebug() << "Request JSON:" << QString::fromUtf8(data);
qDebug() << "Request URL:" << m_apiUrl;
qDebug() << "API Key (first 10 chars):" << m_apiKey.left(10);
```

### Step 2: Check if Response Arrives
The `onNetworkReplyFinished()` function should be called. Check:
- Is it being called at all?
- What HTTP status code is returned?
- What is the response body?

### Step 3: Test API Manually
Use curl or Postman to test the API:

```bash
curl -X POST https://api-inference.huggingface.co/models/Qwen/Qwen2-VL-2B-Instruct \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "test"}'
```

### Step 4: Check Network Errors
In `onNetworkReplyFinished()`, check:
```cpp
qDebug() << "Network Error Code:" << reply->error();
qDebug() << "Network Error String:" << reply->errorString();
qDebug() << "HTTP Status:" << statusCode;
qDebug() << "Response:" << QString::fromUtf8(responseData);
```

## Most Likely Issue

**The request format is probably wrong.** Hugging Face Inference API for vision models likely doesn't use the OpenAI messages format. You need to check the actual API documentation for Qwen2-VL-2B-Instruct to see what format it expects.

## Next Steps

1. Add more debug output to see what's actually being sent
2. Check if `onNetworkReplyFinished()` is being called
3. Test the API endpoint manually with curl
4. Verify the correct request format from Hugging Face documentation

