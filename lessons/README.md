# Essential teaching units / Unidades essenciais

`units.pt-BR.json` contains original, concise teaching material for all 57 approved
objectives in `exam/curriculum.json`. Match `competency_id` to the curriculum;
prerequisites, objective wording and assessment criteria remain there. The JSON
is intentionally separate from the practice bank: a teaching prompt that has been
explained or hinted is learning evidence, not an unseen assessment item.

Use one unit at a time: explain, discuss the worked example, ask the retrieval
prompt, give feedback, then change the context with the transfer prompt. Ask for
reasoning and adapt the depth. The contrast identifies a common misconception.
Each unit also supplies `cloud_azure_distinction` and `depth_guidance`. For a
beginner, check the listed curriculum prerequisites, explain the focus concepts,
then use the example before retrieval. For an experienced learner, start with the
uncued transfer scenario and the unit's specific evaluation challenge; repair only
the observed gap. Experience is a starting depth choice, never evidence of mastery.
The explanation, example and contrast are tutor reference material; do not paste
them together with the prompt during a diagnostic or assessment. Do not require
an Azure account: all examples and prompts are conceptual, with no deployment.

The authored language is Brazilian Portuguese. The tutor can translate into
English on demand, retaining Azure product names and checking the source if a
translation changes meaning. There is no independently reviewed English edition.
These are starting explanations, not full courses or a guarantee of readiness.
All examples are fictitious and original, not recalled exam questions.

`source_urls` point to relevant official Microsoft Learn units reviewed on
2026-10-15. The approved guide controls scope; Learn includes some broader topics.
Keep exact prices, licensing, SLAs and service availability out of these stable
conceptual units; verify those details when a learner needs them. Source review
and structural checks do not establish teaching effectiveness or exam success.

Run `python -m unittest discover -s tests -v` for coverage, mapping and required
content checks. Qualitative tutoring still requires the documented model evals.
