# hw2-Kang-Li

## Business Workflow: Customer Support Response Drafting

### Overview

This project automates the first-pass drafting of customer support email responses using a large language model. A support agent provides a customer's inbound message, and the system returns a draft reply that is professional, empathetic, and actionable.

### Who is the user?

A customer support representative (or support team lead) at a mid-size SaaS or e-commerce company. The user reviews the draft, makes minor edits if needed, and sends it — rather than writing the response from scratch.

### What input does the system receive?

- A raw customer email or support ticket message (free-form text)
- Optionally: a short context note (e.g., "this customer has been with us 3 years" or "their order is delayed")

### What output should the system produce?

A structured draft reply containing:
1. A professional greeting
2. An empathetic acknowledgment of the customer's issue
3. A clear, actionable response or next step
4. A polite closing

### Why is this task valuable to automate?

Support teams spend a large portion of their day writing responses to similar categories of issues (shipping delays, billing questions, account access, etc.). A first-pass draft cuts average handle time significantly, reduces cognitive load, and helps maintain a consistent tone across agents — especially for newer team members. Human review is still required before sending, keeping the human in the loop for quality and accountability.

---

## Video Walkthrough

*(Link to be added after recording)*

---

## Files

| File | Description |
|------|-------------|
| `app.py` | Main Python script — runs the workflow from the command line |
| `prompts.md` | Prompt versions and iteration notes |
| `eval_set.md` | Evaluation set with test cases and expected output criteria |
| `report.md` | Final report: design decisions, evaluation results, and deployment recommendation |
