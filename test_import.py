import sys
print(f"Python path: {sys.path}")
try:
    from sentence_transformers import SentenceTransformer
    print("✓ Successfully imported sentence_transformers")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Successfully loaded model")
except Exception as e:
    print(f"✗ Error importing sentence_transformers: {e}")
    import traceback
    traceback.print_exc()
