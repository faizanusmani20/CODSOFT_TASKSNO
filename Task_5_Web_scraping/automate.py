import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Get the folder where this file is saved
project_folder = Path(__file__).resolve().parent


def run_file(file_name):
    print("\n--- Running", file_name, "---")

    subprocess.run(
        [sys.executable, str(project_folder / file_name)],
        cwd=project_folder,
        check=True
    )


if __name__ == "__main__":

    print("TASK 5 AUTOMATED PIPELINE")

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print("Started:", current_time)

    # Run all project files one by one
    run_file("scraper.py")
    run_file("clean_data.py")
    run_file("analysis.py")

    print("\nPipeline completed successfully.")
