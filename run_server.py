import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    print(f"启动服务器: http://{host}:{port}")
    print(f"API文档: http://localhost:{port}/docs")
    print("按 Ctrl+C 停止服务器")
    print()
    uvicorn.run("src.app:app", host=host, port=port)
