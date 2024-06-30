import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(script):
    # 使用ctypes来提升权限运行脚本
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, script, None, 1)

if __name__ == "__main__":
    script_path = os.path.abspath("StarRailDaily.py")  # 修改为你的脚本路径

    if is_admin():
        # 如果已经是管理员，直接运行脚本
        with open(script_path) as f:
            exec(f.read())
    else:
        # 以管理员身份重新运行脚本
        run_as_admin(script_path)
