Pricing and Prompts (Sessions 10–12)

A. Pricing Research
Date of research: 2025 10 13

Project: PromptWise — AI assistant that helps users refine and optimize their prompts for better AI outputs
Sources checked:

Google Gemini Pricing Overview
Gemini Developer Guide
TechCrunch Gemini Pricing Update
DeepMind Blog Gemini Family

Assumed exchange rate: ₹85 = $1

Summary Table

| Model            | Billing Unit     | Input Cost (per 1K tokens) | Output Cost (per 1K tokens) | Notes                                         |
|------------------|------------------|-----------------------------|------------------------------|-----------------------------------------------|
| Gemini 2.5 Flash | per 1,000 tokens | ₹0.0085                     | ₹0.034                       | Fast and affordable, great for prototype testing |
| Gemini 2.5 Pro   | per 1,000 tokens | ₹0.106                      | ₹0.850                       | Strong reasoning and context understanding    |
| Gemini 2.5 Ultra | per 1,000 tokens | ₹0.213                      | ₹1.275                       | For long documents or complex analysis        |
| Free Tier (AI Studio) | Limited     | Free                        | Free                         | Used for light testing and early-stage experiments |


Summary:
PromptWise primarily uses Gemini 2.5 Flash during testing phases due to its low cost. Gemini 2.5 Pro is used for advanced evaluation and response quality analysis where logic and reasoning are required.

B. Cost Estimation Examples
Example 1 Prompt Feedback Generation (Gemini 2.5 Flash)
Prompt + response ≈ 600 tokens

Input: 300 × ₹0.0085 = ₹2.55
Output: 300 × ₹0.034 = ₹10.2
Total: ₹12.75 per feedback session

Example 2 Advanced Prompt Optimization (Gemini 2.5 Pro)
Prompt + response ≈ 1,200 tokens

Input: 500 × ₹0.106 = ₹53
Output: 700 × ₹0.850 = ₹595
Total: ₹648 per optimization request

Example 3 Daily Hackathon Estimate
If PromptWise processes 150 API calls/day (100 Flash + 50 Pro):
(100 × ₹12.75) + (50 × ₹648) = ₹33,037.5/day

Team Recommendation:
Use Gemini 2.5 Flash for frequent lightweight testing and Gemini 2.5 Pro for in depth logical refinement or final deployment tasks. This combination ensures an effective balance between performance and budget.

C. Prompt Refinement Before / After (RTFC Framework)

Priya — Feedback Evaluator
Bad prompt (before):
Check this user prompt and make it better.

Refined prompt (after):
Role: You are an AI prompt reviewer.
Task: Evaluate the clarity and structure of the user’s prompt.
Format: 3 sections Strengths, Weaknesses, Suggestions.
Constraint: Keep total response under 120 words.

Observation:
Adds structure and limits output length for concise, actionable insights.

Sera — Prompt Trainer
Bad prompt (before):
Explain how to write a good prompt.

Refined prompt (after):
Role: AI training coach.
Task: Teach how to craft effective prompts for LLMs.
Format: Short paragraph + 3 do’s and 3 don’ts list.
Constraint: Use simple, clear English under 150 words.

Observation:
Defines teaching role and structure to create educational, beginner friendly content.

Alan — Content Generator
Bad prompt (before):
Write about climate change.

Refined prompt (after):
Role: You are an environmental science writer.
Task: Explain the causes and effects of climate change for a high school audience.
Format: 2 short paragraphs followed by 3 bullet points on possible solutions.
Constraint: Use simple language and keep the total under 150 words.

Observation:
Defines audience, structure, and tone making the response more focused, educational, and easy to understand.

Adrina — Prompt Analyzer
Bad prompt (before):
Rate this prompt.

Refined prompt (after):
Role: AI evaluation assistant.
Task: Rate the given prompt on clarity, specificity, and goal alignment.
Format: Table with three columns Criteria, Rating (1–5), Comment.
Constraint: Limit each comment to one line.

Observation:
Enforces a uniform scoring format, making results measurable and easy to compare.

Rahul — Idea Expander
Bad prompt (before):
Give me related ideas.

Refined prompt (after):
Role: Creative brainstorming mentor.
Task: Suggest 5 related prompt ideas that expand on the original topic.
Format: Numbered list with a 1 sentence explanation for each idea.
Constraint: Keep each explanation under 15 words.

Observation:
Encourages creative yet concise idea generation for the PromptWise suggestion system.

Senorita — User Guide Writer
Bad prompt (before):
Write instructions.

Refined prompt (after):
Role: Documentation expert.
Task: Write step by step instructions on how to use the PromptWise app.
Format: Numbered list of steps.
Constraint: Limit to 6 steps, simple and direct language.

Observation:
Gives clarity to the role and ensures easy readability for end users.

D. Reflection
This session taught our team how pricing awareness and prompt design are connected.

Cost Management: Token based billing means concise, focused prompts help reduce unnecessary usage.
Prompt Refinement: Using the RTFC framework improved structure and precision across all team tasks.
Model Selection: Gemini Flash works best for trial runs; Pro suits analytical or reasoning heavy tasks.
Overall Insight: Clarity and structure in prompts not only improve AI responses but also keep costs manageable during hackathon scale development.