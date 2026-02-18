"""
Quick test script to verify OpenAI integration works.
Run with: python test_openai_quick.py
This is NOT part of the test suite - it makes real API calls.
"""

from app.services.openai_analyzer import OpenAIAnalyzer, analyze_with_cache

analyzer = OpenAIAnalyzer()

test_cases = [
    ("Simple positive",   "I love this product, it's amazing!"),
    ("Simple negative",   "This is absolutely terrible and I hate it."),
    ("Neutral",           "The meeting is scheduled for 3pm on Thursday."),
    ("Complex emotions",  "I'm so excited about the new job, but also terrified of failing."),
    ("Sarcasm",           "Oh great, another Monday. Just what I needed."),
]

print("=" * 60)
print("OpenAI GPT-4o-mini Sentiment Analysis Test")
print("=" * 60)

for label, text in test_cases:
    print(f"\n📝 {label}")
    print(f"   Text: \"{text}\"")
    
    result = analyzer.analyze(text)
    
    if result.get("error"):
        print(f"   ❌ Error: {result['error']}")
    else:
        score = result.get("compound_score", 0)
        bar = "█" * int(abs(score) * 20)
        direction = "+" if score >= 0 else "-"
        
        print(f"   Sentiment:  {result['sentiment'].upper()}")
        print(f"   Confidence: {result['confidence']:.0%}")
        print(f"   Score:      {direction}{abs(score):.2f}  [{bar}]")
        print(f"   Emotions:   {', '.join(result['emotions']) or 'none detected'}")
        print(f"   Reasoning:  {result['reasoning']}")

print("\n" + "=" * 60)
print("Cache test: sending 'I love this!' twice...")
r1 = analyze_with_cache("I love this!")
r2 = analyze_with_cache("I love this!")
print(f"   First call  - cached: {r1['cached']}")
print(f"   Second call - cached: {r2['cached']}")
print("=" * 60)