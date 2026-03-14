"""
Script to initialise placeholder directories and .gitkeep files.
Run once after cloning: python setup.py
"""
import os

dirs = [
    "models", "data", "data/logos", "data/fonts", "assets", "notebooks",
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    gitkeep = os.path.join(d, ".gitkeep")
    if not os.path.exists(gitkeep):
        open(gitkeep, "w").close()
    print(f"Created: {d}/")

print("\n✓ Project directories initialised.")
print("Next steps:")
print("  1. Download datasets from Drive → place in data/")
print("  2. Add GEMINI_API_KEY to .streamlit/secrets.toml")
print("  3. Run: streamlit run app.py")
