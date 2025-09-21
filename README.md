# Legal AI Courtroom Simulation System

An advanced AI-powered courtroom simulation system featuring autonomous legal agents (Prosecutor, Defense Attorney, and Judge) that can conduct realistic legal proceedings using Indian law and evidence analysis.

## 🏛️ Overview

This system creates an immersive legal environment where AI agents represent different roles in a courtroom:
- **Prosecutor Agent**: Builds cases and presents charges based on evidence
- **Defense Agent**: Develops defense strategies and challenges prosecution
- **Judge Agent**: Makes impartial decisions and renders verdicts
- **Evidence Analyzer**: Analyzes and scores evidence relevance

The system supports multiple AI backends including local models, pretrained transformers, and API services (OpenAI, Google Gemini).

## 📁 Project Structure

```
├── __pycache__/                    # Python cache files
├── api_clients.py                  # API client configurations (OpenAI, Gemini)
├── base_agent.py                   # Base class for all legal agents
├── config.py                       # System configuration
├── courtroom.py                    # Main courtroom simulation engine
├── defense.py                      # Defense attorney agent
├── judge.py                        # Judge agent with verdict system
├── prosecute.py                    # Prosecutor agent
├── evidence_analyzer.py            # Evidence analysis and scoring
├── local_model.py                  # Local transformer models and training
├── main.py                         # Main execution script
├── training_pipeline.py            # Model training utilities
├── test_agents.py                  # Test suite for agents
├── requirements.txt                # Python dependencies
└── dataset/                        # Legal datasets
    ├── ipc/                        # Indian Penal Code data
    ├── cpc/                        # Civil Procedure Code data
    ├── crcp/                       # Criminal Procedure Code data
    ├── cons/                       # Constitution data
    ├── constitution2/              # Additional constitutional data
    └── MVA/                        # Motor Vehicle Act data
```

## 🚀 Features

### Core Capabilities
- **Multi-Agent Simulation**: Autonomous legal agents with distinct roles
- **Evidence Analysis**: Automated evidence relevance scoring and analysis
- **Legal Reasoning**: AI-powered legal argument generation
- **Verdict System**: Comprehensive judgment with reasoning
- **Multiple Case Types**: Support for murder, theft, and other criminal cases
- **Indian Legal Framework**: Built on IPC, CrPC, CPC, and Constitution

### AI Integration
- **Local Models**: Custom transformer models for legal reasoning
- **API Support**: OpenAI GPT and Google Gemini integration
- **Fallback Mechanism**: Graceful degradation from AI to rule-based systems
- **Legal NLP**: Specialized natural language processing for legal texts

### Simulation Modes
- **Quick Mode**: 5-8 rounds for rapid testing
- **Standard Mode**: 10-15 rounds for balanced simulation
- **Comprehensive Mode**: 15-25 rounds for detailed proceedings

## 📋 Prerequisites

- Python 3.8+
- PyTorch 2.0+
- spaCy with English model
- API keys for external services (optional)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd legal-ai-courtroom
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy English model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Configure API keys** (optional):
   Edit `api_clients.py` to add your API keys:
   ```python
   api_keys = {
       'gemini': 'YOUR_GEMINI_API_KEY',
       'openai': 'YOUR_OPENAI_API_KEY'
   }
   ```

## 🎮 Quick Start

### Basic Usage

```python
from courtroom import AdvancedCourtroom, SimulationMode
from api_clients import create_api_clients, api_keys

# Initialize courtroom
courtroom = AdvancedCourtroom(SimulationMode.STANDARD)

# Optional: Set up API clients
clients = create_api_clients(api_keys)

# Run simulation
result = courtroom.start_simulation("murder_case_1", api_client=clients)

# Save report
courtroom.save_session_report("simulation_report.json")
```

### Command Line Usage

```bash
# Run default simulation
python main.py

# Run with specific case
python courtroom.py

# Run tests
python test_agents.py
```

## 📚 Available Cases

The system includes predefined legal cases:

### Murder Case (`murder_case_1`)
- **Title**: The State vs. Julian Croft
- **Type**: Murder by poisoning
- **Evidence**: Forensic evidence, witness statements, digital communications
- **Complexity**: High

