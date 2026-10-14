from pathlib import Path
import subprocess
import sys


project_folder = Path(__file__).resolve().parent.parent

steps = [
    "inspect_data.py",
    "clean_data.py",
    "enrich_data.py",
    "generate_insights.py",
    "generate_finding.py",
]

for step in steps:
    script_path = project_folder / "src" / step

    print(f"\nRunning {step}...")
    print("-" * 40)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=project_folder
    )

    if result.returncode != 0:
        print(f"\nPipeline stopped because {step} failed.")
        sys.exit(result.returncode)

print("\nPipeline successful.")