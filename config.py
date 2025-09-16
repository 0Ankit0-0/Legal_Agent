"""
Configuration settings for Legal AI Simulation System
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class AIProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    LOCAL = "local"
    RULE_BASED = "rule_based"

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass
class SimulationSettings:
    """Settings for courtroom simulation behavior"""
    min_rounds: int = 6
    max_rounds: int = 15
    enable_early_verdict: bool = True
    detailed_evidence_analysis: bool = True
    save_transcripts: bool = True
    transcript_format: str = "json"  # json, txt, html
    
@dataclass 
class AISettings:
    """AI model configuration"""
    preferred_provider: AIProvider = AIProvider.GEMINI
    fallback_providers: List[AIProvider] = None
    gemini_model: str = "gemini-pro"
    openai_model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    
    def __post_init__(self):
        if self.fallback_providers is None:
            self.fallback_providers = [AIProvider.RULE_BASED]

@dataclass
class OutputSettings:
    """Output and display configuration"""
    show_thinking_process: bool = True
    show_evidence_analysis: bool = True
    show_legal_citations: bool = True
    colored_output: bool = True
    save_reports: bool = True
    report_directory: str = "reports"

class Config:
    """Main configuration class"""
    
    def __init__(self):
        # Load from environment variables or use defaults
        self.simulation = SimulationSettings(
            min_rounds=int(os.getenv("SIM_MIN_ROUNDS", "6")),
            max_rounds=int(os.getenv("SIM_MAX_ROUNDS", "15")),
            enable_early_verdict=os.getenv("SIM_EARLY_VERDICT", "true").lower() == "true",
            detailed_evidence_analysis=os.getenv("SIM_EVIDENCE_ANALYSIS", "true").lower() == "true"
        )
        
        self.ai = AISettings(
            preferred_provider=AIProvider(os.getenv("AI_PROVIDER", "gemini")),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-pro"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            max_tokens=int(os.getenv("AI_MAX_TOKENS", "1000")),
            temperature=float(os.getenv("AI_TEMPERATURE", "0.7"))
        )
        
        self.output = OutputSettings(
            show_thinking_process=os.getenv("SHOW_THINKING", "true").lower() == "true",
            show_evidence_analysis=os.getenv("SHOW_EVIDENCE", "true").lower() == "true",
            colored_output=os.getenv("COLORED_OUTPUT", "true").lower() == "true",
            save_reports=os.getenv("SAVE_REPORTS", "true").lower() == "true",
            report_directory=os.getenv("REPORT_DIR", "reports")
        )
        
        # API Keys
        self.api_keys = {
            "gemini": os.getenv("GEMINI_API_KEY"),
            "openai": os.getenv("OPENAI_API_KEY")
        }
        
        # Legal database settings
        self.legal_db = {
            "ipc_sections_file": os.getenv("IPC_SECTIONS_FILE", "data/ipc_sections.json"),
            "case_precedents_file": os.getenv("CASE_PRECEDENTS_FILE", "data/case_precedents.json"),
            "evidence_templates_file": os.getenv("EVIDENCE_TEMPLATES_FILE", "data/evidence_templates.json")
        }
        
        # Performance settings
        self.performance = {
            "max_memory_items": int(os.getenv("MAX_MEMORY_ITEMS", "10")),
            "evidence_analysis_timeout": int(os.getenv("EVIDENCE_TIMEOUT", "30")),
            "ai_response_timeout": int(os.getenv("AI_TIMEOUT", "60"))
        }
    
    def get_api_client(self, provider: AIProvider):
        """Get configured API client for specified provider"""
        if provider == AIProvider.GEMINI:
            return self._get_gemini_client()
        elif provider == AIProvider.OPENAI:
            return self._get_openai_client()
        else:
            return None
    
    def _get_gemini_client(self):
        """Initialize Gemini API client"""
        api_key = self.api_keys.get("gemini")
        if not api_key:
            return None
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            class GeminiClient:
                def __init__(self, model_name, max_tokens, temperature):
                    self.model = genai.GenerativeModel(model_name)
                    self.max_tokens = max_tokens
                    self.temperature = temperature
                
                def generate(self, prompt):
                    try:
                        generation_config = {
                            'temperature': self.temperature,
                            'max_output_tokens': self.max_tokens,
                        }
                        
                        response = self.model.generate_content(
                            prompt,
                            generation_config=generation_config
                        )
                        
                        return {
                            "thought": response.text,
                            "evidence": None,
                            "section": None
                        }
                    except Exception as e:
                        print(f"Gemini API error: {e}")
                        raise
            
            return GeminiClient(self.ai.gemini_model, self.ai.max_tokens, self.ai.temperature)
            
        except ImportError:
            print("google-generativeai package not installed")
            return None
        except Exception as e:
            print(f"Failed to initialize Gemini client: {e}")
            return None
    
    def _get_openai_client(self):
        """Initialize OpenAI API client"""
        api_key = self.api_keys.get("openai")
        if not api_key:
            return None
        
        try:
            import openai
            
            class OpenAIClient:
                def __init__(self, api_key, model, max_tokens, temperature):
                    self.client = openai.OpenAI(api_key=api_key)
                    self.model = model
                    self.max_tokens = max_tokens
                    self.temperature = temperature
                
                def generate(self, prompt):
                    try:
                        response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=self.max_tokens,
                            temperature=self.temperature
                        )
                        
                        return {
                            "thought": response.choices[0].message.content,
                            "evidence": None,
                            "section": None
                        }
                    except Exception as e:
                        print(f"OpenAI API error: {e}")
                        raise
            
            return OpenAIClient(api_key, self.ai.openai_model, self.ai.max_tokens, self.ai.temperature)
            
        except ImportError:
            print("openai package not installed")
            return None
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {e}")
            return None
    
    def get_available_providers(self) -> List[AIProvider]:
        """Get list of available AI providers based on API keys"""
        available = []
        
        if self.api_keys.get("gemini"):
            available.append(AIProvider.GEMINI)
        
        if self.api_keys.get("openai"):
            available.append(AIProvider.OPENAI)
        
        # Rule-based is always available
        available.append(AIProvider.RULE_BASED)
        
        return available
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Check simulation settings
        if self.simulation.min_rounds < 1:
            issues.append("Minimum rounds must be at least 1")
        
        if self.simulation.max_rounds < self.simulation.min_rounds:
            issues.append("Maximum rounds must be >= minimum rounds")
        
        # Check AI settings
        if self.ai.preferred_provider not in self.get_available_providers():
            issues.append(f"Preferred AI provider {self.ai.preferred_provider.value} not available")
        
        if self.ai.max_tokens < 100:
            issues.append("Max tokens should be at least 100")
        
        if not (0.0 <= self.ai.temperature <= 2.0):
            issues.append("Temperature should be between 0.0 and 2.0")
        
        # Check output settings
        if self.output.save_reports:
            report_dir = self.output.report_directory
            if not os.path.exists(report_dir):
                try:
                    os.makedirs(report_dir)
                except Exception as e:
                    issues.append(f"Cannot create report directory {report_dir}: {e}")
        
        return issues
    
    def print_config_summary(self):
        """Print configuration summary"""
        print("LEGAL AI SIMULATION - CONFIGURATION")
        print("=" * 50)
        
        print(f"Simulation Settings:")
        print(f"  • Rounds: {self.simulation.min_rounds}-{self.simulation.max_rounds}")
        print(f"  • Early verdict: {self.simulation.enable_early_verdict}")
        print(f"  • Evidence analysis: {self.simulation.detailed_evidence_analysis}")
        
        print(f"\nAI Settings:")
        print(f"  • Preferred provider: {self.ai.preferred_provider.value}")
        print(f"  • Available providers: {[p.value for p in self.get_available_providers()]}")
        print(f"  • Max tokens: {self.ai.max_tokens}")
        print(f"  • Temperature: {self.ai.temperature}")
        
        print(f"\nOutput Settings:")
        print(f"  • Show thinking: {self.output.show_thinking_process}")
        print(f"  • Show evidence: {self.output.show_evidence_analysis}")
        print(f"  • Save reports: {self.output.save_reports}")
        if self.output.save_reports:
            print(f"  • Report directory: {self.output.report_directory}")
        
        # Validation
        issues = self.validate_config()
        if issues:
            print(f"\n⚠️  Configuration Issues:")
            for issue in issues:
                print(f"  • {issue}")
        else:
            print(f"\n✅ Configuration is valid")
        
        print("=" * 50)

# Global configuration instance
config = Config()

# Convenience functions
def get_ai_client(provider: Optional[AIProvider] = None):
    """Get AI client for specified or preferred provider"""
    if provider is None:
        provider = config.ai.preferred_provider
    
    client = config.get_api_client(provider)
    if client is None and config.ai.fallback_providers:
        # Try fallback providers
        for fallback in config.ai.fallback_providers:
            client = config.get_api_client(fallback)
            if client is not None:
                break
    
    return client

def setup_logging():
    """Setup logging based on configuration"""
    import logging
    
    log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper())
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('legal_simulation.log') if config.output.save_reports else logging.NullHandler()
        ]
    )

# Example usage and configuration templates
EXAMPLE_ENV_FILE = """
# Legal AI Simulation Configuration
# Copy this to .env and customize

# Simulation Settings
SIM_MIN_ROUNDS=6
SIM_MAX_ROUNDS=15
SIM_EARLY_VERDICT=true
SIM_EVIDENCE_ANALYSIS=true

# AI Provider Settings
AI_PROVIDER=gemini
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.7

# API Keys (get these from respective providers)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Output Settings
SHOW_THINKING=true
SHOW_EVIDENCE=true
COLORED_OUTPUT=true
SAVE_REPORTS=true
REPORT_DIR=reports

# Performance Settings
MAX_MEMORY_ITEMS=10
EVIDENCE_TIMEOUT=30
AI_TIMEOUT=60

# Logging
LOG_LEVEL=INFO
"""

if __name__ == "__main__":
    # Print current configuration
    config.print_config_summary()
    
    # Create example .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env.example', 'w') as f:
            f.write(EXAMPLE_ENV_FILE)
        print(f"\n📁 Created '.env.example' - copy to '.env' and customize")