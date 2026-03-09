from nbconvert import MarkdownExporter
import nbformat
import os

# 1. Load notebook
nb_path = "7 docker-volumes-deep-hands-on.ipynb"
nb = nbformat.read(nb_path, as_version=4)

# 2. Configure exporter
exporter = MarkdownExporter()
body, resources = exporter.from_notebook_node(nb)

# 3. Save markdown file
md_path = "7 docker-volumes.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write(body)

# 4. Save extracted resources (images, etc.)
output_dir = "7 docker-volumes_files"
os.makedirs(output_dir, exist_ok=True)

for name, data in resources.get("outputs", {}).items():
    out_path = os.path.join(output_dir, name)
    with open(out_path, "wb") as f:
        f.write(data)