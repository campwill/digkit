import csv
import os
import requests
import gnupg

def download_files_from_csv(input_csv, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_url = row.get('File_Link')
            file_name = row.get('File_Name')

            if not file_url or not file_name:
                print(f"Skipping row due to missing data: {row}")
                continue

            output_path = os.path.join(output_dir, file_name)

            try:
                print(f"Downloading: {file_name}")
                response = requests.get(file_url, stream=True)
                response.raise_for_status()

                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Saved to: {output_path}")

            except Exception as e:
                return f"An error occurred: {e}"

def decrypt_gpg_files_in_directory(input_dir, output_dir, passphrase):
    os.makedirs(output_dir, exist_ok=True)
    gpg = gnupg.GPG()  # uses system's GPG installation

    for filename in os.listdir(input_dir):
        if filename.endswith('.gpg'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename[:-4])

            print(f"Decrypting: {filename}")
            with open(input_path, 'rb') as f:
                status = gpg.decrypt_file(
                    f,
                    passphrase=passphrase,
                    output=output_path
                )

            if status.ok:
                print(f"Decrypted and saved to: {output_path}")
            else:
                print(f"Failed to decrypt {filename}: {status.status}, ensure is passphrase is correct and/or encapsulated with single quotes")

# add parse function