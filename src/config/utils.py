import os
import json
import configparser
from dataclasses import dataclass, asdict, field



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEVICE_CONFIG_DIR = os.path.join(BASE_DIR, "device_config")
CAMERA_INI_PATH = os.path.join(DEVICE_CONFIG_DIR, "cameras.ini")    # cameras.ini 文件路径
SCHEME_DIR = os.path.join(DEVICE_CONFIG_DIR, "schemes")             # schemesi 文件夹路径



@dataclass
class SchemeConfig:
    """
    这个类仅用于临时存储方案数据
    """
    exposure_time: int = 0              # 曝光时间
    gain: int = 0                       # 增益
    focal_length_step: int = 0          # 焦距步进
    focal_point: int = 0                # 焦点位置

    white_balance_R: str = ""           # R
    white_balance_G: str = ""           # G
    white_balance_B: str = ""           # B

    tools: list = None                  # 工具
    image_path: str = ""                # 存图路径

    scheme_name: str = ""               # 方案名称
    scheme_path: str = SCHEME_DIR       # 该方案存储路径（仅现阶段使用，因为要存储在本地）


@dataclass
class CameraConfig:
    name: str = ""
    ip: str = ""
    port: int = None
    current_scheme: str = ""                         # 当前方案名称
    schemes: list = field(default_factory=list)      # 所有方案名称

    def clear(self):
        self.name = ""
        self.ip = ""
        self.port = None
        self.current_scheme = ""
        self.schemes.clear()



def get_all_cameras():
    """
    从配置文件中获取所有相机的名称、ip、端口
    Return: cameras_ip_map
        key1: cam1
        value1: 127.0.0.1:9090
        key2: cam2
        value2: 127.0.0.1:9090
    """
    config = configparser.ConfigParser()
    config.read(CAMERA_INI_PATH, encoding="utf-8")
    cameras_ip_map = dict(config["cameras"])
    return cameras_ip_map


def load_scheme_from_file(json_path):
    """
    从 JSON 文件读取方案并转成 SchemeConfig
    """
    if not os.path.exists(json_path):
        return None

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return SchemeConfig(
        exposure_time=data.get("exposure_time", 0),
        gain=data.get("gain", 0),
        focal_length_step=data.get("focal_length_step", 0),
        focal_point=data.get("focal_point", 0),

        white_balance_R=data.get("white_balance_R", ""),
        white_balance_G=data.get("white_balance_G", ""),
        white_balance_B=data.get("white_balance_B", ""),

        tools=data.get("tools", []),
        image_path=data.get("image_path", ""),

        scheme_name=data.get("scheme_name", ""),
        scheme_path=data.get("scheme_path", "")
    )


def save_scheme_config(scheme_config):
    """
    将 SchemeConfig 保存为 JSON 文件
    """
    # 1. 校验 scheme_path
    if not scheme_config.scheme_path:
        raise ValueError("scheme_path 不能为空！")

    # 自动创建目录
    if not os.path.exists(scheme_config.scheme_path):
        os.makedirs(scheme_config.scheme_path)

    # 2. 校验方案名称
    if not scheme_config.scheme_name:
        raise ValueError("scheme_name 不能为空！")

    # 3. 生成完整路径
    file_path = os.path.join(
        scheme_config.scheme_path,
        scheme_config.scheme_name + ".json"
    )

    # 4. 将 dataclass 转换为字典
    scheme_dict = asdict(scheme_config)

    # 5. 写入 JSON
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(scheme_dict, f, ensure_ascii=False, indent=4)
        return True, file_path

    except Exception as e:
        return False, str(e)


def get_ip_and_port_by_camera_name(cam_name, cameras: dict):
    """
    根据相机名获取 ip 和 port
    """
    if cam_name not in cameras:
        raise ValueError(f"未找到相机配置: {cam_name}")

    addr = cameras[cam_name]

    if ":" not in addr:
        raise ValueError(f"相机地址格式错误: {addr}，应为 ip:port")

    ip, port_str = addr.split(":", 1)
    return ip.strip(), int(port_str.strip())


def get_schemes(camera_name: str):
    """
    获取当前相机的当前方案与备选方案
    Return: current_scheme_name, scheme_list
    """
    config = configparser.ConfigParser()
    config.read(CAMERA_INI_PATH, encoding="utf-8")

    section_name = f"schemes.{camera_name}"

    if section_name not in config:
        raise ValueError(f"未找到相机【{camera_name}】的方案配置")

    # 1️、读取当前方案名
    current_scheme_name = config[section_name].get("current_scheme", "").strip()

    # 2、读取方案列表
    schemes_str = config[section_name].get("schemes", "")
    scheme_list = [s.strip() for s in schemes_str.split(",") if s.strip()]

    # 3、兜底逻辑（防止 ini 写错）
    if current_scheme_name is None and scheme_list:
        print(f"⚠ 当前方案未找到，默认使用第一个方案: {scheme_list[0]}")
        current_scheme_name = scheme_list[0]

    return current_scheme_name, scheme_list


def get_scheme_config_by_name(scheme_name: str) -> SchemeConfig | None:
    """
    根据方案名称，从文件中获取配置并返回 SchemeConfig 结构体
    Args:
        scheme_name:
    Returns:
        SchemeConfig | None
    """
    if not scheme_name:
        print(f"解析失败方案文件名为空")
        return None

    json_path = os.path.join(SCHEME_DIR, scheme_name + ".json")

    scheme_config = load_scheme_from_file(json_path)
    if not scheme_config:
        print(f"方案文件不存在或解析失败: {json_path}")
        return None

    return scheme_config





def main():
    current_scheme_name, scheme_list = get_schemes("cam2")
    print(current_scheme_name)
    print(scheme_list)

    scheme_config = get_scheme_config_by_name(current_scheme_name)
    print(scheme_config)



if __name__ == "__main__":
    main()


