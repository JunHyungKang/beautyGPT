import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import openai
from prompt_manager import Marketing, few_shot_prompt, system_prompt
import tqdm
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    PromptTemplate,
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.output_parsers import OutputFixingParser
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain import PromptTemplate, OpenAI, LLMChain


load_dotenv()


def table_to_markdown(table_data):
    rowCount = table_data.row_count
    columnCount = table_data.column_count
    cells = table_data.cells
    table = [["" for _ in range(columnCount)] for _ in range(rowCount)]

    for cell in cells:
        table[cell.row_index][cell.column_index] = cell.content

    markdown_table = []
    for row in table:
        markdown_table.append("| " + " | ".join(row) + " |")
    markdown_table.insert(1, "| " + " | ".join(["---"] * columnCount) + " |")

    return "\n".join(markdown_table)


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

    return full_contents + "\n".join(markdown_tables) + '\n'


def get_model(temp=0.7):
    openai.organization = os.getenv("OPENAI_ORG")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k',
                     temperature=temp,
                     openai_api_key=openai.api_key,
                     openai_organization=openai.organization,
                     request_timeout=60,
                     )
    return llm


def get_prompt(few_shot_prompt):
    final_prompt = ChatPromptTemplate.from_messages(
        [SystemMessagePromptTemplate.from_template(system_prompt),
         few_shot_prompt,
         HumanMessagePromptTemplate.from_template("###input\n{contents}"),
        ]
    )
    return final_prompt


if __name__ == "__main__":
    image_path = "img/test_1"
    contents = []
    txt_file = [x for x in os.listdir(image_path) if x.endswith('.txt')]
    if len(txt_file):
        with open(os.path.join(image_path, txt_file[0]), 'r') as f:
            contents = '\n'.join(f.readlines())
    else:
        for img_path in tqdm.tqdm(sorted(os.listdir(image_path))):
            contents.append(analyze_doc(os.path.join(image_path, img_path)))
        contents = '\n'.join(contents)
        with open(os.path.join(image_path, 'contents.txt'), 'w') as f:
            f.write(contents)

    parser = PydanticOutputParser(pydantic_object=Marketing)
    prompt = get_prompt(few_shot_prompt)
    chain = LLMChain(llm=get_model(0.7),
                     prompt=prompt,
                     verbose=True)

    target = "20대 외모에 신경쓰는 여성"
    result = chain.run(contents=contents, target=target, format_instructions=parser.get_format_instructions())
    new_parser = OutputFixingParser.from_llm(parser=parser, llm=get_model(0.0))
    new_parser.parse(result)
    print(result)
    print(new_parser.parse(result))