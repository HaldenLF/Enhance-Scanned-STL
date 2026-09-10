"""
Batch-repair-and-sharpen STL/OBJ files across nested folders.

Walks input_folder recursively and, for every .stl/.obj file found,
launches mesh_worker.py as a SEPARATE subprocess to run the verified
MeshLab filter script (cleanup -> manifold repair -> uniform
resampling -> Taubin smoothing -> Unsharp Mask sharpening). Results
go to output_folder, mirroring the same folder structure and
filenames.

Each subprocess's console output is redirected straight to a log
file using subprocess's normal stdout/stderr arguments.

Up to MAX_WORKERS files are processed in parallel.

Usage:
    pip install pymeshlab tqdm
    python enhance_scanned_stl.py
"""

import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


input_folder = r"\Low Quality"
output_folder = r"\Sharpened"
script_path = r"\sharpen_pipeline_clean.mlx"
log_path = r"\meshlab_log.txt"
worker_script = r"\worker.py"

valid_extensions = (".stl", ".obj")
MAX_WORKERS = 3
# ---------------------------


def find_tasks():
    tasks = []
    for root, dirs, files in os.walk(input_folder):
        rel_path = os.path.relpath(root, input_folder)
        target_dir = os.path.join(output_folder, rel_path) if rel_path != "." else output_folder
        os.makedirs(target_dir, exist_ok=True)

        for filename in files:
            if filename.lower().endswith(valid_extensions):
                tasks.append((
                    os.path.join(root, filename),
                    os.path.join(target_dir, filename),
                ))
    return tasks


def run_one(input_path, output_path, log_file_handle):
    result = subprocess.run(
        [sys.executable, worker_script, input_path, output_path, script_path],
        stdout=log_file_handle,
        stderr=log_file_handle,
    )
    return (input_path, result.returncode == 0)


def main():
    if not os.path.isdir(input_folder):
        print(f"ERROR: input folder not found: {input_folder}")
        return
    if not os.path.isfile(script_path):
        print(f"ERROR: filter script not found: {script_path}")
        return
    if not os.path.isfile(worker_script):
        print(f"ERROR: worker script not found: {worker_script}")
        return

    tasks = find_tasks()
    if not tasks:
        print("No matching .stl/.obj files found.")
        return

    print(f"Found {len(tasks)} file(s). Processing with {MAX_WORKERS} worker(s).")
    print(f"Subprocess output is being logged to: {log_path}\n")

    processed, failed = 0, []

    with open(log_path, "a") as log_file_handle:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(run_one, in_path, out_path, log_file_handle): in_path
                for in_path, out_path in tasks
            }
            with tqdm(total=len(tasks), unit="file", desc="Sharpening") as pbar:
                for future in as_completed(futures):
                    input_path, success = future.result()
                    if success:
                        processed += 1
                    else:
                        rel = os.path.relpath(input_path, input_folder)
                        failed.append(input_path)
                        tqdm.write(f"FAIL: {rel} -> see log for details")
                    pbar.update(1)

    print(f"\nDone. Processed {processed}/{len(tasks)} file(s).")
    if failed:
        print(f"{len(failed)} file(s) failed -- see {log_path} for details:")
        for path in failed:
            print(f"  {path}")


if __name__ == "__main__":
    main()