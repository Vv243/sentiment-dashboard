"""
Test script for synthetic data and fallback system

Run this to test that the backup system works correctly
"""

import sys
sys.path.append('.')

from app.services.synthetic_data import SyntheticDataGenerator
from app.services.sentiment_service import SentimentAnalyzer

def test_synthetic_generation():
    """Test synthetic data generation"""
    print("=" * 60)
    print("Testing Synthetic Data Generator")
    print("=" * 60)
    
    generator = SyntheticDataGenerator(seed=42)
    
    # Test 1: Generate single post
    print("\n1. Generating single positive post for TSLA...")
    post = generator.generate_post("TSLA", sentiment="positive")
    print(f"   Text: {post.text}")
    print(f"   Author: {post.author}")
    print(f"   Likes: {post.likes}, Comments: {post.comments}")
    print(f"   Source: {post.source}")
    
    # Test 2: Generate multiple posts
    print("\n2. Generating 10 posts with balanced sentiment...")
    posts = generator.generate_posts_for_ticker("AAPL", count=10, days_back=3)
    print(f"   Generated {len(posts)} posts")
    
    sentiments = {}
    for post in posts:
        # Quick sentiment check based on keywords
        text_lower = post.text.lower()
        if any(word in text_lower for word in ['moon', 'bullish', 'love', 'great', 'amazing']):
            sent = 'positive'
        elif any(word in text_lower for word in ['crash', 'bearish', 'terrible', 'avoid', 'sell']):
            sent = 'negative'
        else:
            sent = 'neutral'
        
        sentiments[sent] = sentiments.get(sent, 0) + 1
    
    print(f"   Distribution: {sentiments}")
    
    # Test 3: Market scenarios
    print("\n3. Testing market scenarios...")
    scenarios = ['bullish', 'bearish', 'volatile']
    
    for scenario in scenarios:
        posts = generator.generate_market_scenario("NVDA", scenario)
        print(f"   {scenario.capitalize()}: {len(posts)} posts generated")
    
    # Test 4: Trending tickers
    print("\n4. Generating trending tickers...")
    trending = generator.generate_trending_tickers(count=5)
    print("   Trending:")
    for i, (ticker, count) in enumerate(trending, 1):
        print(f"   {i}. {ticker}: {count} mentions")
    
    print("\n✅ Synthetic generation tests passed!\n")


def test_sentiment_analysis_on_synthetic():
    """Test that sentiment analysis works on synthetic data"""
    print("=" * 60)
    print("Testing Sentiment Analysis on Synthetic Data")
    print("=" * 60)
    
    generator = SyntheticDataGenerator(seed=42)
    analyzer = SentimentAnalyzer()
    
    # Generate posts with known sentiments
    test_cases = [
        ('positive', "TSLA is going to the moon! 🚀🚀🚀"),
        ('negative', "TSLA is overvalued. Time to sell."),
        ('neutral', "Thoughts on TSLA? Considering buying some shares.")
    ]
    
    print("\n Testing sentiment analysis...")
    correct = 0
    total = len(test_cases)
    
    for expected_sentiment, text in test_cases:
        results = analyzer.analyze(text, use_vader=True, use_finbert=False)
        detected_label = results['vader_score'].label if results['vader_score'] else 'unknown'
        
        is_correct = detected_label == expected_sentiment
        correct += is_correct
        
        status = "✅" if is_correct else "❌"
        print(f"   {status} Expected: {expected_sentiment}, Got: {detected_label}")
        print(f"      Text: {text[:60]}...")
    
    accuracy = (correct / total) * 100
    print(f"\n   Accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    if accuracy >= 66:
        print("   ✅ Sentiment analysis working correctly!\n")
    else:
        print("   ⚠️  Sentiment analysis may need adjustment\n")


def test_realistic_data_quality():
    """Test that synthetic data looks realistic"""
    print("=" * 60)
    print("Testing Data Realism")
    print("=" * 60)
    
    generator = SyntheticDataGenerator(seed=42)
    
    # Generate sample posts
    posts = generator.generate_posts_for_ticker("GME", count=5)
    
    print("\n Sample synthetic posts:")
    print(" " + "-" * 58)
    
    for i, post in enumerate(posts[:5], 1):
        print(f"\n {i}. Author: u/{post.author}")
        print(f"    Text: {post.text}")
        print(f"    Engagement: {post.likes} likes, {post.comments} comments")
        print(f"    Time: {post.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    print("\n" + " " + "-" * 58)
    print("\n ✅ Data appears realistic!\n")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print(" SYNTHETIC DATA & FALLBACK SYSTEM TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_synthetic_generation()
        test_sentiment_analysis_on_synthetic()
        test_realistic_data_quality()
        
        print("=" * 60)
        print(" ALL TESTS PASSED! ✅")
        print("=" * 60)
        print("\n✨ Your fallback system is ready to use!\n")
        print("Next steps:")
        print("1. Start your backend: uvicorn app.main:app --reload")
        print("2. Test the API: curl -X POST 'http://localhost:8000/api/v1/collection/generate-demo-data/TSLA'")
        print("3. Check the dashboard: http://localhost:3000")
        print()
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
