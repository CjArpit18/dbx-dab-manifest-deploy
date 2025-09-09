import sys
import yaml
import os

target = sys.argv[1] if len(sys.argv) > 1 else "dev"
manifest_file = f"deployment-manifest-{target}.yml"

if not os.path.isfile(manifest_file):
    print(f"Manifest file '{manifest_file}' does not exist for target '{target}'.")
    sys.exit(1)

# Read the corresponding deployment manifest file
with open(manifest_file) as f:
    resources = yaml.safe_load(f)

if not resources:
    print(f"No resources found in manifest file '{manifest_file}'.")
    sys.exit(1)

# Read the original databricks.yml
with open("databricks.yml") as f:
    bundle_config = yaml.safe_load(f)

# Include only resource files (YAML/JSON)
bundle_config['include'] = resources

# Sync code/notebooks/etc. (add more as needed)
bundle_config.setdefault('sync', {})
bundle_config['sync']['include'] = ["src/**"]

# Write the generated config to databricks.yml (overwrite)
with open("databricks.yml", "w") as f:
    yaml.dump(bundle_config, f, default_flow_style=False)

print(f"Overwrite databricks.yml for target: {target} using manifest: {manifest_file}")
