#!/bin/bash
# ===============================================
# � Thrift 多文件编译脚本 for camera_debug 项目
# 功能：自动扫描 ../thrift/ 目录中的所有 .thrift 文件
#       并输出生成的 Python 接口文件到 ../thrift/gen-py
# ===============================================

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
THRIFT_DIR="${PROJECT_ROOT}/thrift"
OUTPUT_DIR="${THRIFT_DIR}/gen-py"

# 进入 thrift 文件所在目录
cd "$THRIFT_DIR" || { echo "❌ 无法进入 thrift 目录"; exit 1; }

# 如果 gen-py 目录不存在则创建
mkdir -p "$OUTPUT_DIR"

# 检查 thrift 是否已安装
if ! command -v thrift &> /dev/null; then
    echo "❌ thrift 未安装。请运行以下命令之一安装："
    echo "   sudo apt install thrift"
    echo "   或 pip install thrift"
    exit 1
fi

# 编译所有 .thrift 文件
for file in *.thrift; do
    if [ -f "$file" ]; then
        echo "� 编译：$file ..."
        thrift -r --gen py -out "$OUTPUT_DIR" "$file"
        if [ $? -eq 0 ]; then
            echo "✅ 成功：$file"
        else
            echo "❌ 失败：$file"
        fi
    fi
    echo " "
done

# 在 gen-py 下的所有目录添加 __init__.py
find "$OUTPUT_DIR" -type d -exec touch {}/__init__.py \;