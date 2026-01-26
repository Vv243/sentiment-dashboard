"""
Content moderation service to detect harmful patterns.
"""
import re
import logging

logger = logging.getLogger(__name__)

class ContentModerator:
    """Detect harmful, toxic, or problematic content."""
    
    def __init__(self):
        logger.info("🛡️ Initializing content moderator...")
        
        # Harmful phrase patterns (case-insensitive)
        self.harmful_patterns = [
            # Self-harm suggestions
            r'\b(k[i1*]ll|hurt|harm)\s+(yourself|urself|yo?u?rself)\b',
            r'\bcommit\s+suicide\b',
            r'\bend\s+(your|yo?u?r)\s+life\b',
            r'\bgo\s+(k[i1*]ll|die)\b',
            
            # Direct threats
            r'\bi\s+(will|gonna|going\s+to)\s+(k[i1*]ll|hurt|harm)\s+you\b',
            r'\byou\s+(should|deserve\s+to)\s+die\b',
            
            # Hate speech patterns
            r'\bi\s+hate\s+you\b',
            r'\byou(\s+are|\'re)\s+(worthless|useless|garbage|trash)\b',
            
            # Harassment patterns with negation
            r'\bwhy\s+don\'?t\s+you\s+(just\s+)?(k[i1*]ll|die|leave)\b',
            r'\byou\s+should\s+(k[i1*]ll|die)\b',
        ]
        
        # Compile regex patterns
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.harmful_patterns
        ]
        
        logger.info(f"✅ Content moderator initialized with {len(self.harmful_patterns)} patterns")
    
    def check_content(self, text: str) -> dict:
        """
        Check if content contains harmful patterns.
        
        Args:
            text: The text to check
            
        Returns:
            dict with 'is_harmful', 'matched_pattern', 'severity', 'reason'
        """
        # Normalize text (handle censorship like k*ll, k1ll)
        normalized = text.lower()
        normalized = normalized.replace('*', 'i').replace('1', 'i').replace('!', 'i')
        
        # Check each pattern
        for i, pattern in enumerate(self.compiled_patterns):
            match = pattern.search(normalized)
            if match:
                logger.warning(f"⚠️ Harmful content detected: pattern #{i}")
                return {
                    'is_harmful': True,
                    'matched_pattern': self.harmful_patterns[i],
                    'matched_text': match.group(),
                    'severity': 'high',
                    'reason': 'Contains harmful or threatening language'
                }
        
        return {
            'is_harmful': False,
            'matched_pattern': None,
            'matched_text': None,
            'severity': 'safe',
            'reason': None
        }

# Global instance - THIS LINE CREATES THE INSTANCE!
content_moderator = ContentModerator()