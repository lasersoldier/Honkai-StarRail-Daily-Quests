import os
import subprocess

def install_requirements():
    # 获取当前工作目录
    current_dir = os.getcwd()
    
    # 查找 requirements.txt 文件
    requirements_file = os.path.join(current_dir, 'requirements.txt')
    
    if os.path.isfile(requirements_file):
        print(f"Found requirements.txt at {requirements_file}")
        try:
            # 使用 pip 安装依赖项
            result = subprocess.run(["pip", "install", "-r", requirements_file], capture_output=True, text=True)
            if result.returncode == 0:
                print("All dependencies installed successfully.")
            else:
                print(f"Error occurred: {result.stderr}")
        except Exception as e:
            print(f"An exception occurred: {e}")
    else:
        print("requirements.txt not found in the current directory.")

if __name__ == "__main__":
    install_requirements()
    input("按任意键继续...")
