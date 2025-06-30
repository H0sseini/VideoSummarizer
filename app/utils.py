import os

def ensure_model(path, hf_id, cls, **kwargs):
    if not os.path.exists(path):
        print(f"Downloading {hf_id} to {path}")
        obj = cls.from_pretrained(hf_id, **kwargs)
        obj.save_pretrained(path)
    else:
        print(f"Using cached model at {path} for {hf_id}")
        obj = cls.from_pretrained(path, **kwargs)
    return obj