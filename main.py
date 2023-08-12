import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def table_to_markdown(table):
    headers = [cell['text'] for cell in table['columns']]
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"

    rows = []
    for row in table['rows']:
        row_data = [cell['text'] for cell in row]
        rows.append("| " + " | ".join(row_data) + " |")

    markdown_table = "\n".join([header_row, separator_row] + rows)
    return markdown_table


def analyze_doc(image_path):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(image_path, "rb") as file:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=file
        )
    result = poller.result()

    full_contents = result.content
    if len(result.tables):
        markdown_tables = []
        for table in result.tables:
            markdown_tables.append(table_to_markdown(table))


if __name__ == "__main__":
    load_dotenv()
    endpoint = os.getenv("FORM_URL")
    key = os.getenv("FORM_API_KEY")

    image_path = "/Users/jhkang/PycharmProjects/olive/img/test_1.jpg"
    analyze_doc(image_path)
