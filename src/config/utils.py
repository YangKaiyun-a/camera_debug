import os
import json
from dataclasses import dataclass, asdict


# ========== 默认目录定义  根目录/schemes/ ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEFAULT_SCHEME_DIR = os.path.join(BASE_DIR, "schemes")

if not os.path.exists(DEFAULT_SCHEME_DIR):
    os.makedirs(DEFAULT_SCHEME_DIR)



@dataclass
class SchemeConfig:
    exposure_time: int = 0              # 曝光时间
    gain: int = 0                       # 增益
    focal_length_step: int = 0          # 焦距步进
    focal_point: int = 0                # 焦点位置

    white_balance_R: str = ""           # R
    white_balance_G: str = ""           # G
    white_balance_B: str = ""           # B

    tools: list = None                  # 工具
    image_path: str = ""                # 存图路径

    scheme_name: str = ""                        # 方案名称
    scheme_path: str = DEFAULT_SCHEME_DIR        # 该方案存储路径



def save_scheme_config(scheme):
    """
    将 SchemeConfig 保存为 JSON 文件
    """
    # 1. 校验 scheme_path
    if not scheme.scheme_path:
        raise ValueError("scheme_path 不能为空！")

    # 自动创建目录
    if not os.path.exists(scheme.scheme_path):
        os.makedirs(scheme.scheme_path)

    # 2. 校验方案名称
    if not scheme.scheme_name:
        raise ValueError("scheme_name 不能为空！")

    # 3. 生成完整路径
    file_path = os.path.join(
        scheme.scheme_path,
        scheme.scheme_name + ".json"
    )

    # 4. 将 dataclass 转换为字典
    scheme_dict = asdict(scheme)

    # 5. 写入 JSON
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(scheme_dict, f, ensure_ascii=False, indent=4)
        return True, file_path

    except Exception as e:
        return False, str(e)
