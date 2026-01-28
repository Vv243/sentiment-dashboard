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
            # Suicide - standalone (catches "suicide", "commit suicide", etc.)
            r'\bsuicide\b(?!\s+(prevention|hotline|awareness|help))',
            
            # Commit suicide variations
            r'\b(commit|committing|please commit|just commit|do commit)\s+suicide\b',
            r'\bsuicide\s+(please|now|today|tonight)\b',
            
            # Kill yourself variations
            r'\b(kill|k[i1*]ll)\s+(your)?self\b',
            r'\bkys\b',
            
            # Self-harm commands
            r'\b(hurt|harm)\s+(yourself|urself|yo?u?rself)\b',
            r'\bend\s+(your|yo?u?r)\s+(life|it all)\b',
            r'\btake\s+your\s+own\s+life\b',
            
            # Self-harm methods
            r'\b(hang|shoot|drown)\s+yourself\b',
            r'\b(jump\s+off|slit\s+your|overdose\s+on)\b',
            
            # Direct threats
            r'\bi\s+(will|gonna|going\s+to)\s+(k[i1*]ll|hurt|harm)\s+you\b',
            r'\byou\s+(should|deserve\s+to)\s+die\b',
            
            # Death wishes
            r'\bhope\s+you\s+die\b',
            r'\bwish\s+you\s+were\s+dead\b',
            
            # Hate speech
            r'\bi\s+hate\s+you\b',
            r'\byou(\s+are|\'re)\s+(worthless|useless|garbage|trash|waste of)\b',
            
            # Harassment with negation
            r'\bwhy\s+don\'?t\s+you\s+(just\s+)?(k[i1*]ll|die|leave|end it)\b',
            
            # Harmful encouragement
            r'\b(just do it|go ahead|nobody will miss you|no one cares)\b',
            
            # Racial slurs - N-word variations
            r'\bn[i1!*]+gg?[ae3][rhz]*\b',
            
            # Other racial slurs
            r'\bch[i1!*]nk\b',
            r'\bsp[i1!*]c\b',
            r'\bwetb[a@]ck\b',
            r'\bg[o0][o0]k\b',
            r'\bk[i1!*]ke\b',
            r'\brag\s*head\b',
            r'\bsand\s*n[i1!*]gg?[ae3]r\b',
            r'\bbeaner\b',
            r'\bcamel\s*jockey\b',
            
            # Homophobic slurs
            r'\bf[a@4]gg?[o0]t\b',
            r'\bd[y1]ke\b',
            r'\btr[a@4]nny\b',
            
            # Misogynistic slurs
            r'\bc[u*][n*]t\b',
            r'\bwh[o0]re\b',
            r'\bsl[u*]t\b',
            r'\bb[i1!*]tch\b',
            
            # Ableist slurs
            r'\bret[a@4]rd(ed)?\b',
            r'\bm[o0]ng?[o0]l[o0]id\b',
            r'\bcr[i1!*]pple\b',
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
        if not text:
            return {
                'is_harmful': False,
                'matched_pattern': None,
                'matched_text': None,
                'severity': 'safe',
                'reason': None
            }
        
        # Normalize text (handle censorship like k*ll, k1ll)
        normalized = text.lower()
        # Remove punctuation (keeps word boundaries intact)
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        # Handle censoring variations
        normalized = normalized.replace('*', 'i').replace('1', 'i').replace('@', 'a').replace('0', 'o')
        
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