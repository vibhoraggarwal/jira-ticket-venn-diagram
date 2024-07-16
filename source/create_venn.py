import pandas as pd
from matplotlib_venn import venn3
import matplotlib.pyplot as plt
import requests

def download_csv(url, save_path):
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"CSV file downloaded and saved to {save_path}")

def load_data(file_path):
    return pd.read_csv(file_path)

def extract_issue_sets(df):
    stories = set(df[df['Issue Type'] == 'Story']['Issue key'])
    bugs = set(df[df['Issue Type'] == 'Bug']['Issue key'])
    tasks = set(df[df['Issue Type'] == 'Task']['Issue key'])
    return stories, bugs, tasks

def create_venn_diagram(stories, bugs, tasks):
    plt.figure(figsize=(10, 7))
    venn = venn3([stories, bugs, tasks], ('Story', 'Bug', 'Task'))

    # Annotate the counts inside the Venn diagram
    for idx, subset in enumerate(venn.subset_labels):
        if subset:
            subset.set_text(len(venn.get_label_by_id(venn.id2idx[idx])))
    
    plt.title("Venn Diagram of Jira Issues by Type")
    plt.show()

def main(url, file_path):
    download_csv(url, file_path)
    df = load_data(file_path)
    stories, bugs, tasks = extract_issue_sets(df)
    create_venn_diagram(stories, bugs, tasks)

# URL of the CSV file to be downloaded
csv_url = 'https://example.com/path/to/jira.csv'
# Path where the downloaded CSV file will be saved
file_path = 'jira_issues.csv'
main(csv_url, file_path)
