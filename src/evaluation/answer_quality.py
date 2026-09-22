import json

from pydantic import BaseModel, Field
import time

from src.intelligence.groq_client import (
    DEFAULT_MODEL,
    get_groq_client,
)


class AnswerQualityScore(BaseModel):
    """Structured quality judgment for one answer."""

    relevance: int = Field(
        ge=1,
        le=5,
    )

    evidence_use: int = Field(
        ge=1,
        le=5,
    )

    clarity: int = Field(
        ge=1,
        le=5,
    )

    caution: int = Field(
        ge=1,
        le=5,
    )

    actionability: int = Field(
        ge=1,
        le=5,
    )

    reasoning: str = Field(
        min_length=1,
    )

    @property
    def average_score(self) -> float:
        values = [
            self.relevance,
            self.evidence_use,
            self.clarity,
            self.caution,
            self.actionability,
        ]

        return round(
            sum(values) / len(values),
            2,
        )


def evaluate_answer_quality(
    user_query: str,
    answer: str,
    evidence: dict,
) -> AnswerQualityScore:
    """Evaluate answer quality using a structured LLM judge."""

    client = get_groq_client()

    prompt = f"""
You are evaluating the quality of a RetailOps AI business answer.

Evaluate ONLY the supplied answer against the supplied question
and evidence.

USER QUESTION:
{user_query}

ANSWER:
{answer}

VERIFIED EVIDENCE:
{json.dumps(evidence, ensure_ascii=False, default=str)}

Score each dimension from 1 to 5.

RELEVANCE
5 = directly and completely answers the question
3 = partially answers it
1 = largely irrelevant

EVIDENCE_USE
5 = claims are clearly supported by supplied evidence
3 = mostly supported but weakly connected
1 = unsupported or contradicts evidence

CLARITY
5 = concise, structured, easy for a business user to understand
3 = understandable but verbose or unclear in places
1 = confusing

CAUTION
5 = appropriately distinguishes evidence, association,
    uncertainty, and causation
3 = slightly overstated
1 = makes unsupported causal or certain claims

ACTIONABILITY
5 = provides a useful evidence-supported next step
3 = generic recommendation
1 = no useful next step when one is appropriate

Do not reward verbosity.

Do not penalize an answer for refusing to invent a cause
when the evidence does not establish one.

Return valid JSON only:

{{
    "relevance": 1,
    "evidence_use": 1,
    "clarity": 1,
    "caution": 1,
    "actionability": 1,
    "reasoning": "Brief explanation."
}}
"""

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict evaluator of "
                    "evidence-grounded business AI answers."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={
            "type": "json_object"
        },
    )

    data = json.loads(
        response.choices[0]
        .message.content
    )

    return AnswerQualityScore.model_validate(
        data
    )

def evaluate_answer_quality_dataset(
    dataset,
):
    """Evaluate answer quality across a question dataset."""

    import pandas as pd

    from src.agents.graph import (
        retailops_graph,
    )

    results = []

    for query in dataset["user_query"]:

        state = {
            "user_query": query,
            "selected_agents": [],
            "agent_results": {},
            "evidence": [],
            "final_answer": None,
            "errors": [],
        }

        graph_result = retailops_graph.invoke(
            state
        )

        quality = evaluate_answer_quality(
            user_query=query,
            answer=graph_result["final_answer"],
            evidence=graph_result["agent_results"],
        )

        results.append({
            "user_query": query,
            "relevance": quality.relevance,
            "evidence_use": quality.evidence_use,
            "clarity": quality.clarity,
            "caution": quality.caution,
            "actionability": quality.actionability,
            "average_score": quality.average_score,
            "reasoning": quality.reasoning,
        })

        # Answer-quality evaluation is token intensive:
        # each case runs the agent graph and then an
        # additional LLM judge call.
        #
        # Use a larger delay than the other evaluators
        # to stay below Groq's TPM limit.
        time.sleep(15.0)

    result_df = pd.DataFrame(
        results
    )

    metrics = {
        "total_answers": len(result_df),

        "relevance": round(
            float(
                result_df[
                    "relevance"
                ].mean()
            ),
            2,
        ),

        "evidence_use": round(
            float(
                result_df[
                    "evidence_use"
                ].mean()
            ),
            2,
        ),

        "clarity": round(
            float(
                result_df[
                    "clarity"
                ].mean()
            ),
            2,
        ),

        "caution": round(
            float(
                result_df[
                    "caution"
                ].mean()
            ),
            2,
        ),

        "actionability": round(
            float(
                result_df[
                    "actionability"
                ].mean()
            ),
            2,
        ),

        "overall_average": round(
            float(
                result_df[
                    "average_score"
                ].mean()
            ),
            2,
        ),
    }

    return result_df, metrics