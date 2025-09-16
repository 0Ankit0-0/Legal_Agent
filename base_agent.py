import logging
from typing import Dict, List, Optional, Tuple, Any, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all legal agents with AI integration capabilities."""
    
    def __init__(self, name: str, role: str, case_data: Dict, evidence: List[Dict], laws: Dict):
        # Input validation
        if not all([name, role, case_data, evidence, laws]):
            raise ValueError("All parameters (name, role, case_data, evidence, laws) are required")
        
        self.name = name
        self.role = role
        self.case_data = case_data
        self.evidence = evidence
        self.laws = laws
        self.memory = []
        
        # AI integration properties
        self.local_model = None
        self.pretrained_model = None
        self.api_client = None
        
        logger.info(f"Initialized {self.__class__.__name__} agent: {name} as {role}")

    def set_ai_models(self, local_model=None, pretrained_model=None, api_client=None):
        """Set AI models for fallback mechanism."""
        self.local_model = local_model
        self.pretrained_model = pretrained_model
        self.api_client = api_client
        logger.info(f"AI models configured for {self.name}: Local={bool(local_model)}, Pretrained={bool(pretrained_model)}, API={bool(api_client)}")

    def think(self, last_statement: Optional[str] = None) -> Tuple[str, Optional[str], Any]:
        """
        Plan what to say based on case facts, role, and last statement from other agent.
        Returns: (thought_process: str, target_evidence: str or None, additional_data: any)
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def speak(self, thought_result: Tuple[str, Optional[str], Any]) -> Dict[str, Any]:
        """Generate a final statement from the thought result.
        Returns: dict { 'role': str, 'statement': str, 'thought': str, 'evidence': optional filename }
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def remember(self, statement: str, thought: str) -> None:
        """Save to agents memory for future turn."""
        self.memory.append({"statement": statement, "thought": thought})

    def get_relevant_evidence(self, keywords: List[str]) -> List[Dict]:
        """Helper method to find relevant evidence based on keywords."""
        if not keywords:
            return []
        
        relevant_evidence = []
        for ev in self.evidence:
            # Check both text content and filename for keywords
            ev_text = ev.get("text", "").lower()
            ev_filename = ev.get("filename", "").lower()
            
            if any(keyword.lower() in ev_text or keyword.lower() in ev_filename for keyword in keywords):
                relevant_evidence.append(ev)
        
        # Sort by relevance score
        def relevance_score(evidence):
            relevance = evidence.get("relevance", "").lower()
            if relevance == "critical":
                return 3
            elif relevance == "high":
                return 2
            elif relevance == "medium":
                return 1
            return 0
        
        relevant_evidence.sort(key=relevance_score, reverse=True)
        return relevant_evidence

    def _try_ai_generation(self, prompt: str, method_name: str) -> Optional[Dict[str, Any]]:
        """
        Common AI generation method with fallback mechanism.
        Returns: dict with 'thought', 'evidence', and optional 'section' keys
        """
        
        # 1. Try local model first
        if self.local_model:
            try:
                logger.info(f"Attempting {method_name} with local model for {self.name}")
                result = getattr(self.local_model, method_name, None)
                if result:
                    response = result(self.case_data, prompt, self.evidence, self.laws)
                    logger.info(f"Local model {method_name} successful for {self.name}")
                    return response
            except Exception as e:
                logger.warning(f"Local model {method_name} failed for {self.name}: {e}")

        # 2. Try pretrained model
        if self.pretrained_model:
            try:
                logger.info(f"Attempting {method_name} with pretrained model for {self.name}")
                result = getattr(self.pretrained_model, method_name, None)
                if result:
                    response = result(self.case_data, prompt, self.evidence, self.laws)
                    logger.info(f"Pretrained model {method_name} successful for {self.name}")
                    return response
            except Exception as e:
                logger.warning(f"Pretrained model {method_name} failed for {self.name}: {e}")

        # 3. Try API clients
        if self.api_client:
            # Try Gemini API
            if "gemini" in self.api_client:
                try:
                    logger.info(f"Attempting {method_name} with Gemini API for {self.name}")
                    
                    # Enhanced prompt for better responses
                    enhanced_prompt = f"""
                    You are a {self.role} in an Indian legal proceeding.
                    
                    {prompt}
                    
                    Please respond in JSON format with:
                    {{
                        "thought": "Your detailed reasoning process as a {self.role}",
                        "evidence": "Filename of most relevant evidence (if applicable)",
                        "section": "Most applicable IPC section number (if applicable)"
                    }}
                    
                    Ensure your response is professional, legally sound, and appropriate for Indian legal context.
                    """
                    
                    response = self.api_client["gemini"].generate(enhanced_prompt)
                    logger.info(f"Gemini API {method_name} successful for {self.name}")
                    
                    # Try to parse as JSON, fallback to simple format
                    try:
                        import json
                        if isinstance(response.get("thought"), str) and response["thought"].strip().startswith("{"):
                            parsed = json.loads(response["thought"])
                            return {
                                "thought": parsed.get("thought", response.get("thought", "")),
                                "evidence": parsed.get("evidence", response.get("evidence", None)),
                                "section": parsed.get("section", response.get("section", None))
                            }
                    except:
                        pass
                    
                    return {
                        "thought": response.get("thought", ""),
                        "evidence": response.get("evidence", None),
                        "section": response.get("section", None)
                    }
                except Exception as e:
                    logger.warning(f"Gemini API {method_name} failed for {self.name}: {e}")

            # Try OpenAI API
            openai_keys = ["chatgpt", "OpenAI", "openai"]
            for key in openai_keys:
                if key in self.api_client:
                    try:
                        logger.info(f"Attempting {method_name} with OpenAI API ({key}) for {self.name}")
                        response = self.api_client[key].generate(prompt)
                        logger.info(f"OpenAI API {method_name} successful for {self.name}")
                        return {
                            "thought": response.get("thought", ""),
                            "evidence": response.get("evidence", None),
                            "section": response.get("section", None)
                        }
                    except Exception as e:
                        logger.warning(f"OpenAI API {method_name} failed for {self.name}: {e}")
                    break

        logger.warning(f"All AI generation methods failed for {method_name} - {self.name}")
        return None

    def _create_base_prompt(self, last_statement: Optional[str] = None) -> str:
        """Create base prompt with case information."""
        prompt = f"""
        CASE INFORMATION:
        Title: {self.case_data.get('title', 'Unknown Case')}
        Type: {self.case_data.get('type', 'Criminal Case')}
        Description: {self.case_data.get('description', '')}
        Summary: {self.case_data.get('summary', '')}
        
        AVAILABLE EVIDENCE:
        """
        
        for i, ev in enumerate(self.evidence, 1):
            prompt += f"{i}. {ev.get('filename', 'Unknown')} ({ev.get('type', 'unknown')} - {ev.get('relevance', 'unknown')} relevance)\n"
            prompt += f"   Content: {ev.get('text', 'No description')}\n"
        
        prompt += f"\nAPPLICABLE LAWS:\n"
        for section, law_info in self.laws.get('ipc', {}).items():
            prompt += f"Section {section}: {law_info.get('title', '')} - {law_info.get('description', '')}\n"
        
        if last_statement:
            prompt += f"\nLAST STATEMENT FROM OTHER PARTY: {last_statement}"
        
        if self.memory:
            prompt += f"\nPREVIOUS STATEMENTS IN THIS CASE: "
            for mem in self.memory[-3:]:  # Last 3 for context
                prompt += f"- {mem['statement'][:100]}...\n"
        
        prompt += f"\nYOUR ROLE: {self.role.upper()}"
        prompt += f"\nYOUR NAME: {self.name}"
        
        return prompt

    def get_memory_summary(self) -> str:
        """Get a summary of the agent's memory for context."""
        if not self.memory:
            return "No previous statements."
        
        summary = f"Previous {len(self.memory)} statement(s):\n"
        for i, mem in enumerate(self.memory[-5:], 1):  # Last 5 statements
            summary += f"{i}. {mem['statement'][:150]}...\n"
        
        return summary

    def analyze_opponent_strategy(self, opponent_statements: List[str]) -> Dict[str, Any]:
        """Analyze opponent's strategy based on their statements."""
        if not opponent_statements:
            return {"strategy": "unknown", "weaknesses": [], "strengths": []}
        
        # Simple keyword analysis
        all_text = " ".join(opponent_statements).lower()
        
        # Identify legal strategies
        strategies = []
        if any(word in all_text for word in ["reasonable doubt", "burden of proof", "insufficient evidence"]):
            strategies.append("burden_of_proof_challenge")
        
        if any(word in all_text for word in ["alibi", "elsewhere", "not present"]):
            strategies.append("alibi_defense")
        
        if any(word in all_text for word in ["self-defense", "justified", "protection"]):
            strategies.append("justification")
        
        if any(word in all_text for word in ["circumstantial", "indirect", "speculation"]):
            strategies.append("circumstantial_evidence_attack")
        
        return {
            "strategies": strategies,
            "statement_count": len(opponent_statements),
            "average_length": sum(len(s) for s in opponent_statements) / len(opponent_statements),
            "key_themes": self._extract_key_themes(all_text)
        }
    
    def _extract_key_themes(self, text: str) -> List[str]:
        """Extract key themes from opponent statements."""
        legal_terms = [
            "evidence", "witness", "alibi", "motive", "intent", "reasonable doubt",
            "burden of proof", "circumstantial", "direct", "testimony", "forensic",
            "guilty", "innocent", "verdict", "sentence", "conviction", "acquittal"
        ]
        
        themes = []
        for term in legal_terms:
            if term in text:
                themes.append(term)
        
        return themes[:10]  # Top 10 themes