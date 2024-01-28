import os
import zipfile


def unpack_crx(crx_path):
    output_dir = crx_path.replace(".crx", "")

    if not os.path.exists(output_dir):
        with open(crx_path, "rb") as crx_file:
            crx_file.seek(16)  # Skip the CRX header
            with open(output_dir + ".zip", "wb") as zip_file:
                zip_file.write(crx_file.read())

        with zipfile.ZipFile(output_dir + ".zip", "r") as zip_ref:
            zip_ref.extractall(output_dir)

        os.remove(output_dir + ".zip")

    return output_dir
