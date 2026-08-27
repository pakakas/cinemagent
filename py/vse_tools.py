import sys
import os
import subprocess
import argparse

ACTIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "actions")

def main():
    parser = argparse.ArgumentParser(description="Blender VSE Action Delegator CLI")
    parser.add_argument("--action", type=str, required=True, help="Action name matching py/actions/<action>.py")
    args, unknown_args = parser.parse_known_args()

    action_script = os.path.join(ACTIONS_DIR, f"{args.action}.py")
    if not os.path.exists(action_script):
        print(f"❌ Error: Action '{args.action}' not found in {ACTIONS_DIR}")
        print(f"Available actions: {[f[:-3] for f in os.listdir(ACTIONS_DIR) if f.endswith('.py')]}")
        sys.exit(1)

    cmd = [sys.executable, action_script] + unknown_args
    res = subprocess.run(cmd, text=True)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
