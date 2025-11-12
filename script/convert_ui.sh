#!/bin/bash
# ==============================================================
# 自动将 src/ui 下的 .ui 文件转换为对应的 .py 文件
# 使用 pyuic5（PyQt5）或 pyuic6（PyQt6）
# ==============================================================
# 使用方式：
#   1. 先激活虚拟环境： conda activate camera_debug
#   2. 然后运行： bash script/convert_ui.sh
# ==============================================================

# 检查 PyQt 工具是否存在
if command -v pyuic5 &>/dev/null; then
    UIC_CMD=pyuic5
elif command -v pyuic6 &>/dev/null; then
    UIC_CMD=pyuic6
else
    echo "❌ 请先激活安装了 PyQt 的虚拟环境。"
    echo "� 示例：conda activate camera_debug"
    exit 1
fi

# 设置源文件与目标目录
UI_DIR="$(dirname "$0")/../src/ui"
echo "� UI 源目录: $UI_DIR"
echo "⚙️  使用转换工具: $UIC_CMD"

# 检查是否存在 .ui 文件
shopt -s nullglob
UI_FILES=("$UI_DIR"/*.ui)
if [ ${#UI_FILES[@]} -eq 0 ]; then
    echo "⚠️ 未找到任何 .ui 文件。请确认文件位于 src/ui 目录下。"
    exit 0
fi

# 执行转换
for ui_file in "${UI_FILES[@]}"; do
    base_name=$(basename "${ui_file%.ui}")
    py_file="$UI_DIR/${base_name}.py"
    echo "� 转换: $ui_file → $py_file"
    $UIC_CMD "$ui_file" -o "$py_file"
done

echo "✅ 所有 UI 文件已成功转换为 Python 文件！"
