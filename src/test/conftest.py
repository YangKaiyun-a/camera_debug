import threading
import time
import pytest
from src.test.server import main as start_server


@pytest.fixture(scope="session", autouse=True)
def thrift_server():
    """
    ✅ 测试前自动启动 Thrift Server
    """
    print("✅ conftest.py 已加载，thrift 服务启动中...")
    t = threading.Thread(target=start_server, daemon=True)
    # t.start()

    time.sleep(1)  # 等待服务启动
    yield

    # ✅ 测试结束自动退出（daemon 线程）
