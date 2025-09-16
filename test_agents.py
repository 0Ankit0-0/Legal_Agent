#!/usr/bin/env python3
"""
Quick test runner for the legal simulation system
"""

import os
import sys
from typing import Optional

def test_gemini_api() -> tuple[bool, Optional[dict]]:
    """Test Gemini API connection"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY environment variable not set")
            print("   Set it with: export GEMINI_API_KEY='your_api_key_here'")
            return False, None
            
        genai.configure(api_key=api_key)
        
        class GeminiClient:
            def __init__(self):
                self.model = genai.GenerativeModel('gemini-pro')
                
            def generate(self, prompt):
                try:
                    response = self.model.generate_content(prompt)
                    return {"thought": response.text, "evidence": None, "section": None}
                except Exception as e:
                    print(f"   ⚠️ Gemini API call failed: {e}")
                    raise
        
        # Test API call
        client = GeminiClient()
        test_prompt = "Briefly explain the concept of burden of proof in criminal law."
        result = client.generate(test_prompt)
        
        print("✅ Gemini API connection successful!")
        print(f"   Sample response: {result['thought'][:100]}...")
        
        return True, {"gemini": client}
        
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("   Install with: pip install google-generativeai")
        return False, None
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False, None

def run_basic_simulation():
    """Run basic simulation without AI"""
    try:
        from courtroom import run_courtroom_simulation
        
        print("\n" + "="*60)
        print("RUNNING BASIC SIMULATION (Rule-based AI)")
        print("="*60)
        
        result = run_courtroom_simulation()
        
        print(f"\n✅ Basic simulation completed successfully!")
        print(f"   Total arguments: {len(result['arguments'])}")
        print(f"   Final verdict: {result.get('final_verdict', {}).get('verdict', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic simulation failed: {e}")
        return False

def run_advanced_simulation(api_client=None):
    """Run advanced simulation"""
    try:
        from advanced_courtroom import AdvancedCourtroom, SimulationMode
        
        print("\n" + "="*60)
        print("RUNNING ADVANCED SIMULATION")
        print("="*60)
        
        courtroom = AdvancedCourtroom(SimulationMode.QUICK)  # Quick mode for testing
        result = courtroom.start_simulation("murder_case_1", api_client=api_client)
        
        print(f"\n✅ Advanced simulation completed successfully!")
        print(f"   Case: {result['case_information']['title']}")
        print(f"   Duration: {result['simulation_details']['duration_minutes']:.1f} minutes")
        print(f"   Verdict: {result['final_verdict']['verdict']}")
        
        # Save report
        courtroom._last_report = result
        courtroom.save_session_report("test_session_report.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'torch', 'spacy', 'numpy', 'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Main test runner"""
    print("LEGAL AI SIMULATION - TEST RUNNER")
    print("="*50)
    
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        return
    
    print("\n2. Testing Gemini API...")
    api_working, api_client = test_gemini_api()
    
    print("\n3. Running basic simulation...")
    basic_success = run_basic_simulation()
    
    if not basic_success:
        print("\n❌ Basic simulation failed. Please check your code.")
        return
    
    print("\n4. Running advanced simulation...")
    advanced_success = run_advanced_simulation(api_client if api_working else None)
    
    if not advanced_success:
        print("\n❌ Advanced simulation failed.")
        return
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    if api_working:
        print("✅ Gemini API is working - AI-enhanced responses available")
    else:
        print("⚠️  Gemini API not available - using rule-based fallbacks")
    
    print("✅ Basic simulation working")
    print("✅ Advanced simulation working") 
    print("✅ Report generation working")
    
    print(f"\n📁 Check 'test_session_report.json' for detailed results")
    
    print("\n🚀 Your legal simulation system is ready to use!")
    print("\nTo run a full simulation:")
    print("   python advanced_courtroom.py")
    print("\nTo run basic simulation:")
    print("   python courtroom.py")