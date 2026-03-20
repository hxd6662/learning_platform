import os
import base64
import json
from dotenv import load_dotenv
import requests
import hashlib
import hmac
from datetime import datetime
from urllib.parse import quote, urlencode

load_dotenv()

class AliyunOCRService:
    def __init__(self):
        self.access_key_id = os.getenv("ALIYUN_OCR_ACCESS_KEY_ID")
        self.access_key_secret = os.getenv("ALIYUN_OCR_ACCESS_KEY_SECRET")
        self.endpoint = "ocr-api.cn-hangzhou.aliyuncs.com"
        self.region = "cn-hangzhou"
        self.api_version = "2021-07-07"
        self.is_available = self.access_key_id and self.access_key_secret and \
                         self.access_key_id != "your-aliyun-access-key-id"
    
    def _sign(self, params):
        sorted_params = sorted(params.items())
        canonicalized_query_string = '&'.join([f'{quote(k, safe="~")}={quote(v, safe="~")}' for k, v in sorted_params])
        
        string_to_sign = f'POST&%2F&{quote(canonicalized_query_string, safe="~")}'
        
        key = self.access_key_secret + '&'
        signature = hmac.new(key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()
        signature = base64.b64encode(signature).decode('utf-8')
        
        return signature
    
    def recognize_text(self, image_data: bytes = None, image_url: str = None) -> dict:
        if not self.is_available:
            return {
                "text": "阿里云OCR服务未配置，这是模拟识别结果。\n在实际应用中，这里会调用阿里云OCR API。",
                "confidence": 0.95,
                "lines": [
                    {"text": "题目：解方程 2x + 5 = 15", "confidence": 0.98},
                    {"text": "A. x=5", "confidence": 0.96},
                    {"text": "B. x=10", "confidence": 0.95}
                ]
            }
        
        try:
            params = {
                "Action": "RecognizeGeneral",
                "Format": "JSON",
                "Version": self.api_version,
                "SignatureMethod": "HMAC-SHA1",
                "SignatureVersion": "1.0",
                "SignatureNonce": str(int(datetime.now().timestamp() * 1000)),
                "Timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "AccessKeyId": self.access_key_id,
            }
            
            if image_data:
                params["ImageURL"] = ""
                params["ImageData"] = base64.b64encode(image_data).decode('utf-8')
            elif image_url:
                params["ImageURL"] = image_url
            else:
                return {"error": "Either image_data or image_url is required"}
            
            params["Signature"] = self._sign(params)
            
            url = f"https://{self.endpoint}/"
            response = requests.post(url, data=params, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("Code") == "200" or result.get("Status") == "OK":
                    data = result.get("Data", {})
                    texts = []
                    lines = []
                    
                    if "Words" in data:
                        for word in data["Words"]:
                            texts.append(word.get("Word", ""))
                            lines.append({
                                "text": word.get("Word", ""),
                                "confidence": word.get("Probability", 0.9)
                            })
                    
                    return {
                        "text": "\n".join(texts),
                        "confidence": 0.95,
                        "lines": lines,
                        "raw_response": result
                    }
                else:
                    return {
                        "error": result.get("Message", "OCR recognition failed"),
                        "code": result.get("Code")
                    }
            else:
                return {"error": f"HTTP Error: {response.status_code}", "details": response.text}
                
        except Exception as e:
            return {
                "error": f"OCR Error: {str(e)}",
                "text": "这是模拟识别结果（阿里云OCR调用失败）。\n题目：解方程 2x + 5 = 15"
            }

_aliyun_ocr_service = None

def get_aliyun_ocr_service() -> AliyunOCRService:
    global _aliyun_ocr_service
    if _aliyun_ocr_service is None:
        _aliyun_ocr_service = AliyunOCRService()
    return _aliyun_ocr_service
