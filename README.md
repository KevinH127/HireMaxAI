# HireMaxAI

HireMaxAI is an AI-powered resume analysis tool that helps users optimize their resumes for applicant tracking systems (ATS) and recruiters.

Think of it as resume “looksmaxxing”: identify weak points, improve alignment, and maximize interview potential.

---

## Problem

Most resumes fail before reaching a human reviewer.

Common issues:
- Poor keyword alignment with job descriptions
- Weak or vague bullet points
- Generic resumes not tailored to specific roles

Applicants rarely know what changes actually matter.

---

## Solution

HireMaxAI analyzes a resume against a job description and returns:
- An ATS match score
- Ranked, high-impact improvement suggestions
- Rewritten resume bullets optimized for clarity and impact

The goal is actionable feedback, not generic advice.

---

## Core Features (MVP)

- ATS Match Scoring (0–100)
- Resume-to-job-description keyword analysis
- Bullet point rewriting with quantified impact
- Structured resume parsing from PDF files
- Output in structured JSON format

---

## How It Works

1. Parse resume PDF into structured sections (Education, Experience, Skills, Projects)
2. Analyze job description for required skills and keywords
3. Compare resume content against job requirements
4. Generate prioritized fixes and rewritten bullets

---

## Tech Stack

- Frontend: React / Next.js
- Backend: Python
- AI: Large Language Model (LLM)
- PDF Parsing: pdfplumber
- Data Output: Python dictionary and JSON

---

## Example Output

```json
{
  "match_score": 72,
  "missing_keywords": ["SQL", "data visualization"],
  "rewritten_bullets": [
    {
      "before": "Worked on reports",
      "after": "Built automated reports used by 3 teams, reducing reporting time by 25%"
    }
  ]
}
