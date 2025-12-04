from dataclasses import dataclass


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
    save_path: str = ""                 # 存图路径
    scheme_name: str = ""               # 方案名称
