import sys
import yaml

target = sys.argv[1] if len(sys.argv) > 1 else "dev"

# Read the deployment-manifest.yml
with open("deployment-manifest.yml") as f:
    manifest = yaml.safe_load(f)

resources = manifest.get(target)
if not resources:
    print(f"No resources found for target '{target}'.")
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

print(f"Overwrite databricks.yml for target: {target}")
