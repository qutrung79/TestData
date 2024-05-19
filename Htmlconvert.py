import os
from bs4 import BeautifulSoup

def html_to_text(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    return text_content

def convert_html_to_text_folder(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".html"):
                html_file_path = os.path.join(root, file)
                text_content = html_to_text(html_file_path)
                # Change file extension to .txt
                text_file_name = os.path.splitext(file)[0] + ".txt"
                text_file_path = os.path.join(output_folder, text_file_name)
                with open(text_file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)

# Example usage:
input_folder = "F:\Tesssata\HTLM"
output_folder = "stData\HTLM"
convert_html_to_text_folder(input_folder, output_folder)
