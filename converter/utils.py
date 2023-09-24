from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
from io import BytesIO,StringIO
import base64
import seaborn as sns
import os


fs = FileSystemStorage()

def handle_uploaded_file(f):
    '''
    Import file and return the path to file, at the same time delete older file
        Parameter:
            f: (file)
        Return
            path
    '''
    fs = FileSystemStorage()
    path = os.path.join(fs.location, f.name)
    for file in fs.listdir(fs.location)[1]:
            if file:
                fs.delete(file)

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path


def plot_heatmap_missing_values_daily(df):
    # Group by day and check for any missing values for each day
    missing_data = df.resample("D").apply(lambda x: x.isnull().any())

    # Determine the number of days (rows) in your dataframe
    num_days = missing_data.shape[0]

    # Set the height of the figure based on the number of days, and a fixed width
    plt.figure(figsize=(10, num_days * 0.15 + 3))

    sns.heatmap(missing_data, cmap="Greens_r", cbar=False)

    # Set y-tick labels to represent each day
    plt.yticks(range(num_days), missing_data.index.date, rotation=0)

    plt.title("Heatmap of Missing Values (white = missing)")
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    #plt.show()

    return string.decode('utf-8')