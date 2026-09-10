# Scanned STL Enhancement

This project prepares rough or low-quality scanned STL and OBJ files for 3D printing by processing them through a verified mesh repair and sharpening pipeline.

## Overview

The script in `enchance_scanned_stl.py` scans a source folder recursively, finds STL and OBJ files, and sends each file through a MeshLab filter script. The processed meshes are written to a separate output directory while preserving the original folder layout and filenames.

It is designed for noisy or imperfect scanned meshes that need cleaning before they are ready for printing.

## What the script does

- walks the input directory tree recursively
- finds matching `.stl` and `.obj` files
- loads each mesh with PyMeshLab
- applies the saved MeshLab filter script
- saves the repaired and sharpened file to the output folder
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

This combination is intended to remove scan noise, fix mesh defects, and sharpen detail for better printability.

## Files in this project

- `enchance_scanned_stl.py` — batch processing script
- `sharpen_pipeline_clean.mlx` — verified MeshLab filter script
- Test different 

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
script_path = r"\sharpen_pipeline_clean.mlx"
```

You can also adjust how many files are processed at once:

```python
MAX_WORKERS = 3
```

## Usage

Run the script from the project folder:

```bash
python "enchance_scanned_stl.py"
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

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full terms.
