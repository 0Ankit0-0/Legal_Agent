from typing import Dict, List, Optional, Tuple, Any
import json
import datetime
from dataclasses import dataclass
from enum import Enum

from prosecute import ProsecutorAgent
from defense import DefenseAgent
from judge import JudgeAgent
from evidence_analyzer import EvidenceAnalyzer

class CasePhase(Enum):
    OPENING = "opening_statements"
    EVIDENCE = "evidence_presentation"
    EXAMINATION = "witness_examination"
    ARGUMENTS = "closing_arguments"
    VERDICT = "verdict"

class SimulationMode(Enum):
    QUICK = "quick"      # 5-8 rounds
    STANDARD = "standard" # 10-15 rounds
    COMPREHENSIVE = "comprehensive" # 15-25 rounds

@dataclass
class CourtSession:
    case_id: str
    case_title: str
    judge_name: str
    prosecutor_name: str
    defense_name: str
    start_time: datetime.datetime
    phase: CasePhase
    round_number: int
    total_rounds: int

class AdvancedCourtroom:
    """Advanced courtroom simulation with multiple case types and enhanced AI"""
    
    def __init__(self, simulation_mode: SimulationMode = SimulationMode.STANDARD):
        self.simulation_mode = simulation_mode
        self.current_session: Optional[CourtSession] = None
        self.case_database = self._load_case_database()
        self.transcript = []
        self.evidence_analyzer = None
        
    def _load_case_database(self) -> Dict[str, Dict]:
        """Load predefined legal cases for simulation"""
        return {
            "murder_case_1": {
                "title": "The State vs. Julian Croft",
                "description": "Murder by poisoning during a social gathering",
                "type": "Murder Case",
                "summary": "On September 9th, Elias Vance died from poison at Julian Croft's dinner party. Evidence suggests premeditated murder over artistic theft dispute.",
                "complexity": "high",
                "evidence": [
                    {
                        "filename": "Exhibit_A_Torn_Sheet_Music.pdf",
                        "type": "physical",
                        "text": "Torn sheet music found at crime scene showing confrontation between victim and accused over artistic theft. Paper analysis confirms victim's handwriting.",
                        "relevance": "high"
                    },
                    {
                        "filename": "Exhibit_B_Poison_Gloves.pdf", 
                        "type": "forensic",
                        "text": "Latex gloves found in accused's possession with traces of cyanide compound. Chain of custody maintained by investigating officer.",
                        "relevance": "critical"
                    },
                    {
                        "filename": "Exhibit_C_Encrypted_Communications.pdf",
                        "type": "digital",
                        "text": "Encrypted email thread between accused and unknown party discussing 'permanent solution to plagiarism problem'. Digital forensics confirmed authenticity.",
                        "relevance": "high"
                    },
                    {
                        "filename": "Post_Mortem_Report.pdf",
                        "type": "medical",
                        "text": "Official post-mortem examination by certified pathologist confirms death by cyanide poisoning. Time of death: 11:30 PM on September 9th. No other contributing factors.",
                        "relevance": "critical"
                    },
                    {
                        "filename": "Witness_Statement_Host.pdf",
                        "type": "testimonial",
                        "text": "Party host witnessed heated argument between victim and accused at 10:45 PM regarding stolen musical compositions. Accused appeared agitated and left briefly.",
                        "relevance": "high"
                    }
                ],
                "laws": {
                    "ipc": {
                        "302": {
                            "title": "Murder",
                            "description": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine",
                            "keywords": ["murder", "kill", "death", "unlawful", "intention", "premeditation"]
                        },
                        "304": {
                            "title": "Culpable homicide not amounting to murder",
                            "description": "Punishment for culpable homicide not amounting to murder",
                            "keywords": ["homicide", "death", "intention", "knowledge", "without premeditation"]
                        },
                        "201": {
                            "title": "Causing disappearance of evidence",
                            "description": "Whoever causes disappearance of evidence or gives false information",
                            "keywords": ["evidence", "destruction", "concealment", "false information"]
                        }
                    }
                }
            },
            
            "theft_case_1": {
                "title": "The State vs. Rajesh Kumar",
                "description": "Theft of valuable jewelry from employer's residence",
                "type": "Theft Case", 
                "summary": "Rajesh Kumar, employed as house help, allegedly stole diamond jewelry worth ₹5 lakhs from employer Mrs. Sharma's bedroom safe.",
                "complexity": "medium",
                "evidence": [
                    {
                        "filename": "CCTV_Footage.mp4",
                        "type": "digital",
                        "text": "CCTV footage shows accused entering employer's bedroom at 2:30 PM when family was absent. Clear image of accused near the safe location.",
                        "relevance": "critical"
                    },
                    {
                        "filename": "Pawn_Shop_Receipt.pdf",
                        "type": "documentary", 
                        "text": "Receipt from pawn shop showing jewelry items matching description sold by person matching accused's identity on same day as theft.",
                        "relevance": "high"
                    },
                    {
                        "filename": "Employer_Statement.pdf",
                        "type": "testimonial",
                        "text": "Mrs. Sharma's statement confirming missing jewelry items, their estimated value, and accused's access to house keys and safe location knowledge.",
                        "relevance": "high"
                    }
                ],
                "laws": {
                    "ipc": {
                        "379": {
                            "title": "Theft",
                            "description": "Whoever intends to take dishonestly any movable property out of the possession of any person",
                            "keywords": ["theft", "dishonestly", "movable property", "possession", "intention"]
                        },
                        "381": {
                            "title": "Theft by clerk or servant",
                            "description": "Theft by clerk or servant of property in possession of master",
                            "keywords": ["servant", "clerk", "master", "employment", "trust"]
                        }
                    }
                }
            }
        }
    
    def start_simulation(self, case_id: str, api_client=None) -> Dict[str, Any]:
        """Start a new courtroom simulation"""
        if case_id not in self.case_database:
            raise ValueError(f"Case {case_id} not found in database")
        
        case_data = self.case_database[case_id]
        
        # Initialize evidence analyzer
        self.evidence_analyzer = EvidenceAnalyzer(case_data["laws"])
        
        # Create session
        self.current_session = CourtSession(
            case_id=case_id,
            case_title=case_data["title"],
            judge_name="Justice Verma",
            prosecutor_name="Advocate Ramesh Kumar",
            defense_name="Advocate Suresh Sharma", 
            start_time=datetime.datetime.now(),
            phase=CasePhase.OPENING,
            round_number=0,
            total_rounds=self._get_max_rounds()
        )
        
        # Initialize agents
        prosecutor = ProsecutorAgent(
            case_data=case_data,
            evidence=case_data["evidence"],
            laws=case_data["laws"],
            name=self.current_session.prosecutor_name,
            role="prosecutor"
        )
        
        defense = DefenseAgent(
            case_data=case_data,
            evidence=case_data["evidence"], 
            laws=case_data["laws"],
            name=self.current_session.defense_name,
            role="defendant"
        )
        
        judge = JudgeAgent(
            case_data=case_data,
            evidence=case_data["evidence"],
            laws=case_data["laws"],
            name=self.current_session.judge_name,
            role="judge"
        )
        
        # Set AI models if provided
        if api_client:
            prosecutor.set_ai_models(api_client=api_client)
            defense.set_ai_models(api_client=api_client)
            judge.set_ai_models(api_client=api_client)
        
        # Run simulation
        return self._run_full_simulation(prosecutor, defense, judge, case_data)
    
    def _get_max_rounds(self) -> int:
        """Get maximum rounds based on simulation mode"""
        if self.simulation_mode == SimulationMode.QUICK:
            return 8
        elif self.simulation_mode == SimulationMode.STANDARD:
            return 15
        else:  # COMPREHENSIVE
            return 25
    
    def _run_full_simulation(self, prosecutor, defense, judge, case_data) -> Dict[str, Any]:
        """Run the complete simulation with all phases"""
        
        print(f"\n{'='*80}")
        print(f"COURTROOM SIMULATION: {self.current_session.case_title}")
        print(f"{'='*80}")
        print(f"Judge: {self.current_session.judge_name}")
        print(f"Prosecutor: {self.current_session.prosecutor_name}")
        print(f"Defense: {self.current_session.defense_name}")
        print(f"Case Type: {case_data['type']}")
        print(f"Simulation Mode: {self.simulation_mode.value.upper()}")
        print(f"{'='*80}\n")
        
        # Analyze evidence before starting
        evidence_summary = self.evidence_analyzer.generate_evidence_summary(
            case_data["evidence"], case_data
        )
        
        print(f"EVIDENCE SUMMARY:")
        print(f"- Total Evidence: {evidence_summary['total_evidence_pieces']}")
        print(f"- Strong Evidence: {evidence_summary['strong_evidence_count']}")
        print(f"- Overall Case Strength: {evidence_summary['overall_case_strength']:.2f}/1.0")
        print(f"- Evidence Gaps: {', '.join(evidence_summary['evidence_gaps']) if evidence_summary['evidence_gaps'] else 'None identified'}")
        print(f"\n{'='*80}\n")
        
        turns = []
        last_statement = None
        
        # Phase 1: Opening Statements
        self._run_opening_phase(judge, prosecutor, defense, turns)
        
        # Phase 2: Evidence Presentation and Arguments
        self._run_arguments_phase(prosecutor, defense, judge, turns, case_data)
        
        # Phase 3: Final Verdict
        final_verdict = self._run_verdict_phase(judge, turns)
        
        # Generate final report
        return self._generate_final_report(turns, final_verdict, evidence_summary, case_data)
    
    def _run_opening_phase(self, judge, prosecutor, defense, turns):
        """Run opening statements phase"""
        print("PHASE 1: OPENING STATEMENTS")
        print("-" * 50)
        
        # Judge opens court
        opening = (
            f"The Court is in session. We are here for the trial of {self.current_session.case_title}. "
            f"The accused stands charged under the relevant provisions of the Indian Penal Code. "
            f"The prosecution may present their opening statement."
        )
        
        judge_statement = {
            'role': 'judge',
            'statement': opening,
            'thought': 'Opening court session and establishing formal proceedings',
            'evidence': None,
            'phase': 'opening'
        }
        turns.append(judge_statement)
        
        print(f"\n**{self.current_session.judge_name} (Presiding Judge)**")
        print(f"{opening}\n")
        
        self.current_session.phase = CasePhase.OPENING
        self.current_session.round_number = 1
    
    def _run_arguments_phase(self, prosecutor, defense, judge, turns, case_data):
        """Run the main arguments phase"""
        print("\nPHASE 2: ARGUMENTS AND EVIDENCE PRESENTATION")
        print("-" * 50)
        
        self.current_session.phase = CasePhase.ARGUMENTS
        last_statement = None
        
        while self.current_session.round_number <= self.current_session.total_rounds:
            print(f"\n--- Round {self.current_session.round_number} ---")
            
            # Prosecutor's turn
            print(f"\n**{self.current_session.prosecutor_name} (Public Prosecutor)**")
            prosecution_thought = prosecutor.think(last_statement)
            prosecution_statement = prosecutor.speak(prosecution_thought)
            prosecutor.remember(prosecution_statement['statement'], prosecution_thought[0])
            prosecution_statement['round'] = self.current_session.round_number
            turns.append(prosecution_statement)
            
            print(f"\n{prosecution_statement['statement']}")
            print(f"\n***Thinking Process:*** *{prosecution_thought[0][:200]}...*")
            
            # Analyze prosecution's evidence if mentioned
            if prosecution_statement.get('evidence'):
                self._analyze_presented_evidence(prosecution_statement['evidence'], case_data)
            
            judge.record_argument('prosecutor', prosecution_statement['statement'], prosecution_thought[0])
            
            # Defense's turn
            print(f"\n**{self.current_session.defense_name} (Defense Advocate)**")
            defense_thought = defense.think(prosecution_statement['statement'])
            defense_statement = defense.speak(defense_thought)
            defense.remember(defense_statement['statement'], defense_thought[0])
            defense_statement['round'] = self.current_session.round_number
            turns.append(defense_statement)
            
            print(f"\n{defense_statement['statement']}")
            print(f"\n***Thinking Process:*** *{defense_thought[0][:200]}...*")
            
            judge.record_argument('defense', defense_statement['statement'], defense_thought[0])
            
            # Judge's observations
            print(f"\n**{self.current_session.judge_name} (Presiding Judge)**")
            judge_thought = judge.think(
                f"Prosecution: {prosecution_statement['statement']} Defense: {defense_statement['statement']}"
            )
            judge_statement = judge.speak(judge_thought)
            judge.remember(judge_statement['statement'], judge_thought[0])
            judge_statement['round'] = self.current_session.round_number
            turns.append(judge_statement)
            
            print(f"\n{judge_statement['statement']}")
            print(f"\n***Judicial Reasoning:*** *{judge_thought[0][:200]}...*")
            
            last_statement = judge_statement['statement']
            self.current_session.round_number += 1
            
            # Check for early verdict indicators
            if self._should_conclude_early(judge_statement, self.current_session.round_number):
                print(f"\nCourt indicates readiness for final judgment...")
                break
        
    def _run_verdict_phase(self, judge, turns):
        """Run final verdict phase"""
        print(f"\n{'='*80}")
        print("PHASE 3: FINAL JUDGMENT")
        print(f"{'='*80}")
        
        self.current_session.phase = CasePhase.VERDICT
        
        print(f"\n**{self.current_session.judge_name} (Presiding Judge)**")
        print("The Court will now pronounce its judgment...")
        
        final_verdict = judge.render_verdict(turns)
        
        verdict_statement = (
            f"After careful consideration of all evidence presented, the arguments of learned counsel, "
            f"and the applicable provisions of law, this Court finds the accused {final_verdict['verdict']}. "
            f"\n\nREASONING: {final_verdict['reasoning']}"
        )
        
        if final_verdict['verdict'].lower() == 'guilty' and final_verdict.get('sentence'):
            verdict_statement += f"\n\nSENTENCE: {final_verdict['sentence']}"
        
        verdict_statement += f"\n\nThis judgment is pronounced in open court on {datetime.datetime.now().strftime('%B %d, %Y')}."
        
        print(f"\n{verdict_statement}")
        
        turns.append({
            'role': 'judge',
            'statement': verdict_statement,
            'thought': 'Final verdict and reasoning',
            'evidence': None,
            'verdict_details': final_verdict,
            'phase': 'verdict'
        })
        
        return final_verdict
    
    def _analyze_presented_evidence(self, evidence_filename, case_data):
        """Analyze evidence when presented in court"""
        for evidence in case_data["evidence"]:
            if evidence["filename"] == evidence_filename:
                analysis = self.evidence_analyzer.analyze_evidence(evidence, case_data)
                print(f"\n    [EVIDENCE ANALYSIS: {evidence_filename}]")
                print(f"    Strength: {analysis.strength_score:.2f} | Relevance: {analysis.relevance_score:.2f}")
                if analysis.potential_challenges:
                    print(f"    Potential Challenges: {', '.join(analysis.potential_challenges[:2])}")
                break
    
    def _should_conclude_early(self, judge_statement, round_number):
        """Determine if court should conclude early"""
        statement = judge_statement['statement'].lower()
        verdict_indicators = [
            'ready to pronounce', 'sufficient evidence', 'conclude the matter',
            'final judgment', 'render verdict', 'case is clear'
        ]
        
        # Early conclusion after minimum rounds
        if round_number >= 6:
            return any(indicator in statement for indicator in verdict_indicators)
        
        return False
    
    def _generate_final_report(self, turns, final_verdict, evidence_summary, case_data) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        
        # Count statements by each party
        prosecutor_statements = len([t for t in turns if t['role'] == 'prosecutor'])
        defense_statements = len([t for t in turns if t['role'] == 'defendant'])
        judge_statements = len([t for t in turns if t['role'] == 'judge'])
        
        # Calculate session duration
        session_duration = datetime.datetime.now() - self.current_session.start_time
        
        report = {
            'case_information': {
                'case_id': self.current_session.case_id,
                'title': self.current_session.case_title,
                'type': case_data['type'],
                'complexity': case_data.get('complexity', 'unknown'),
                'description': case_data['description']
            },
            'simulation_details': {
                'mode': self.simulation_mode.value,
                'start_time': self.current_session.start_time.isoformat(),
                'duration_minutes': round(session_duration.total_seconds() / 60, 2),
                'total_rounds': self.current_session.round_number - 1,
                'total_statements': len(turns)
            },
            'participant_statistics': {
                'judge': {
                    'name': self.current_session.judge_name,
                    'statements': judge_statements
                },
                'prosecutor': {
                    'name': self.current_session.prosecutor_name, 
                    'statements': prosecutor_statements
                },
                'defense': {
                    'name': self.current_session.defense_name,
                    'statements': defense_statements
                }
            },
            'evidence_analysis': evidence_summary,
            'final_verdict': final_verdict,
            'transcript': turns,
            'legal_sections_cited': self._extract_legal_citations(turns),
            'evidence_presented': self._extract_evidence_citations(turns),
            'case_outcome': {
                'verdict': final_verdict['verdict'],
                'reasoning_summary': final_verdict['reasoning'][:200] + "...",
                'sentence': final_verdict.get('sentence'),
                'applied_sections': final_verdict.get('applied_sections', [])
            }
        }
        
        # Print final summary
        print(f"\n{'='*80}")
        print("SIMULATION COMPLETED - FINAL SUMMARY")
        print(f"{'='*80}")
        print(f"Case: {report['case_information']['title']}")
        print(f"Duration: {report['simulation_details']['duration_minutes']:.1f} minutes")
        print(f"Total Rounds: {report['simulation_details']['total_rounds']}")
        print(f"Final Verdict: {report['final_verdict']['verdict']}")
        print(f"Evidence Strength: {evidence_summary['overall_case_strength']:.2f}/1.0")
        print(f"Legal Sections Cited: {', '.join(report['legal_sections_cited'])}")
        print(f"{'='*80}")
        
        return report
    
    def _extract_legal_citations(self, turns) -> List[str]:
        """Extract all IPC sections cited during the trial"""
        sections = set()
        for turn in turns:
            if turn.get('section'):
                sections.add(turn['section'])
        return sorted(list(sections))
    
    def _extract_evidence_citations(self, turns) -> List[str]:
        """Extract all evidence files mentioned during the trial"""
        evidence = set()
        for turn in turns:
            if turn.get('evidence'):
                evidence.add(turn['evidence'])
        return sorted(list(evidence))
    
    def save_session_report(self, filename: Optional[str] = None):
        """Save the session report to a JSON file"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"courtroom_session_{timestamp}.json"
        
        if hasattr(self, '_last_report'):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self._last_report, f, indent=2, ensure_ascii=False)
            print(f"Session report saved to: {filename}")
        else:
            print("No session report available to save")

# Example usage and testing
if __name__ == "__main__":
    # Quick test
    courtroom = AdvancedCourtroom(SimulationMode.STANDARD)
    
    print("Available cases:")
    for case_id, case_info in courtroom.case_database.items():
        print(f"- {case_id}: {case_info['title']} ({case_info['type']})")
    
    # Run simulation
    case_to_run = "murder_case_1"
    print(f"\nRunning simulation for: {case_to_run}")
    
    # Test without API first
    result = courtroom.start_simulation(case_to_run)
    courtroom._last_report = result
    
    # Save report
    courtroom.save_session_report()