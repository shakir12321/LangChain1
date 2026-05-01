# LangChain Attachment Demo

This is a small LangChain project that reads a person profile from an attachment and returns:

1. A short summary
2. Two interesting facts

It supports `.txt`, `.md`, and `.pdf` attachments.

## 1) Setup

```bash
cd /Users/shakir/langchain-attachment-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Configure API key

```bash
cp .env.example .env
```

Open `.env` and set:

```env
OPENAI_API_KEY=your_real_key_here
```

## 3) Create a sample attachment

```bash
cat > person.txt <<'EOF'
Elon Musk is an entrepreneur known for Tesla and SpaceX.
He was born in South Africa and later moved to the United States.
He also founded companies like Neuralink and The Boring Company.
EOF
```

## 4) Run

```bash
python main.py --attachment person.txt
```

Optional arguments:
- `--model` (default: `gpt-5`)
- `--temperature` (default: `0.0`)

Example:

```bash
python main.py --attachment person.txt --model gpt-5 --temperature 0
```
# LangChain1
