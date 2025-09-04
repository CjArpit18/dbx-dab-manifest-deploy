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

# Always include all src/ code
resources.append("src/**")

# Read the original databricks.yml
with open("databricks.yml") as f:
    bundle_config = yaml.safe_load(f)

# Add the include section
bundle_config['include'] = resources

# Write the generated config to a temp file
with open(".github/workflows/generated_databricks.yml", "w") as f:
    yaml.dump(bundle_config, f, default_flow_style=False)

print(f"Generated .github/workflows/generated_databricks.yml for target: {target}")
