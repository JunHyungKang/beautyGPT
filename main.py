import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import os
import openai

load_dotenv()


def table_to_markdown(table):
    headers = [cell["text"] for cell in table["columns"]]
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"

    rows = []
    for row in table["rows"]:
        row_data = [cell["text"] for cell in row]
        rows.append("| " + " | ".join(row_data) + " |")

    markdown_table = "\n".join([header_row, separator_row] + rows)
    return markdown_table


def analyze_doc(image_path):
    endpoint = os.getenv("FORM_URL")
    key = os.getenv("FORM_API_KEY")
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(image_path, "rb") as file:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=file
        )
    result = poller.result()

    full_contents = result.content
    markdown_tables = []
    if len(result.tables):
        for table in result.tables:
            markdown_tables.append(table_to_markdown(table))

    return full_contents + "\n".join(markdown_tables)


def get_model():
    openai.organization = os.getenv("OPENAI_ORG")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model_list = [x['id'] for x in openai.Model.list()['data']]
    for model_name in model_list:
        print(model_name)
    # chat = ChatOpenAI(temperature=0)


if __name__ == "__main__":
    image_path = "img/test_1.jpg"
    # contents = analyze_doc(image_path)
    # print(contents)

    get_model()
