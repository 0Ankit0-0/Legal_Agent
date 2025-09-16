"""
Enhanced Evidence Analysis Module for Legal AI Agents
"""

from typing import Dict, List, Tuple, Optional, Any
import re
from dataclasses import dataclass
from enum import Enum

class EvidenceType(Enum):
    PHYSICAL = "physical"
    DIGITAL = "digital" 
    TESTIMONIAL = "testimonial"
    DOCUMENTARY = "documentary"
    FORENSIC = "forensic"
    MEDICAL = "medical"

class RelevanceLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class EvidenceAnalysis:
    """Structured evidence analysis result"""
    evidence_id: str
    strength_score: float  # 0.0 to 1.0
    relevance_score: float  # 0.0 to 1.0
    admissibility_score: float  # 0.0 to 1.0
    key_points: List[str]
    potential_challenges: List[str]
    supporting_sections: List[str]

class EvidenceAnalyzer:
    """Advanced evidence analysis for legal proceedings"""
    
    def __init__(self, laws: Dict[str, Any]):
        self.laws = laws
        self.evidence_patterns = self._build_evidence_patterns()
        
    def _build_evidence_patterns(self) -> Dict[str, List[str]]:
        """Build patterns for different types of evidence"""
        return {
            "forensic": ["dna", "fingerprint", "blood", "trace", "ballistics", "fiber"],
            "medical": ["autopsy", "post-mortem", "injury", "cause of death", "toxicology"],
            "digital": ["email", "message", "phone", "computer", "encrypted", "data"],
            "witness": ["testimony", "statement", "saw", "heard", "observed", "witnessed"],
            "physical": ["weapon", "clothing", "object", "material", "substance"],
            "documentary": ["contract", "receipt", "record", "document", "certificate"]
        }
    
    def analyze_evidence(self, evidence: Dict[str, Any], case_context: Dict[str, Any]) -> EvidenceAnalysis:
        """Comprehensive analysis of a single piece of evidence"""
        
        evidence_text = evidence.get("text", "").lower()
        evidence_type = evidence.get("type", "").lower()
        filename = evidence.get("filename", "")
        
        # Calculate strength score
        strength_score = self._calculate_strength_score(evidence, case_context)
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(evidence, case_context)
        
        # Calculate admissibility score
        admissibility_score = self._calculate_admissibility_score(evidence)
        
        # Extract key points
        key_points = self._extract_key_points(evidence, case_context)
        
        # Identify potential challenges
        challenges = self._identify_challenges(evidence)
        
        # Find supporting legal sections
        supporting_sections = self._find_supporting_sections(evidence, case_context)
        
        return EvidenceAnalysis(
            evidence_id=filename,
            strength_score=strength_score,
            relevance_score=relevance_score,
            admissibility_score=admissibility_score,
            key_points=key_points,
            potential_challenges=challenges,
            supporting_sections=supporting_sections
        )
    
    def _calculate_strength_score(self, evidence: Dict[str, Any], case_context: Dict[str, Any]) -> float:
        """Calculate the strength/reliability of evidence"""
        score = 0.5  # Base score
        
        evidence_type = evidence.get("type", "").lower()
        evidence_text = evidence.get("text", "").lower()
        
        # Type-based scoring
        type_scores = {
            "forensic": 0.9,
            "medical": 0.85,
            "digital": 0.7,
            "physical": 0.75,
            "documentary": 0.65,
            "testimonial": 0.6,
            "witness": 0.55
        }
        
        for etype, tscore in type_scores.items():
            if etype in evidence_type:
                score = max(score, tscore)
                break
        
        # Content quality indicators
        quality_indicators = {
            "scientific": 0.1, "laboratory": 0.1, "certified": 0.1,
            "expert": 0.08, "professional": 0.08, "official": 0.08,
            "chain of custody": 0.12, "authenticated": 0.1,
            "corroborated": 0.09, "independent": 0.07
        }
        
        for indicator, bonus in quality_indicators.items():
            if indicator in evidence_text:
                score = min(1.0, score + bonus)
        
        # Reliability detractors
        detractors = {
            "hearsay": -0.15, "speculation": -0.1, "opinion": -0.05,
            "biased": -0.1, "interested party": -0.08, "contaminated": -0.2
        }
        
        for detractor, penalty in detractors.items():
            if detractor in evidence_text:
                score = max(0.0, score + penalty)
        
        return min(1.0, max(0.0, score))
    
    def _calculate_relevance_score(self, evidence: Dict[str, Any], case_context: Dict[str, Any]) -> float:
        """Calculate relevance to the case"""
        evidence_text = evidence.get("text", "").lower()
        case_summary = case_context.get("summary", "").lower()
        case_type = case_context.get("type", "").lower()
        
        # Direct relevance based on case keywords
        case_keywords = case_summary.split()
        evidence_keywords = evidence_text.split()
        
        common_keywords = set(case_keywords) & set(evidence_keywords)
        keyword_score = min(0.4, len(common_keywords) * 0.02)
        
        # Relevance based on case type
        type_relevance = {
            "murder": ["cause of death", "weapon", "motive", "opportunity", "intent"],
            "theft": ["stolen property", "possession", "value", "intent to steal"],
            "fraud": ["deception", "financial loss", "misrepresentation", "intent"],
            "assault": ["injury", "force", "intent to harm", "weapon"]
        }
        
        relevance_score = keyword_score
        for case_t, relevant_terms in type_relevance.items():
            if case_t in case_type:
                for term in relevant_terms:
                    if term in evidence_text:
                        relevance_score = min(1.0, relevance_score + 0.15)
        
        # Specific relevance indicators
        if evidence.get("relevance", "").lower() == "critical":
            relevance_score = min(1.0, relevance_score + 0.3)
        elif evidence.get("relevance", "").lower() == "high":
            relevance_score = min(1.0, relevance_score + 0.2)
        elif evidence.get("relevance", "").lower() == "medium":
            relevance_score = min(1.0, relevance_score + 0.1)
        
        return min(1.0, max(0.0, relevance_score))
    
    def _calculate_admissibility_score(self, evidence: Dict[str, Any]) -> float:
        """Calculate likelihood of evidence being admitted in court"""
        score = 0.8  # Default high admissibility
        
        evidence_text = evidence.get("text", "").lower()
        
        # Admissibility enhancers
        enhancers = {
            "chain of custody": 0.1, "authenticated": 0.1, "certified": 0.08,
            "expert testimony": 0.08, "scientific": 0.08, "official record": 0.1
        }
        
        for enhancer, bonus in enhancers.items():
            if enhancer in evidence_text:
                score = min(1.0, score + bonus)
        
        # Admissibility concerns
        concerns = {
            "hearsay": -0.3, "privileged": -0.5, "illegally obtained": -0.8,
            "contaminated": -0.4, "unreliable": -0.3, "prejudicial": -0.2
        }
        
        for concern, penalty in concerns.items():
            if concern in evidence_text:
                score = max(0.0, score + penalty)
        
        return min(1.0, max(0.0, score))
    
    def _extract_key_points(self, evidence: Dict[str, Any], case_context: Dict[str, Any]) -> List[str]:
        """Extract key points from evidence"""
        evidence_text = evidence.get("text", "")
        key_points = []
        
        # Look for specific patterns
        patterns = [
            r"shows?\s+([^.]{20,100})",
            r"indicates?\s+([^.]{20,100})",
            r"confirms?\s+([^.]{20,100})",
            r"establishes?\s+([^.]{20,100})",
            r"proves?\s+([^.]{20,100})"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, evidence_text, re.IGNORECASE)
            key_points.extend([match.strip() for match in matches[:3]])
        
        # Extract numerical data
        numbers = re.findall(r'\b\d+(?:\.\d+)?(?:\s*(?:mg|ml|cm|mm|hours?|minutes?|days?|%|percent))\b', evidence_text)
        if numbers:
            key_points.append(f"Numerical data: {', '.join(numbers[:3])}")
        
        # Extract dates and times
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', evidence_text)
        if dates:
            key_points.append(f"Temporal information: {', '.join(dates[:2])}")
        
        return key_points[:5]  # Top 5 key points
    
    def _identify_challenges(self, evidence: Dict[str, Any]) -> List[str]:
        """Identify potential challenges to the evidence"""
        evidence_text = evidence.get("text", "").lower()
        challenges = []
        
        challenge_indicators = {
            "chain of custody": "Chain of custody issues may affect admissibility",
            "contamination": "Potential contamination questions reliability",
            "hearsay": "May be challenged as hearsay evidence",
            "bias": "Witness bias may affect credibility",
            "speculation": "Contains speculative elements that may be objected to",
            "opinion": "Opinion testimony may require expert qualification",
            "prejudicial": "May be more prejudicial than probative"
        }
        
        for indicator, challenge in challenge_indicators.items():
            if indicator in evidence_text:
                challenges.append(challenge)
        
        # Generic challenges based on evidence type
        evidence_type = evidence.get("type", "").lower()
        if "witness" in evidence_type or "testimony" in evidence_type:
            challenges.append("Witness credibility and memory accuracy")
        
        if "digital" in evidence_type:
            challenges.append("Digital evidence authentication and integrity")
        
        return challenges[:4]  # Top 4 challenges
    
    def _find_supporting_sections(self, evidence: Dict[str, Any], case_context: Dict[str, Any]) -> List[str]:
        """Find IPC sections that this evidence supports"""
        evidence_text = evidence.get("text", "").lower()
        case_summary = case_context.get("summary", "").lower()
        supporting_sections = []
        
        for section_num, section_data in self.laws.get("ipc", {}).items():
            section_keywords = [kw.lower() for kw in section_data.get("keywords", [])]
            
            # Check if evidence supports this section
            keyword_matches = sum(1 for kw in section_keywords if kw in evidence_text)
            case_matches = sum(1 for kw in section_keywords if kw in case_summary)
            
            if keyword_matches >= 1 and case_matches >= 1:
                supporting_sections.append(section_num)
        
        return supporting_sections[:3]  # Top 3 supporting sections
    
    def rank_evidence_by_strength(self, evidence_list: List[Dict], case_context: Dict) -> List[Tuple[Dict, EvidenceAnalysis]]:
        """Rank all evidence by overall strength for the case"""
        analyzed_evidence = []
        
        for evidence in evidence_list:
            analysis = self.analyze_evidence(evidence, case_context)
            overall_score = (
                analysis.strength_score * 0.4 + 
                analysis.relevance_score * 0.4 + 
                analysis.admissibility_score * 0.2
            )
            analyzed_evidence.append((evidence, analysis, overall_score))
        
        # Sort by overall score
        analyzed_evidence.sort(key=lambda x: x[2], reverse=True)
        
        return [(ev, analysis) for ev, analysis, score in analyzed_evidence]
    
    def generate_evidence_summary(self, evidence_list: List[Dict], case_context: Dict) -> Dict[str, Any]:
        """Generate comprehensive evidence summary"""
        ranked_evidence = self.rank_evidence_by_strength(evidence_list, case_context)
        
        total_evidence = len(evidence_list)
        strong_evidence = sum(1 for _, analysis in ranked_evidence if analysis.strength_score > 0.7)
        admissible_evidence = sum(1 for _, analysis in ranked_evidence if analysis.admissibility_score > 0.6)
        
        summary = {
            "total_evidence_pieces": total_evidence,
            "strong_evidence_count": strong_evidence,
            "admissible_evidence_count": admissible_evidence,
            "strongest_evidence": ranked_evidence[0] if ranked_evidence else None,
            "evidence_gaps": self._identify_evidence_gaps(evidence_list, case_context),
            "overall_case_strength": self._calculate_overall_case_strength(ranked_evidence)
        }
        
        return summary
    
    def _identify_evidence_gaps(self, evidence_list: List[Dict], case_context: Dict) -> List[str]:
        """Identify potential gaps in evidence"""
        case_type = case_context.get("type", "").lower()
        gaps = []
        
        evidence_types = [ev.get("type", "").lower() for ev in evidence_list]
        evidence_text = " ".join([ev.get("text", "") for ev in evidence_list]).lower()
        
        # Standard evidence expectations by case type
        if "murder" in case_type:
            if not any("medical" in et or "forensic" in et for et in evidence_types):
                gaps.append("Missing medical/forensic evidence for cause of death")
            if "motive" not in evidence_text:
                gaps.append("Motive not clearly established")
            if "weapon" not in evidence_text:
                gaps.append("Murder weapon not identified")
        
        if "theft" in case_type:
            if "value" not in evidence_text:
                gaps.append("Value of stolen property not established")
            if not any("possession" in et for et in evidence_types):
                gaps.append("Possession of stolen goods not proven")
        
        # General gaps
        if not any("witness" in et for et in evidence_types):
            gaps.append("No witness testimony available")
        
        return gaps
    
    def _calculate_overall_case_strength(self, ranked_evidence: List[Tuple[Dict, EvidenceAnalysis]]) -> float:
        """Calculate overall strength of the case based on evidence"""
        if not ranked_evidence:
            return 0.0
        
        # Weighted scoring - strongest evidence has more impact
        total_score = 0.0
        weight_sum = 0.0
        
        for i, (evidence, analysis) in enumerate(ranked_evidence):
            weight = 1.0 / (i + 1)  # Decreasing weight for lower-ranked evidence
            evidence_score = (
                analysis.strength_score * 0.5 + 
                analysis.relevance_score * 0.3 + 
                analysis.admissibility_score * 0.2
            )
            total_score += evidence_score * weight
            weight_sum += weight
        
        return min(1.0, total_score / weight_sum if weight_sum > 0 else 0.0)

# Example usage
if __name__ == "__main__":
    # Sample laws data
    laws = {
        "ipc": {
            "302": {
                "title": "Murder",
                "keywords": ["murder", "kill", "death", "intention", "unlawful"]
            }
        }
    }
    
    # Sample evidence
    evidence_list = [
        {
            "filename": "PostMortem.pdf",
            "type": "medical",
            "text": "Post-mortem examination confirms death by poisoning. Toxicology shows presence of cyanide.",
            "relevance": "critical"
        }
    ]
    
    case_context = {
        "type": "murder case",
        "summary": "Accused poisoned victim with cyanide during dinner party"
    }
    
    analyzer = EvidenceAnalyzer(laws)
    analysis = analyzer.analyze_evidence(evidence_list[0], case_context)
    
    print(f"Evidence Analysis:")
    print(f"Strength Score: {analysis.strength_score:.2f}")
    print(f"Relevance Score: {analysis.relevance_score:.2f}")
    print(f"Key Points: {analysis.key_points}")
    print(f"Challenges: {analysis.potential_challenges}")