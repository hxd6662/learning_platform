import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage.database.mysql_db import init_db, get_engine, Base
from src.models.user import User
from src.models.learning import LearningStat, LearningGoal
from src.models.question import WrongQuestion, LearningResource
from src.models.health import HealthRecord, AIConversation

def init_database():
    print("开始初始化数据库...")
    
    try:
        init_db()
        print("数据库表创建成功！")
        
        engine = get_engine()
        print("\n已创建的表：")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
        print("\n数据库初始化完成！")
        return True
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
