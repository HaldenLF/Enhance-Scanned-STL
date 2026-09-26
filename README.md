# Scanned STL Enhancement

This project prepares rough or low-quality scanned STL and OBJ files for 3D printing by processing them through a verified mesh repair and sharpening pipeline.

## Overview

The workflow uses a main controller script and a worker script:

- `enhanced.py` launches the batch process
- `worker.py` processes one mesh at a time inside a separate subprocess
- `pipeline.mlx` contains the verified MeshLab filter sequence

This setup is designed for large batches of scanned meshes but can be used for smaller batches. Time to completion depends on the size of the orignial file. It walks the input folder tree, preserves the original folder layout, and writes processed copies into a separate output directory.

## What the script does

- walks the input directory tree recursively
- finds matching `.stl` and `.obj` files
- loads each mesh with PyMeshLab
- applies the saved MeshLab filter script
- saves the repaired and sharpened file to the output folder as .stl
- keeps the same relative folder structure as the source
- runs several files in parallel using multiple worker processes
- displays a progress bar while processing

## Mesh processing pipeline

The applied filter sequence is:

1. cleanup
2. manifold repair
3. uniform resampling at 0.05
4. Taubin smoothing repeated 7 times
5. unsharp mask geometry repeated 5 times
6. close holes
7. reduce vertices amount by 50%
8. repeats repair steps

This is intended to remove scan noise, fix mesh defects, and sharpen detail for better quality prints.

## Files in this project

- `enhanced.py` — main batch controller
- `worker.py` — single-file processing worker
- `pipeline.mlx` — MeshLab filter script
- `meshlab_log.txt` — logfile for worker subprocess output

## Requirements

Install the required packages:

```bash
pip install pymeshlab tqdm
```

## Configuration

Edit the path values near the top of the script:

```python
input_folder = r"\Low Quality"
output_folder = r"\Sharpened"
script_path = r"\pipeline.mlx"
worker_script = r"\worker.py"
log_path = r"\meshlab_log.txt"
```

You can also adjust how many files are processed at once:

```python
MAX_WORKERS = 3
```

## Usage

Run the script from the project folder:

```bash
python "enchanced_stl.py"
```

The script will:

- scan the input folder
- detect supported mesh files
- process them in parallel
- print the overall result when complete
- list any files that failed during processing

## Output behaviour

- output keeps the same relative folder structure as the input
- original filename and file extension are preserved
- source files remain untouched
- output is written to a separate destination folder

## Example

```text
\Low Quality\Model A\scan.stl
```

becomes:

```text
\Sharpened\Model A\scan.stl
```

after cleanup, repair, resampling, smoothing, and sharpening.

## Notes

- Always keep backups of the original scan files.
- Test a small batch before processing a full collection.
- Check the result mesh before sending it to the printer.
- Some models may fail depending on topology, defects, or bad triangulation.
- - Since the worker output is redirected to `meshlab_log.txt`, the main terminal stays cleaner while failures can still be investigated.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full terms.
