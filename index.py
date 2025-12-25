"""
Python script to read index.csv file, generate html table from its contents, and replace <table> tag in an HTML file with the generated table.
"""
import pandas as pd
from loguru import logger


def generate_html_table_from_csv(csv_file, html_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Generate HTML table from DataFrame
    html_table = df.to_html(index=False, classes='table table-striped', border=0)

    # add hyperlinks to "Blog" column
    if 'Blog' in df.columns:
        for i, row in df.iterrows():
            blog_url = row['Blog']
            html_table = html_table.replace(f'>{blog_url}<', f'><a href="{blog_url}">{blog_url}</a><')

    # add "class="sortable"" to the <table> tag
    html_table = html_table.replace('<table ', '<table class="sortable" ')

    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Replace the <table> tag with the generated HTML table
    start_index = html_content.find('<table')
    end_index = html_content.find('</table>') + len('</table>')
    if start_index != -1 and end_index != -1:
        new_html_content = html_content[:start_index] + html_table + html_content[end_index:]
    else:
        print("No <table> tag found in the HTML file.")
        return

    # Write the modified HTML content back to the file
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(new_html_content)
    logger.info(f"Replaced <table> tag in {html_file} with generated HTML table from {csv_file}.")


def main():
    csv_file = 'index.csv'
    html_file = 'index.html'
    logger.info("Generating HTML table from {} and updating {}", csv_file, html_file)
    generate_html_table_from_csv('index.csv', 'index.html')


if __name__ == "__main__":
    main()