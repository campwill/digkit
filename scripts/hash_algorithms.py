import hashlib
import os

ALGORITHMS = ["md5", "sha1", "sha256"]

def calculate_file_hash(file_path, algorithm, output_dir=None):
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")

    write_to_file = output_dir is not None
    output_dir = output_dir or "."
    if write_to_file:
        os.makedirs(output_dir, exist_ok=True) 

    try:
        if algorithm == 'md5':
            hash_func = hashlib.md5()
        elif algorithm == 'sha1':
            hash_func = hashlib.sha1()
        elif algorithm == 'sha256':
            hash_func = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)

        hash_value = hash_func.hexdigest()
        output_text = f"{algorithm.upper()} ({file_path}): {hash_value}"

        if write_to_file:
            filename = os.path.join(output_dir, f"{os.path.basename(file_path)}.{algorithm}.txt")
            with open(filename, "w") as out_file:
                out_file.write(output_text + "\n")
            print(f"Hash saved to {filename}")
        else:
            print(output_text)
            
        return hash_value

    except Exception as e:
        return f"An error occurred: {e}"
    
    # add comparitive hash function