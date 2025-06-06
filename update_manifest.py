import os
from pathlib import Path

SUPPORT_URL = os.environ.get("SUPPORT_URL", "https://example.com/help")
APP_DOMAIN = os.environ.get("APP_DOMAIN", "https://example.com")

manifest_path = Path("manifest.xml")
output_path = Path("manifest.build.xml")

text = manifest_path.read_text()
text = text.replace("{{SUPPORT_URL}}", SUPPORT_URL)
text = text.replace("{{APP_DOMAIN}}", APP_DOMAIN)
output_path.write_text(text)
print(f"Wrote {output_path}")
