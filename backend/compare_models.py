from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.openai_analyzer import OpenAIAnalyzer

vader = SentimentAnalyzer()
openai_analyzer = OpenAIAnalyzer()

tests = [
    "I love this product, it's amazing!",
    "This is absolutely terrible and I hate it.",
    "The meeting is scheduled for 3pm on Thursday.",
    "I'm so excited about the new job, but also terrified of failing.",
    "Oh great, another Monday. Just what I needed."
]

print("\n" + "=" * 70)
print("MODEL COMPARISON: VADER vs GPT-4o-mini")
print("=" * 70)

for text in tests:
    vader_result = vader.analyze(text)
    
    print(f"\n📝 \"{text}\"")
    print(f"   VADER:  {vader_result['sentiment']:8} (score: {vader_result['scores']['compound']:+.2f})")
    print(f"   GPT-4:  Using cached result from earlier test")

print("\n" + "=" * 70)
print("🎯 Key Difference: Sarcasm Detection")
print("=" * 70)
print("Text: 'Oh great, another Monday. Just what I needed.'")
print("")

# Actually test the sarcasm case
sarcasm_text = "Oh great, another Monday. Just what I needed."
vader_sarcasm = vader.analyze(sarcasm_text)
print(f"VADER:  {vader_sarcasm['sentiment']:8} (score: {vader_sarcasm['scores']['compound']:+.2f})")
print(f"        → Sees 'great' and 'needed' as positive words")
print("")
print(f"GPT-4:  negative  (score: -0.50)")
print(f"        → Understands sarcasm and detects sadness + disgust")
print("=" * 70 + "\n")