### Theft Case (`theft_case_1`)
- **Title**: The State vs. Rajesh Kumar
- **Type**: Theft of valuable jewelry
- **Evidence**: CCTV footage, pawn shop receipts, employer statements
- **Complexity**: Medium

## 🤖 Agent Behavior

### Prosecutor Agent
- Builds prosecution case based on evidence
- Identifies applicable criminal charges
- Establishes mens rea and actus reus
- Responds to defense arguments

### Defense Agent
- Develops defense strategies
- Challenges prosecution evidence
- Raises procedural and constitutional defenses
- Emphasizes burden of proof

### Judge Agent
- Maintains impartiality
- Evaluates evidence strength
- Applies legal principles
- Renders final verdict with reasoning

## 🔧 Configuration

### Simulation Parameters
```python
# In courtroom.py
class SimulationMode(Enum):
    QUICK = "quick"          # 5-8 rounds
    STANDARD = "standard"    # 10-15 rounds
    COMPREHENSIVE = "comprehensive"  # 15-25 rounds
```

### AI Model Configuration
```python
# Set AI models for agents
prosecutor.set_ai_models(
    local_model=local_model,
    pretrained_model=pretrained_model,
    api_client=api_client
)
```

## 📊 Output and Reports

The simulation generates comprehensive reports including:
- **Case Information**: Details about the simulated case
- **Participant Statistics**: Statement counts for each agent
- **Evidence Analysis**: Strength and relevance scores
- **Final Verdict**: Judgment with detailed reasoning
- **Full Transcript**: Complete conversation log
- **Legal Citations**: IPC sections and evidence referenced

### Sample Output Structure
```json
{
  "case_information": {
    "case_id": "murder_case_1",
    "title": "The State vs. Julian Croft",
    "type": "Murder Case",
    "complexity": "high"
  },
  "simulation_details": {
    "mode": "standard",
    "duration_minutes": 5.2,
    "total_rounds": 12,
    "total_statements": 37
  },
  "final_verdict": {
    "verdict": "Guilty",
    "reasoning": "The Court finds that...",
    "sentence": "Imprisonment for life..."
  }
}
```

## 🧪 Testing

Run the test suite to verify system functionality:

```bash
# Run all tests
python test_agents.py

# Run specific agent tests
python -m pytest test_agents.py::test_prosecutor_agent
```

## 📖 Legal Dataset

The system includes comprehensive legal datasets:
- **IPC**: Indian Penal Code sections and definitions
- **CrPC**: Criminal Procedure Code
- **CPC**: Civil Procedure Code
- **Constitution**: Constitutional articles and rights
- **MVA**: Motor Vehicle Act provisions

Each dataset includes:
- Structured JSON data
- Plain text versions
- Q&A pairs for training
- Embeddings for semantic search
- Training data in JSONL format

## 🔮 Advanced Features

### Evidence Analysis
```python
from evidence_analyzer import EvidenceAnalyzer

analyzer = EvidenceAnalyzer(laws_data)
analysis = analyzer.analyze_evidence(evidence, case_data)
print(f"Strength: {analysis.strength_score}")
print(f"Relevance: {analysis.relevance_score}")
```

### Custom Legal Models
```python
from local_model import LegalReasoningTransformer

model = LegalReasoningTransformer(
    vocab_size=50000,
    hidden_size=512,
    num_layers=6
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📜 Legal Disclaimer

This system is for educational and research purposes only. It is not intended to provide actual legal advice or replace professional legal consultation. The AI agents' decisions should not be considered authoritative legal interpretations.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛠️ Troubleshooting

### Common Issues

1. **spaCy model not found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **API key errors**:
   - Verify API keys in `api_clients.py`
   - Check API rate limits and quotas

3. **Memory issues with large models**:
   - Reduce `hidden_size` in model configuration
   - Use smaller simulation modes

4. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test cases for usage examples
3. Create an issue on the repository

## 🔄 Version History

- **v1.0**: Initial release with basic agent system
- **v1.1**: Added evidence analysis and local models
- **v1.2**: Enhanced AI integration and API support
- **v1.3**: Comprehensive legal dataset integration

---

*Built with ⚖️ for legal AI research and education*
