"""
app.py — Customer Support Response Drafting
Uses Alibaba Qwen (Tongyi) via OpenAI-compatible API.

Usage:
  # Draft a response for a single message
  python app.py --input "I never received my order." --context "Order is delayed."

  # Run all eval-set cases
  python app.py --run-eval

  # Override the model
  python app.py --run-eval --model qwen-plus

Set your API key via environment variable before running:
  export DASHSCOPE_API_KEY="your_key_here"   # macOS/Linux / PowerShell
  set DASHSCOPE_API_KEY=your_key_here        # Windows CMD
"""

import argparse
import os
import sys
from datetime import datetime
from openai import OpenAI

# ---------------------------------------------------------------------------
# Configurable system prompt — edit this to iterate (see prompts.md)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a professional customer support representative for an e-commerce and SaaS company.

Your job is to draft a first-pass reply to a customer's support message.

Follow this structure in every response:
1. Greeting — address the customer warmly and professionally
2. Acknowledgment — briefly acknowledge their issue with empathy
3. Action — provide a clear next step or resolution
4. Closing — end politely and invite further questions

Rules:
- Never fabricate specific details such as tracking numbers, refund amounts, or internal ticket IDs
- If the issue involves legal liability, injury, or a threat of legal action, flag it clearly and recommend human review before sending
- Match the customer's urgency without matching their emotional tone if they are angry
- Keep the reply concise — no more than 150 words
- If the message is out of scope for support (e.g., job inquiries), politely redirect without inventing contacts"""

# ---------------------------------------------------------------------------
# Eval set — mirrors eval_set.md
# ---------------------------------------------------------------------------
EVAL_CASES = [
    {
        "id": 1,
        "type": "Normal",
        "label": "Order Shipping Delay",
        "message": "Hi, I placed an order five days ago (order #48291) and haven't received a shipping confirmation yet. Can you let me know what's going on?",
        "context": None,
    },
    {
        "id": 2,
        "type": "Normal",
        "label": "Password Reset Request",
        "message": "I can't log into my account. I tried resetting my password but I never got the reset email. Please help.",
        "context": None,
    },
    {
        "id": 3,
        "type": "Normal",
        "label": "Billing Overcharge",
        "message": "I was charged $49.99 on March 15th but I canceled my subscription on March 10th. I'd like a refund.",
        "context": "Customer has been with the company for 2 years.",
    },
    {
        "id": 4,
        "type": "Edge",
        "label": "Angry and Threatening Customer",
        "message": "This is absolutely unacceptable. I've been waiting THREE WEEKS for my order and no one has helped me. If I don't hear back in 24 hours I'm disputing the charge with my bank and posting about this everywhere.",
        "context": "Order is confirmed delayed due to a warehouse backlog.",
    },
    {
        "id": 5,
        "type": "Edge",
        "label": "Out-of-Scope / Misdirected Message",
        "message": "Hey I saw your ad on Instagram and wanted to know if you're hiring. I have 5 years of experience in logistics. Who do I contact?",
        "context": None,
    },
    {
        "id": 6,
        "type": "Likely to Fail / Human Review Required",
        "label": "Legal / Liability Claim",
        "message": "The product I received was defective and caused a minor injury to my child. I have photos. I want to know what you're going to do about this and I'm already talking to a lawyer.",
        "context": None,
    },
]


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------
def draft_response(customer_message: str, context: str | None, model_name: str, client: OpenAI) -> str:
    user_content = f"Customer message:\n{customer_message}"
    if context:
        user_content += f"\n\nContext for the support agent:\n{context}"

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------
def print_section(title: str, content: str) -> None:
    width = 70
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)
    print(content)


def save_output(lines: list[str], output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nOutput saved to: {output_file}")


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------
def run_single(message: str, context: str | None, model_name: str, output_file: str, client: OpenAI) -> None:
    print(f"\nModel: {model_name}")
    print(f"Input: {message[:80]}{'...' if len(message) > 80 else ''}")

    draft = draft_response(message, context, model_name, client)

    print_section("DRAFT RESPONSE", draft)

    lines = [
        "Customer Support Response Draft",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Model: {model_name}",
        "",
        "--- INPUT ---",
        message,
    ]
    if context:
        lines += ["", "--- CONTEXT ---", context]
    lines += ["", "--- DRAFT RESPONSE ---", draft]

    save_output(lines, output_file)


def run_eval(model_name: str, output_file: str, client: OpenAI) -> None:
    print(f"\nRunning eval set ({len(EVAL_CASES)} cases) with model: {model_name}\n")

    all_lines = [
        "Customer Support Response Drafting — Eval Run",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Model: {model_name}",
        "=" * 70,
    ]

    for case in EVAL_CASES:
        print(f"[{case['id']}/{len(EVAL_CASES)}] {case['label']} ({case['type']})...")
        draft = draft_response(case["message"], case["context"], model_name, client)

        section = [
            "",
            f"CASE {case['id']}: {case['label']}",
            f"Type: {case['type']}",
            "-" * 50,
            "Customer message:",
            case["message"],
        ]
        if case["context"]:
            section += ["", "Context:", case["context"]]
        section += ["", "Draft response:", draft, "=" * 70]

        all_lines.extend(section)
        print_section(f"CASE {case['id']}: {case['label']} [{case['type']}]", draft)

    save_output(all_lines, output_file)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Customer Support Response Drafting — GenAI Prototype")
    parser.add_argument("--input", type=str, help="Customer message to draft a response for")
    parser.add_argument("--context", type=str, default=None, help="Optional context note for the support agent")
    parser.add_argument("--run-eval", action="store_true", help="Run all eval-set cases")
    parser.add_argument("--model", type=str, default="qwen-turbo", help="Model name (default: qwen-turbo)")
    parser.add_argument("--output", type=str, default="output.txt", help="Output file path (default: output.txt)")
    args = parser.parse_args()

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("Error: DASHSCOPE_API_KEY environment variable is not set.")
        print("  export DASHSCOPE_API_KEY='your_key_here'   # macOS/Linux/PowerShell")
        print("  set DASHSCOPE_API_KEY=your_key_here        # Windows CMD")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    if args.run_eval:
        run_eval(args.model, args.output, client)
    elif args.input:
        run_single(args.input, args.context, args.model, args.output, client)
    else:
        parser.print_help()
        print("\nExamples:")
        print('  python app.py --input "I never received my order." --context "Order is delayed."')
        print("  python app.py --run-eval")


if __name__ == "__main__":
    main()
