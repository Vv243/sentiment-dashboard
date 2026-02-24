import pytest
from unittest.mock import patch, MagicMock
from app.services.openai_analyzer import OpenAIAnalyzer, _cached_analyze


def make_mock_openai_response(content: str):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = content
    return mock_response


MOCK_POSITIVE_JSON = '{"sentiment": "positive", "compound_score": 0.85, "confidence": 0.95, "emotions": ["joy", "trust"], "reasoning": "Clear positive text."}'
MOCK_NEGATIVE_JSON = '{"sentiment": "negative", "compound_score": -0.75, "confidence": 0.90, "emotions": ["sadness", "anger"], "reasoning": "Clear negative text."}'
MOCK_SARCASM_JSON = '{"sentiment": "negative", "compound_score": -0.50, "confidence": 0.85, "emotions": ["sadness", "anticipation"], "reasoning": "Oh great is sarcastic."}'
MOCK_MIXED_JSON = '{"sentiment": "neutral", "compound_score": 0.20, "confidence": 0.80, "emotions": ["joy", "fear"], "reasoning": "Mixed excitement and fear."}'


@pytest.fixture(autouse=True)
def clear_cache():
    _cached_analyze.cache_clear()
    yield
    _cached_analyze.cache_clear()


class TestOpenAIAnalyzer:

    @patch('app.services.openai_analyzer.OpenAI')
    def test_positive_sentiment(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_mock_openai_response(MOCK_POSITIVE_JSON)
        analyzer = OpenAIAnalyzer()
        result = analyzer.analyze("I love this product!")
        assert result['sentiment'] == 'positive'
        assert result['scores']['compound'] > 0
        assert result['model'] == 'gpt-4o-mini'
        assert 'joy' in result['emotions']
        assert result['reasoning'] != ''

    @patch('app.services.openai_analyzer.OpenAI')
    def test_negative_sentiment(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_mock_openai_response(MOCK_NEGATIVE_JSON)
        analyzer = OpenAIAnalyzer()
        result = analyzer.analyze("This is absolutely terrible.")
        assert result['sentiment'] == 'negative'
        assert result['scores']['compound'] < 0
        assert 'sadness' in result['emotions'] or 'anger' in result['emotions']

    @patch('app.services.openai_analyzer.OpenAI')
    def test_sarcasm_detection(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_mock_openai_response(MOCK_SARCASM_JSON)
        analyzer = OpenAIAnalyzer()
        result = analyzer.analyze("Oh great, another Monday!")
        assert result['sentiment'] == 'negative'
        assert result['scores']['compound'] < 0
        assert result['reasoning'] != ''

    @patch('app.services.openai_analyzer.OpenAI')
    def test_mixed_emotions(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_mock_openai_response(MOCK_MIXED_JSON)
        analyzer = OpenAIAnalyzer()
        result = analyzer.analyze("I'm excited but also terrified.")
        assert len(result['emotions']) >= 2
        assert 'joy' in result['emotions']
        assert 'fear' in result['emotions']

    @patch('app.services.openai_analyzer.OpenAI')
    def test_response_has_required_fields(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_mock_openai_response(MOCK_POSITIVE_JSON)
        analyzer = OpenAIAnalyzer()
        result = analyzer.analyze("Test text")
        assert 'sentiment' in result
        assert 'emoji' in result
        assert 'scores' in result
        assert 'compound' in result['scores']
        assert 'confidence' in result
        assert 'emotions' in result
        assert 'reasoning' in result
        assert 'model' in result
        assert 'cached' in result
        assert result['model'] == 'gpt-4o-mini'

    @patch('app.services.openai_analyzer.OpenAI')
    def test_scores_are_valid_range(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_mock_openai_response(MOCK_POSITIVE_JSON)
        analyzer = OpenAIAnalyzer()
        result = analyzer.analyze("Test text")
        assert -1.0 <= result['scores']['compound'] <= 1.0
        assert 0.0 <= result['scores']['positive'] <= 1.0
        assert 0.0 <= result['scores']['negative'] <= 1.0
        assert 0.0 <= result['scores']['neutral'] <= 1.0
        assert 0.0 <= result['confidence'] <= 1.0

    @patch('app.services.openai_analyzer.OpenAI')
    def test_api_failure_returns_error_response(self, mock_openai_class):
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API unavailable")
        analyzer = OpenAIAnalyzer()
        result = analyzer.analyze("Test text")
        assert result is not None
        assert 'sentiment' in result
        assert result['error'] is not None


class TestGPTAPIEndpoint:

    def test_gpt_model_accepted(self, client):
        with patch('app.services.sentiment_analyzer.SentimentAnalyzer._analyze_with_gpt') as mock_gpt:
            mock_gpt.return_value = {'text': 'I love this!', 'sentiment': 'positive', 'emoji': '😊', 'scores': {'positive': 0.9, 'negative': 0.05, 'neutral': 0.05, 'compound': 0.85}, 'confidence': 0.95, 'model': 'gpt-4o-mini', 'emotions': ['joy'], 'reasoning': 'Clear positive sentiment.', 'cached': False, 'error': None, 'moderation': {'flagged': False, 'reason': None, 'severity': 'safe'}}
            response = client.post("/api/v1/sentiment/analyze", json={"text": "I love this!", "model": "gpt-4o-mini"})
            assert response.status_code == 200
            assert response.json()['model'] == 'gpt-4o-mini'

    def test_gpt_response_includes_emotions(self, client):
        with patch('app.services.sentiment_analyzer.SentimentAnalyzer._analyze_with_gpt') as mock_gpt:
            mock_gpt.return_value = {'text': 'Test', 'sentiment': 'positive', 'emoji': '😊', 'scores': {'positive': 0.9, 'negative': 0.05, 'neutral': 0.05, 'compound': 0.85}, 'confidence': 0.95, 'model': 'gpt-4o-mini', 'emotions': ['joy', 'trust'], 'reasoning': 'Positive text.', 'cached': False, 'error': None, 'moderation': {'flagged': False, 'reason': None, 'severity': 'safe'}}
            response = client.post("/api/v1/sentiment/analyze", json={"text": "Test", "model": "gpt-4o-mini"})
            assert response.status_code == 200
            data = response.json()
            assert 'emotions' in data
            assert 'reasoning' in data
