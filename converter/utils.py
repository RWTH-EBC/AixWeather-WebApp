import os
from io import BytesIO
import base64

from django.core.files.storage import FileSystemStorage

# create a singular root directory
root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))


# Function to handle data upload
def handle_uploaded_file(f):
    """
    Import file and return the path to file, at the same time delete older file
        Parameter:
            f: (file)
        Return
            path
    """
    fs = FileSystemStorage()
    path = os.path.join(fs.location, f.name)
    for file in fs.listdir(fs.location)[1]:
        if file:
            fs.delete(file)

    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path


def render_graph(plt):
    """Function plotly to render graph to html supported format"""
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return string.decode("utf-8")


def create_unique_result_folder():
    """
    This function generates folder names in the format "data_i" (e.g., "data_0", "data_1") and makes sure that each
    webapp run uses a unique result folder.
    This function returns the folder path and creates the directory.
    """
    folder_path = os.path.join(root_dir, "results")

    i = 0
    while True:
        # Construct the path for the potential data folder using an f-string
        result_path = os.path.join(folder_path, f"data_{i}", f"data_{i}")

        # Check if the folder with this name already exists
        if not os.path.exists(result_path):
            # If it doesn't exist, create the folder and return its path
            os.makedirs(result_path)

            print(f"created the following results path: {result_path}")
            return result_path
        i += 1
