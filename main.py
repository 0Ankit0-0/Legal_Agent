#!/usr/bin/env python3
"""
Legal AI Simulation System - Main Runner
Complete courtroom simulation with AI integration
"""

import argparse
import sys
import os
from datetime import datetime
from typing import Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config, setup_logging, get_ai_client, AIProvider
from courtroom import AdvancedCourtroom, SimulationMode

def create_colored_output(text: str, color: str = "white") -> str:
    """Add color to terminal output if enabled"""
    if not config.output.colored_output:
        return text
    
    colors = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "end": "\033[0m"
    }
    
    return f"{colors.get(color, colors['white'])}{text}{colors['end']}"

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                  LEGAL AI SIMULATION SYSTEM                  ║
    ║                   Advanced Courtroom AI                      ║
    ║              Indian Legal System Simulation                  ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(create_colored_output(banner, "cyan"))

def list_available_cases(courtroom: AdvancedCourtroom):
    """List all available cases"""
    print(create_colored_output("\nAVAILABLE CASES:", "bold"))
    print("-" * 50)
    
    for case_id, case_info in courtroom.case_database.items():
        case_type = case_info.get('type', 'Unknown Type')
        complexity = case_info.get('complexity', 'unknown').upper()
        evidence_count = len(case_info.get('evidence', []))
        
        print(f"{create_colored_output('•', 'green')} {create_colored_output(case_id, 'yellow')}")
        print(f"  Title: {case_info['title']}")
        print(f"  Type: {create_colored_output(case_type, 'blue')}")
        print(f"  Complexity: {create_colored_output(complexity, 'purple')}")
        print(f"  Evidence Items: {create_colored_output(str(evidence_count), 'cyan')}")
        print(f"  Description: {case_info['description'][:100]}...")
        print()

def check_system_status():
    """Check system status and dependencies"""
    print(create_colored_output("SYSTEM STATUS CHECK", "bold"))
    print("-" * 30)
    
    # Check configuration
    issues = config.validate_config()
    if issues:
        print(create_colored_output("⚠️  Configuration Issues:", "yellow"))
        for issue in issues:
            print(f"   • {issue}")
    else:
        print(create_colored_output("✅ Configuration: OK", "green"))
    
    # Check AI providers
    available_providers = config.get_available_providers()
    print(f"{create_colored_output('🤖 AI Providers:', 'blue')}")
    
    for provider in [AIProvider.GEMINI, AIProvider.OPENAI, AIProvider.RULE_BASED]:
        if provider in available_providers:
            print(f"   ✅ {provider.value}")
        else:
            print(f"   ❌ {provider.value} (not configured)")
    
    # Check dependencies
    required_packages = ['torch', 'numpy', 'spacy']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)
    
    if missing:
        print(create_colored_output(f"\n⚠️  Install missing packages: pip install {' '.join(missing)}", "yellow"))
    
    return len(issues) == 0 and len(missing) == 0

def run_interactive_mode():
    """Run interactive case selection and simulation"""
    courtroom = AdvancedCourtroom()
    
    while True:
        print("\n" + "="*60)
        print(create_colored_output("INTERACTIVE MODE", "bold"))
        print("="*60)
        
        print(f"\n{create_colored_output('Available Options:', 'blue')}")
        print("1. List available cases")
        print("2. Run simulation")
        print("3. Check system status")
        print("4. View configuration")
        print("5. Exit")
        
        choice = input(f"\n{create_colored_output('Select option (1-5):', 'yellow')} ").strip()
        
        if choice == "1":
            list_available_cases(courtroom)
            
        elif choice == "2":
            # Case selection
            list_available_cases(courtroom)
            case_id = input(f"\n{create_colored_output('Enter case ID:', 'yellow')} ").strip()
            
            if case_id not in courtroom.case_database:
                print(create_colored_output(f"❌ Case '{case_id}' not found", "red"))
                continue
            
            # Simulation mode selection
            print(f"\n{create_colored_output('Simulation Modes:', 'blue')}")
            print("1. Quick (5-8 rounds)")
            print("2. Standard (10-15 rounds)")  
            print("3. Comprehensive (15-25 rounds)")
            
            mode_choice = input(f"\n{create_colored_output('Select mode (1-3):', 'yellow')} ").strip()
            
            mode_map = {
                "1": SimulationMode.QUICK,
                "2": SimulationMode.STANDARD,
                "3": SimulationMode.COMPREHENSIVE
            }
            
            if mode_choice not in mode_map:
                print(create_colored_output("❌ Invalid mode selection", "red"))
                continue
            
            courtroom.simulation_mode = mode_map[mode_choice]
            
            # Get AI client
            ai_client = get_ai_client()
            if ai_client:
                provider_name = config.ai.preferred_provider.value
                print(create_colored_output(f"🤖 Using AI provider: {provider_name}", "green"))
            else:
                print(create_colored_output("🤖 Using rule-based AI (no API available)", "yellow"))
            
            # Run simulation
            try:
                print(create_colored_output(f"\n🚀 Starting simulation for: {case_id}", "green"))
                api_client_dict = {"gemini": ai_client} if ai_client else None
                
                result = courtroom.start_simulation(case_id, api_client=api_client_dict)
                
                # Save report
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_filename = f"{config.output.report_directory}/session_{case_id}_{timestamp}.json"
                
                if config.output.save_reports:
                    courtroom._last_report = result
                    courtroom.save_session_report(report_filename)
                    print(create_colored_output(f"📁 Report saved: {report_filename}", "cyan"))
                
            except Exception as e:
                print(create_colored_output(f"❌ Simulation failed: {e}", "red"))
                import traceback
                traceback.print_exc()
        
        elif choice == "3":
            check_system_status()
            
        elif choice == "4":
            config.print_config_summary()
            
        elif choice == "5":
            print(create_colored_output("👋 Goodbye!", "green"))
            break
            
        else:
            print(create_colored_output("❌ Invalid option", "red"))
        
        input(f"\n{create_colored_output('Press Enter to continue...', 'cyan')}")

