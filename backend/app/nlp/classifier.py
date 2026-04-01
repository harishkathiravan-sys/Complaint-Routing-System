"""
NLP-based Complaint Classifier
Classifies complaints to appropriate departments using keyword matching
Keyword-based approach with optional sentiment analysis extension
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from enum import Enum

logger = logging.getLogger(__name__)

class Department(str, Enum):
    """Department enumeration"""
    CSE = "CSE"
    IT = "IT"
    ELECTRICAL = "ELECTRICAL"
    PLUMBING = "PLUMBING"
    ADMINISTRATION = "ADMINISTRATION"

# Keyword mappings for each department
DEPARTMENT_KEYWORDS: Dict[str, List[str]] = {
    "CSE": [
        "computer", "lab", "program", "software", "server", "coding", "system",
        "desktop", "workstation", "cpu", "processor", "memory", "ram", "disk",
        "monitor", "keyboard", "mouse", "application", "code", "debug", "compile",
        "terminal", "command", "script", "file", "database", "algorithm", "data structure",
        "machine learning", "ai", "python", "java", "c++", "javascript"
    ],
    "IT": [
        "wifi", "internet", "network", "router", "connection", "bandwidth", "speed",
        "ethernet", "lan", "wireless", "connectivity", "signal", "bridge", "gateway",
        "ip address", "dns", "ping", "latency", "server down", "network issue"
    ],
    "ELECTRICAL": [
        "light", "fan", "power", "electric", "voltage", "switch", "bulb", "lamp",
        "circuit", "breaker", "generator", "transformer", "wiring", "socket", "outlet",
        "power supply", "electricity", "blackout", "failure", "short circuit", "surge",
        "ac", "dc", "frequency", "phase"
    ],
    "PLUMBING": [
        "water", "leak", "pipe", "bathroom", "toilet", "drain", "tap", "sink",
        "faucet", "sewage", "clogged", "blockage", "leakage", "water supply", "shower",
        "flush", "pressure", "overflow", "water damage", "rust", "corrosion"
    ],
    "ADMINISTRATION": [
        "certificate", "office", "fees", "id card", "document", "approval", "admission",
        "registration", "application", "form", "deadline", "enrollment", "transcript",
        "pass", "exam", "grade", "result", "transcript", "hostel", "permission",
        "leave", "policy", "payment", "refund", "scholarship"
    ]
}

# Negative keywords that might indicate a department is WRONG
NEGATIVE_INDICATORS = {
    # If complaint has electrical terms, less likely to be IT
    "IT": ["power", "light", "bulb", "circuit", "voltage", "switch"],
    "ELECTRICAL": ["wifi", "internet", "network", "ethernet"],
    "CSE": ["water", "leak", "plumbing", "toilet"],
}

class ComplaintClassifier:
    """
    Complaint classifier using keyword-based NLP approach
    Can be extended with ML models (sklearn, spaCy)
    """
    
    def __init__(self):
        """Initialize classifier with keyword mappings"""
        self.keywords = DEPARTMENT_KEYWORDS
        self.departments = list(Department.__members__.keys())
        logger.info("Complaint Classifier initialized")
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess complaint text
        - Convert to lowercase
        - Remove special characters
        - Tokenize into words
        
        Args:
            text: Raw complaint text
            
        Returns:
            List of cleaned and lowercased words
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Split into words
        words = text.split()
        
        return words

    def get_keyword_scores(self, words: List[str]) -> Dict[str, int]:
        """
        Calculate keyword match scores for each department
        
        Args:
            words: Preprocessed words from complaint
            
        Returns:
            Dictionary with department scores
        """
        scores: Dict[str, int] = defaultdict(int)
        
        # Count keyword matches for each department
        for dept in self.departments:
            keywords = self.keywords.get(dept, [])
            
            for word in words:
                # Exact match or partial match (word in keyword)
                for keyword in keywords:
                    if word == keyword or (len(word) > 3 and word in keyword) or (keyword in word):
                        scores[dept] += 1
        
        return dict(scores)
    
    def apply_negative_indicators(self, scores: Dict[str, int], words: List[str]) -> Dict[str, int]:
        """
        Reduce scores for departments that don't match complaint content
        
        Args:
            scores: Current department scores
            words: Preprocessed words
            
        Returns:
            Adjusted scores
        """
        adjusted_scores = scores.copy()
        
        for dept, negative_keywords in NEGATIVE_INDICATORS.items():
            if dept in adjusted_scores:
                # Count negative indicators
                negative_count = sum(1 for neg_kw in negative_keywords if neg_kw in words)
                
                # Reduce score by negative count (but not below 0)
                adjusted_scores[dept] = max(0, adjusted_scores[dept] - (negative_count * 2))
        
        return adjusted_scores
    
    def classify(self, complaint_text: str) -> Tuple[str, float]:
        """
        Classify a complaint to the best matching department
        
        Args:
            complaint_text: The complaint text from student
            
        Returns:
            Tuple of (department_code, confidence_score)
            confidence_score is between 0-1
            
        Examples:
            "Computer lab PCs not working" -> ("CSE", 0.95)
            "WiFi is slow" -> ("IT", 0.92)
        """
        if not complaint_text or len(complaint_text.strip()) < 3:
            logger.warning("Invalid complaint text")
            return "ADMINISTRATION", 0.5  # Default to ADMINISTRATION
        
        # Preprocess
        words = self.preprocess_text(complaint_text)
        
        if not words:
            return "ADMINISTRATION", 0.5
        
        # Get keyword scores
        scores = self.get_keyword_scores(words)
        
        # Apply negative indicators
        scores = self.apply_negative_indicators(scores, words)
        
        # If no scores, default to ADMINISTRATION
        if not scores or max(scores.values()) == 0:
            logger.info(f"No keyword match found, defaulting to ADMINISTRATION")
            return "ADMINISTRATION", 0.5
        
        # Find department with highest score
        best_dept = max(scores, key=scores.get)
        best_score = scores[best_dept]
        
        # Calculate confidence (normalized score)
        # Maximum possible score is the length of words
        max_possible_score = len(words) * 1  # One match per keyword
        actual_score = best_score / max(max_possible_score, 1)
        confidence = min(actual_score * 2, 1.0)  # Scale up confidence, max 1.0
        
        logger.info(f"Classified complaint to {best_dept} with confidence {confidence:.2f}")
        logger.debug(f"Scores: {scores}")
        
        return best_dept, confidence
    
    def classify_with_scores(self, complaint_text: str) -> Dict[str, float]:
        """
        Get classification scores for all departments
        
        Args:
            complaint_text: The complaint text
            
        Returns:
            Dictionary with all department scores
        """
        words = self.preprocess_text(complaint_text)
        scores = self.get_keyword_scores(words)
        scores = self.apply_negative_indicators(scores, words)
        
        # Normalize scores to 0-1
        max_score = max(scores.values()) if scores else 1
        normalized = {dept: score / max(max_score, 1) for dept, score in scores.items()}
        
        # Ensure all departments are in result
        for dept in self.departments:
            if dept not in normalized:
                normalized[dept] = 0.0
        
        return normalized

# Global classifier instance
_classifier: Optional[ComplaintClassifier] = None

def get_classifier() -> ComplaintClassifier:
    """Get or create global classifier instance (singleton pattern)"""
    global _classifier
    if _classifier is None:
        _classifier = ComplaintClassifier()
    return _classifier

def classify_complaint(complaint_text: str) -> Tuple[str, float]:
    """
    Classify a complaint (convenience function)
    
    Args:
        complaint_text: The complaint text
        
    Returns:
        Tuple of (department_code, confidence_score)
    """
    classifier = get_classifier()
    return classifier.classify(complaint_text)

def get_classification_scores(complaint_text: str) -> Dict[str, float]:
    """
    Get scores for all departments (convenience function)
    
    Args:
        complaint_text: The complaint text
        
    Returns:
        Dictionary with department scores
    """
    classifier = get_classifier()
    return classifier.classify_with_scores(complaint_text)

if __name__ == "__main__":
    # Test the classifier
    test_complaints = [
        "The computer lab PCs are not working",
        "WiFi in the hostel is very slow",
        "There is water leakage in the bathroom",
        "The lights in classroom are not working",
        "Office is delaying certificate approval"
    ]
    
    classifier = ComplaintClassifier()
    
    print("Testing Complaint Classifier...")
    print("-" * 60)
    
    for complaint in test_complaints:
        dept, confidence = classifier.classify(complaint)
        print(f"\nComplaint: {complaint}")
        print(f"Classified to: {dept} (confidence: {confidence:.2%})")
