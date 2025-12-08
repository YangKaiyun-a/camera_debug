import os
import json
import configparser
from dataclasses import dataclass, asdict



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEVICE_CONFIG_DIR = os.path.join(BASE_DIR, "device_config")
CAMERA_INI_PATH = os.path.join(DEVICE_CONFIG_DIR, "cameras.ini")
SCHEME_DIR = os.path.join(DEVICE_CONFIG_DIR, "schemes")



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

    scheme_name: str = ""               # 方案名称
    scheme_path: str = SCHEME_DIR       # 该方案存储路径（仅现阶段使用，因为要存储在本地）


@dataclass
class CameraConfig:
    camera_name: str = ""                           # 相机名称
    camera_ip: str = ""                             # 相机ip
    camera_port: str = ""                           # 相机端口
    camera_current_scheme: SchemeConfig = None      # 相机当前方案
    camera_schemes: list = None                     # 相机所有方案



def get_all_cameras():
    """
    获取所有相机的名称、ip、端口
    TODO: 后续更改为从 thrift 接口获取
    """
    config = configparser.ConfigParser()
    config.read(CAMERA_INI_PATH, encoding="utf-8")
    cameras_ip_map = dict(config["cameras"])
    return cameras_ip_map



def load_camera_and_scheme_config():
    """
    加载配置文件
    """
    config = configparser.ConfigParser()
    config.read(CAMERA_INI_PATH, encoding="utf-8")

    cameras = dict(config["cameras"])

    default_camera = ""
    if "global" in config:
        default_camera = config["global"].get("default_camera", "")

    camera_schemes = {}
    for section in config.sections():
        if section.startswith("schemes."):
            cam_name = section.split(".", 1)[1]
            schemes_str = config[section].get("schemes", "")
            scheme_list = [s.strip() for s in schemes_str.split(",") if s.strip()]
            camera_schemes[cam_name] = scheme_list

    return cameras, camera_schemes, default_camera


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
    TODO: 后续会与 thrift 接口结合
    """
    config = configparser.ConfigParser()
    config.read(CAMERA_INI_PATH, encoding="utf-8")

    section_name = f"schemes.{camera_name}"

    if section_name not in config:
        raise ValueError(f"未找到相机【{camera_name}】的方案配置")

    # 1️⃣ 读取当前方案名
    current_scheme_name = config[section_name].get("current_scheme", "").strip()

    # 2️⃣ 读取方案列表
    schemes_str = config[section_name].get("schemes", "")
    scheme_names = [s.strip() for s in schemes_str.split(",") if s.strip()]

    scheme_list: list[SchemeConfig] = []
    current_scheme: SchemeConfig | None = None

    # 3️⃣ 逐个加载 json → SchemeConfig
    for scheme_name in scheme_names:
        json_path = os.path.join(SCHEME_DIR, scheme_name + ".json")

        scheme = load_scheme_from_file(json_path)
        if not scheme:
            print(f"⚠ 方案文件不存在或解析失败: {json_path}")
            continue

        scheme.scheme_name = scheme_name
        scheme.scheme_path = SCHEME_DIR

        scheme_list.append(scheme)

        # 4️⃣ 识别当前方案
        if scheme_name == current_scheme_name:
            current_scheme = scheme

    # 5️⃣ 兜底逻辑（防止 ini 写错）
    if current_scheme is None and scheme_list:
        print(f"⚠ 当前方案未找到，默认使用第一个方案: {scheme_list[0].scheme_name}")
        current_scheme = scheme_list[0]

    return current_scheme, scheme_list