def run_direct_simulation(case_id: str, mode: SimulationMode, ai_provider: Optional[str] = None):
    """Run simulation directly with specified parameters"""
    courtroom = AdvancedCourtroom(mode)
    
    if case_id not in courtroom.case_database:
        print(create_colored_output(f"❌ Case '{case_id}' not found", "red"))
        print("\nAvailable cases:")
        for cid in courtroom.case_database.keys():
            print(f"  • {cid}")
        return False
    
    # Get AI client
    if ai_provider:
        try:
            provider_enum = AIProvider(ai_provider.lower())
            ai_client = config.get_api_client(provider_enum)
        except ValueError:
            print(create_colored_output(f"❌ Invalid AI provider: {ai_provider}", "red"))
            return False
    else:
        ai_client = get_ai_client()
    
    if ai_client:
        provider_name = ai_provider or config.ai.preferred_provider.value
        print(create_colored_output(f"🤖 Using AI provider: {provider_name}", "green"))
    else:
        print(create_colored_output("🤖 Using rule-based AI", "yellow"))
    
    try:
        print(create_colored_output(f"🚀 Starting {mode.value} simulation for: {case_id}", "green"))
        api_client_dict = {"gemini": ai_client} if ai_client else None
        
        result = courtroom.start_simulation(case_id, api_client=api_client_dict)
        
        # Save report
        if config.output.save_reports:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"{config.output.report_directory}/session_{case_id}_{timestamp}.json"
            courtroom._last_report = result
            courtroom.save_session_report(report_filename)
            print(create_colored_output(f"📁 Report saved: {report_filename}", "cyan"))
        
        return True
        
    except Exception as e:
        print(create_colored_output(f"❌ Simulation failed: {e}", "red"))
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Legal AI Simulation System - Advanced Courtroom AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Interactive mode
  python main.py --case murder_case_1               # Run specific case
  python main.py --case theft_case_1 --mode quick  # Quick simulation
  python main.py --list-cases                      # List available cases
  python main.py --status                          # Check system status
        """
    )
    
    parser.add_argument("--case", "-c", help="Case ID to simulate")
    parser.add_argument("--mode", "-m", choices=["quick", "standard", "comprehensive"], 
                       default="standard", help="Simulation mode")
    parser.add_argument("--ai-provider", "-ai", choices=["gemini", "openai", "rule_based"],
                       help="AI provider to use")
    parser.add_argument("--list-cases", "-l", action="store_true", 
                       help="List available cases")
    parser.add_argument("--status", "-s", action="store_true",
                       help="Check system status")
    parser.add_argument("--config", "-cfg", action="store_true",
                       help="Show configuration")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("--no-color", action="store_true",
                       help="Disable colored output")
    
    args = parser.parse_args()
    
    # Setup
    if args.no_color:
        config.output.colored_output = False
    
    setup_logging()
    print_banner()
    
    # Handle specific commands
    if args.status:
        check_system_status()
        return
    
    if args.config:
        config.print_config_summary()
        return
    
    if args.list_cases:
        courtroom = AdvancedCourtroom()
        list_available_cases(courtroom)
        return
    
    # Run simulation modes
    if args.case:
        # Direct simulation
        mode_map = {
            "quick": SimulationMode.QUICK,
            "standard": SimulationMode.STANDARD,
            "comprehensive": SimulationMode.COMPREHENSIVE
        }
        
        mode = mode_map[args.mode]
        success = run_direct_simulation(args.case, mode, args.ai_provider)
        sys.exit(0 if success else 1)
    
    elif args.interactive or len(sys.argv) == 1:
        # Interactive mode (default if no arguments)
        run_interactive_mode()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(create_colored_output("\n\n👋 Simulation interrupted by user", "yellow"))
        sys.exit(0)
    except Exception as e:
        print(create_colored_output(f"\n❌ Unexpected error: {e}", "red"))
        import traceback
        traceback.print_exc()
        sys.exit(1)