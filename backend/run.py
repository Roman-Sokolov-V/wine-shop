import shutil
import subprocess
from pathlib import Path
import sys

def main():
    project_dir = Path(__file__).parent.resolve()
    src = project_dir / ".env.sample"
    dst = project_dir / ".env"

    try:
        shutil.copyfile(src, dst)
        print(f"✅ Copied {src} → {dst}")
    except FileNotFoundError:
        print(f"❌ {src} not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        sys.exit(1)

    try:
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ docker-compose failed: {e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
