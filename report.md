# Report: Customer Support Response Drafting

**Author:** Kang Li
**Date:** April 2026
**Model:** qwen-turbo (Alibaba Tongyi / DashScope, OpenAI-compatible API)

---

## 1. Business Use Case

Customer support teams at e-commerce and SaaS companies spend a significant portion of their day composing replies to repetitive categories of messages — shipping delays, billing disputes, password resets, and account issues. Writing each reply from scratch is time-consuming and introduces inconsistency in tone, especially across agents with different experience levels.

This prototype automates the **first-pass draft** of customer support email responses. A human agent provides the inbound customer message and an optional context note; the system returns a structured draft that the agent reviews, edits if needed, and sends. The human remains in the loop for every outbound message.

The target user is a support representative or team lead at a mid-size company who handles moderate-to-high ticket volume and values consistency and speed over full automation.

---

## 2. Model Selection

**Chosen model: `qwen-turbo`** (Alibaba Tongyi, accessed via DashScope's OpenAI-compatible API)

Qwen-turbo was selected for two practical reasons: it is accessible from mainland China without a VPN, and it offers a free usage tier sufficient for prototyping and evaluation. The OpenAI-compatible endpoint made it straightforward to integrate with standard Python tooling.

**Observations on model behavior:**
- For normal cases (shipping delay, password reset, billing), qwen-turbo produced fluent, professionally-toned drafts consistent with typical support language.
- For edge cases (angry customer, out-of-scope message), the model required explicit prompt guidance to stay on task — without rules, it defaulted to generic reassurances.
- For the high-risk legal/injury case, the model initially attempted to offer a resolution path rather than flagging for human review. This required a dedicated, clearly-worded rule to correct.

No other models were tested in this prototype. A comparative evaluation against a larger model (e.g., qwen-plus or GPT-4o-mini) would be a natural next step to assess whether more capable models reduce the remaining failure cases.

---

## 3. Baseline vs. Final Design

### Prompt Iteration Summary

| Version | Key Changes | Notable Results |
|---------|-------------|-----------------|
| V1 (Baseline) | Basic structure + 5 general rules | Placeholder text in drafts; loyalty context ignored; fabricated URLs; no reliable human-review flag |
| V2 (Revision 1) | Explicit ban on placeholders; `--- HUMAN REVIEW REQUIRED ---` flag; anti-echo rule added | Flag appeared reliably on Case 6; URL fabrication eliminated; placeholder text largely gone |
| V3 (Final) | Concrete example added to context-usage rule; anti-echo rule strengthened with explicit alternative phrasing; out-of-scope rule tightened | Consistent prose output; Case 6 flag stable; cleaner redirects on Case 5 |

### Baseline Output (V1) — Selected Examples

**Case 5 (Out-of-Scope):**
> "For job inquiries, please visit our careers page at **[companywebsite.com/careers]**."

The model invented a URL despite a rule against fabrication. Sending this draft would direct a customer to a broken link.

**Case 6 (Legal/Injury):**
> "We recommend you contact our dedicated support team directly at **[support email/phone number]**..."

No human-review flag appeared. The model attempted to resolve a legally sensitive case by routing the customer to a contact that does not exist in the draft.

### Final Output (V3) — Same Cases

**Case 5 (Out-of-Scope):**
> "Please visit our careers page to explore current opportunities and apply."

No invented URL. Clean redirect. (Note: the model still mentions a "careers page" generically, which is acceptable since it does not invent a specific address.)

**Case 6 (Legal/Injury):**
> "--- HUMAN REVIEW REQUIRED ---
> We are truly sorry to hear about the incident and the concern for your child's safety. Please know that we take this very seriously. We will review your case promptly and get back to you as soon as possible."

The flag appears reliably and the draft is non-committal — appropriate for a case with legal exposure.

---

## 4. Where the Prototype Still Fails

Two failure patterns persisted across all three prompt versions:

**1. Loyalty context not used (Case 3 — Billing Overcharge)**
When the context note stated "Customer has been with the company for 2 years," all three prompt versions produced a generic billing response with no acknowledgment of customer tenure. The model appeared to deprioritize free-text context notes relative to the structured system prompt. A more reliable fix would be to restructure the input to include a labeled field (e.g., `Customer tier: 2-year subscriber`) rather than relying on a prose context note.

**2. Threat timeline echo (Case 4 — Angry Customer)**
The customer's message included "If I don't hear back in 24 hours..." All three prompt versions produced a draft that echoed this deadline back ("We will follow up within the next 24 hours"), despite explicit rules against it. Mirroring the customer's threat framing can be interpreted as accepting the terms of an ultimatum. This is a consistent behavioral pattern in the model that did not respond to prompt-level instructions alone. A post-processing filter or a fine-tuned model would be required to reliably suppress it.

In both cases, a human agent reviewing the draft before sending would catch these issues — which is the expected workflow.

---

## 5. Deployment Recommendation

**Recommendation: Deploy with mandatory human review at the current stage.**

The prototype demonstrates genuine value: it produces well-structured, professional first-pass drafts for the majority of common support cases, eliminates placeholder fabrication, and reliably flags high-risk legal cases for escalation. For a team handling high ticket volume, this alone reduces cognitive load and drafting time.

However, the following conditions should be met before deployment:

- **Every draft must be reviewed by a human agent before sending.** The prototype is a drafting tool, not an autonomous responder. This is especially critical for billing disputes, escalations, and any case involving legal language.
- **Case 4 (angry/threatening customers) requires extra scrutiny.** The deadline-echo failure means agents should explicitly check that no customer-stated timeframe has been repeated back as a commitment.
- **Case 3 (loyalty context) requires a structured input format.** Free-text context notes are unreliable. A simple form interface with labeled fields (customer tier, account age, prior contacts) would improve context utilization significantly.
- **The `--- HUMAN REVIEW REQUIRED ---` flag should trigger a routing rule** in any real deployment — automatically assigning the ticket to a senior agent or legal reviewer rather than the general queue.

Deploying without these controls — particularly without mandatory human review — would introduce reputational and legal risk that outweighs the efficiency gains.
