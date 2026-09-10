"""
Processes a single mesh file through the verified MeshLab filter
script. 

Usage:
    python mesh_worker.py <input_path> <output_path> <script_path>
"""

import sys
import pymeshlab


def main():
    input_path, output_path, script_path = sys.argv[1], sys.argv[2], sys.argv[3]
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_path)
    ms.load_filter_script(script_path)
    ms.apply_filter_script()
    ms.save_current_mesh(output_path)


if __name__ == "__main__":
    main()