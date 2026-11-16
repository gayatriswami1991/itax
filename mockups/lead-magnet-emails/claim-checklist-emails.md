# Claim readiness checklist: automatic emails

Two emails fire when someone submits the checklist form on the home page (`lead_source` = `home-lead-magnet-claim-readiness`).
Form fields: **name, email, company**. Attach `itax-claim-readiness-checklist.pdf` to Email 2 (or link it).
Merge tags are shown as `{{name}}`, `{{email}}`, `{{company}}`, `{{lead_source}}`, `{{submitted_at}}`, `{{page_url}}`. Rename them to match the form plugin the developer uses.

Setup notes for the developer
- Email 1 goes to the client inbox: info@itaxadvisors.co.uk. Set Reply-To to `{{email}}` so the team can reply to the lead directly.
- Email 2 goes to the person who filled the form, `{{email}}`. Send from info@itaxadvisors.co.uk, Reply-To info@itaxadvisors.co.uk.
- Send Email 2 only if the consent box is ticked. Store the lead in the CRM or form-entries list as well.
- The same two templates serve the HMRC enquiry and life sciences checklists. Change the checklist name, PDF and the `lead_source` value.

---

## EMAIL 1: To the client (internal notification)

**To:** info@itaxadvisors.co.uk
**Reply-To:** {{email}}
**Subject:** New checklist download: {{company}} ({{name}})

Hi team,

A new lead has downloaded the claim readiness checklist from the website.

- Name: {{name}}
- Work email: {{email}}
- Company: {{company}}
- Checklist: The 15-point claim readiness checklist
- Form: {{lead_source}}
- Submitted: {{submitted_at}}
- Page: {{page_url}}

What to do next
1. Reply to this email to reach {{name}} directly.
2. Lead has already received the PDF automatically. A short personal note from a specialist usually works best.
3. Add the lead to the CRM with the source "Website: claim readiness checklist".

(Automatic message from itaxadvisors.co.uk)

---

## EMAIL 2: To the user (auto-reply with the PDF)

**From:** iTax Advisors <info@itaxadvisors.co.uk>
**Reply-To:** info@itaxadvisors.co.uk
**To:** {{email}}
**Subject:** Your 15-point claim readiness checklist
**Attachment:** itax-claim-readiness-checklist.pdf

Hi {{name}},

Thank you for requesting the 15-point claim readiness checklist. It is attached to this email.

Use it to review the technical, financial and procedural readiness of your R&D claim before you submit. It covers five areas:

1. Eligibility and applicable scheme
2. Project scope and technical review
3. Qualifying costs and activities
4. Contracts, contracted-out expenditure and overseas costs
5. Evidence, deadlines and submission

How to use it
- Tick a box when the point has been checked and documented.
- Resolve gaps before submission.
- Record any open issue, an owner and a due date in the "What next?" box on page 2.

This is a readiness check, not an eligibility score. A completed checklist does not establish entitlement to relief.

If any point is unclear, or you would like a specialist to review your claim, just reply to this email or write to info@itaxadvisors.co.uk. We will get back to you.

Kind regards,
The iTax Advisors team
itaxadvisors.co.uk
LinkedIn: https://www.linkedin.com/company/itax-advisors-limited

You are receiving this email because you requested the checklist on itaxadvisors.co.uk. General information only; requirements depend on the facts, accounting period, scheme and applicable law.
