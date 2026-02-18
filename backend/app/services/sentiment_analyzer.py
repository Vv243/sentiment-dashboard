"""
Sentiment analysis service with multiple models.
Supports VADER (fast), Hybrid (accurate), and GPT-4o-mini (advanced).

All models return a contract-compliant response shape defined in
analyzer_contract.py. The API layer never needs to know which model ran.
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.services.content_moderator import content_moderator
from app.services.hybrid_analyzer import hybrid_analyzer
from app.services.openai_analyzer import analyze_with_cache
from app.services.analyzer_contract import (
    build_standard_response,
    build_error_response,
    derive_scores_from_compound,
    MODEL_VADER,
    MODEL_HYBRID,
    MODEL_GPT,
)
import logging

logger = logging.getLogger(__name__)

# Valid model strings the API will accept
VALID_MODELS = {MODEL_VADER, MODEL_HYBRID, MODEL_GPT}


class SentimentAnalyzer:
    """
    Multi-model sentiment analyzer and router.

    Supported models:
    - "vader"      : Fast, rule-based. Good for simple text.
    - "hybrid"     : VADER + TextBlob + Patterns. Better accuracy.
    - "gpt-4o-mini": OpenAI GPT. Best for sarcasm, mixed emotions, nuance.

    All three return the same response shape (see analyzer_contract.py).
    Moderation is applied before routing to any model.
    """

    def __init__(self):
        logger.info("🧠 Initializing sentiment analyzers...")
        self.vader = SentimentIntensityAnalyzer()
        # hybrid_analyzer and analyze_with_cache load on import
        logger.info("✅ Sentiment analyzers ready")

    def analyze(self, text: str, model: str = MODEL_VADER) -> dict:
        """
        Analyze sentiment with the specified model.

        Args:
            text:  Text to analyze
            model: "vader" | "hybrid" | "gpt-4o-mini"
                   Defaults to "vader" if not specified or invalid.

        Returns:
            Contract-compliant dict (see analyzer_contract.py).
            Always includes a 'moderation' key added after analysis.
        """
        logger.info(f"📊 Analyzing with {model}: {text[:50]}...")

        # Normalize model string — unknown models fall back to vader
        if model not in VALID_MODELS:
            logger.warning(f"⚠️ Unknown model '{model}', falling back to vader")
            model = MODEL_VADER

        # Step 1: Content moderation runs regardless of model choice
        moderation = content_moderator.check_content(text)

        if moderation['is_harmful']:
            logger.warning("⚠️ Harmful content detected, overriding sentiment")
            result = build_standard_response(
                text=text,
                sentiment="harmful",
                scores=derive_scores_from_compound(-0.99),
                confidence=1.0,
                model=model,
                emotions=[],
                reasoning="Content flagged by moderation system.",
            )
            result['moderation'] = {
                'flagged': True,
                'reason': moderation['reason'],
                'severity': moderation['severity'],
            }
            return result

        # Step 2: Route to the correct analyzer
        if model == MODEL_GPT:
            result = self._analyze_with_gpt(text)
        elif model == MODEL_HYBRID:
            result = self._analyze_with_hybrid(text)
        else:
            result = self._analyze_with_vader(text)

        # Step 3: Attach moderation info (always present, flagged=False here)
        result['moderation'] = {
            'flagged': False,
            'reason': None,
            'severity': 'safe',
        }

        return result

    # ------------------------------------------------------------------
    # Private routing methods
    # ------------------------------------------------------------------

    def _analyze_with_vader(self, text: str) -> dict:
        """Analyze with VADER (fast, rule-based)."""
        scores = self.vader.polarity_scores(text)
        compound = scores['compound']

        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return build_standard_response(
            text=text,
            sentiment=sentiment,
            scores={
                'positive': round(scores['pos'], 3),
                'negative': round(scores['neg'], 3),
                'neutral':  round(scores['neu'], 3),
                'compound': round(compound, 3),
            },
            confidence=round(abs(compound), 3),
            model=MODEL_VADER,
            emotions=[],
            reasoning="",
        )

    def _analyze_with_hybrid(self, text: str) -> dict:
        """Analyze with Hybrid (VADER + TextBlob + Patterns)."""
        return hybrid_analyzer.analyze(text)

    def _analyze_with_gpt(self, text: str) -> dict:
        """
        Analyze with GPT-4o-mini via OpenAI API.

        Uses analyze_with_cache() so repeated identical inputs
        skip the API call entirely (80% cost reduction at demo usage).

        If the API call fails, analyze_with_cache() returns a
        contract-compliant error response with error field set.
        The API layer can inspect result['error'] to decide whether
        to surface the error to the user or handle it silently.
        """
        return analyze_with_cache(text)


# Global instance
sentiment_analyzer = SentimentAnalyzer()