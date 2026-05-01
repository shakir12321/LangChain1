import argparse
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pypdf import PdfReader

def read_attachment(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()
    raise ValueError(
        f"Unsupported attachment type: {suffix}. Use .txt, .md, or .pdf"
    )


def build_chain(temperature: float):
    summary_template = """
Given the information below about a person:
{information}

Create:
1. A short summary
2. Two interesting facts about them
"""
    prompt = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )
    llm = ChatOllama(temperature=temperature, model="deepseek-r1:1.5b")
    return prompt | llm


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize person details from an attachment using local Ollama."
    )
    parser.add_argument(
        "--attachment",
        default="person.txt",
        help="Path to a .txt, .md, or .pdf file (default: person.txt).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="LLM temperature (default: 0.0).",
    )
    args = parser.parse_args()

    attachment_path = Path(args.attachment)
    if not attachment_path.exists():
        raise FileNotFoundError(f"Attachment not found: {attachment_path}")

    information = read_attachment(attachment_path)
    if not information.strip():
        raise ValueError("Attachment content is empty.")

    chain = build_chain(temperature=args.temperature)
    response = chain.invoke({"information": information})
    print(response.content)


if __name__ == "__main__":
    main()
