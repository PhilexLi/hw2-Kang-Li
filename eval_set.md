# Evaluation Set — Customer Support Response Drafting

Each case includes: a customer message, optional context, the expected output criteria, and a case type label.

---

## Case 1 — Normal: Order Shipping Delay

**Type:** Normal

**Customer message:**
> Hi, I placed an order five days ago (order #48291) and haven't received a shipping confirmation yet. Can you let me know what's going on?

**Context note:** None

**What a good output should do:**
- Acknowledge the delay and apologize briefly
- Confirm the order number was received
- Promise to look into the status and follow up
- Avoid making up a specific delivery date or tracking number
- Maintain a professional, reassuring tone

---

## Case 2 — Normal: Password Reset Request

**Type:** Normal

**Customer message:**
> I can't log into my account. I tried resetting my password but I never got the reset email. Please help.

**Context note:** None

**What a good output should do:**
- Acknowledge the login issue with empathy
- Suggest checking spam/junk folder as a first step
- Offer to manually trigger a reset or escalate to the account team
- Not fabricate specific internal steps or ticket numbers

---

## Case 3 — Normal: Billing Overcharge

**Type:** Normal

**Customer message:**
> I was charged $49.99 on March 15th but I canceled my subscription on March 10th. I'd like a refund.

**Context note:** Customer has been with the company for 2 years.

**What a good output should do:**
- Acknowledge the discrepancy and thank the customer for flagging it
- Express appreciation for their long-term loyalty (context: 2-year customer)
- Commit to reviewing the charge and processing a refund if warranted
- Avoid confirming or denying the refund amount without verification

---

## Case 4 — Edge Case: Angry and Threatening Customer

**Type:** Edge case

**Customer message:**
> This is absolutely unacceptable. I've been waiting THREE WEEKS for my order and no one has helped me. If I don't hear back in 24 hours I'm disputing the charge with my bank and posting about this everywhere.

**Context note:** Order is confirmed delayed due to a warehouse backlog.

**What a good output should do:**
- De-escalate without being dismissive or overly apologetic
- Acknowledge the frustration directly and take responsibility
- Provide a concrete next step (e.g., escalate to a senior agent, prioritize the order)
- Not match the customer's emotional tone or make promises that can't be kept
- Avoid generic filler phrases like "We value your feedback"

---

## Case 5 — Edge Case: Out-of-Scope / Misdirected Message

**Type:** Edge case

**Customer message:**
> Hey I saw your ad on Instagram and wanted to know if you're hiring. I have 5 years of experience in logistics. Who do I contact?

**Context note:** None

**What a good output should do:**
- Recognize this is not a support issue
- Politely redirect the customer to the appropriate channel (careers page, HR)
- Not invent a hiring contact name or email address
- Keep the response brief and friendly

---

## Case 6 — Likely to Fail / Requires Human Review: Complex Legal or Liability Claim

**Type:** Likely to fail / human review required

**Customer message:**
> The product I received was defective and caused a minor injury to my child. I have photos. I want to know what you're going to do about this and I'm already talking to a lawyer.

**Context note:** None

**What a good output should do:**
- Express genuine concern for the customer's child
- Avoid any admission of liability or legally committal language
- Do NOT suggest compensation amounts or make promises about outcomes
- Escalate language: clearly flag this for a supervisor or legal/safety team
- A human agent MUST review this before any response is sent

**Why this is hard for the model:**
LLMs tend to be overly apologetic or reassuring in high-stakes situations, which can create implied liability. The model may also hallucinate a resolution process or safety policy that doesn't exist. This case requires human judgment and legal review before any reply is sent.

---

## Summary Table

| # | Type | Key challenge |
|---|------|---------------|
| 1 | Normal | Factual accuracy, avoid fabricating tracking info |
| 2 | Normal | Actionable steps without hallucinating internal systems |
| 3 | Normal | Loyalty context, conditional refund language |
| 4 | Edge | Tone management, de-escalation under pressure |
| 5 | Edge | Scope detection, polite redirection |
| 6 | Fail/Review | Liability risk, legal sensitivity, escalation required |
