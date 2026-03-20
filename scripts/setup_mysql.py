import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from dotenv import load_dotenv

load_dotenv()

def create_database():
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "learning_platform")

    print("=" * 60)
    print("青少年智能学习平台 - 数据库设置")
    print("=" * 60)
    print()

    try:
        print(f"正在连接到MySQL服务器... (host: {host}, port: {port})")
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✓ MySQL连接成功！")
        print()

        with connection.cursor() as cursor:
            print(f"正在创建数据库 '{database}'...")
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print(f"✓ 数据库 '{database}' 创建成功！")
            print()

            cursor.execute(f"USE `{database}`")
            print("数据库已选中")
            print()

        connection.commit()
        connection.close()

        print("=" * 60)
        print("数据库设置完成！")
        print("=" * 60)
        print()
        print("现在可以运行以下命令初始化数据表：")
        print("  python scripts/init_db.py")
        print()
        return True

    except Exception as e:
        print(f"✗ 错误: {e}")
        print()
        print("请检查：")
        print("1. MySQL服务是否已启动")
        print("2. .env文件中的数据库配置是否正确")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_database()
    sys.exit(0 if success else 1)
