# Upwork System/Automation Scripts/sync_templates.py
from pathlib import Path
import shutil

# --- Configuration ---
# Define the source and destination directories relative to this script's location.
SCRIPT_DIR = Path(__file__).parent
SOURCE_DIR = SCRIPT_DIR / "../Master Templates"
DEST_DIR = SCRIPT_DIR / "LocalPython/templates"

def run_sync():
    """
    Finds all `*_master.md` files in the source directory,
    and creates a clean .txt copy in the destination directory.
    """
    print("--- Starting Template Sync ---")
    
    # 1. Ensure the source directory exists
    if not SOURCE_DIR.is_dir():
        print(f"❌ ERROR: Source directory not found at: {SOURCE_DIR}")
        return

    # 2. Ensure the destination directory exists, create it if not
    DEST_DIR.mkdir(exist_ok=True)
    print(f"Source:      {SOURCE_DIR.resolve()}")
    print(f"Destination: {DEST_DIR.resolve()}")

    # 3. Find all master templates recursively (ignores variations)
    master_templates = list(SOURCE_DIR.rglob("*_master.md"))

    if not master_templates:
        print("⚠️ WARNING: No `*_master.md` files found in the source directory.")
        return

    print(f"\nFound {len(master_templates)} master template(s) to sync...")

    # 4. Copy and rename each template
    synced_count = 0
    for md_path in master_templates:
        # Create the new filename, e.g., `automation_master.txt`
        txt_filename = md_path.stem + ".txt"
        dest_path = DEST_DIR / txt_filename

        try:
            # shutil.copy is a simple way to copy the file content
            shutil.copy(md_path, dest_path)
            print(f"  ✅ Synced: {md_path.name} -> {txt_filename}")
            synced_count += 1
        except Exception as e:
            print(f"  ❌ FAILED to sync {md_path.name}: {e}")

    print(f"\n--- Sync Complete. {synced_count} templates updated. ---")


if __name__ == "__main__":
    run_sync()