#!/usr/bin/env python3
"""
Enhanced Master Test Runner for Unified Attribution Framework
Executes all domain examples with improved reporting and error handling
"""

import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class TestResult:
    """Structured test result data"""
    name: str
    success: bool
    output: str
    error: str
    duration: float
    timestamp: str


class EnhancedTestRunner:
    """Enhanced test runner with comprehensive reporting"""
    
    def __init__(self, examples_dir: str = "examples"):
        self.examples_dir = Path(examples_dir)
        self.results: List[TestResult] = []
        self.start_time = None
        
    def run_example(self, script_path: Path, timeout: int = 120) -> TestResult:
        """Run a single example script and capture structured results"""
        print(f"\n{'='*70}")
        print(f"🔬 Running: {script_path.name}")
        print(f"{'='*70}")
        
        start = time.time()
        timestamp = datetime.now().isoformat()
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            duration = time.time() - start
            success = result.returncode == 0
            
            # Print immediate feedback
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{status} in {duration:.2f}s")
            
            if not success and result.stderr:
                print(f"Error preview: {result.stderr[:200]}")
            
            return TestResult(
                name=script_path.stem,
                success=success,
                output=result.stdout,
                error=result.stderr,
                duration=duration,
                timestamp=timestamp
            )
            
        except subprocess.TimeoutExpired:
            duration = timeout
            print(f"⏱️  TIMEOUT after {timeout}s")
            return TestResult(
                name=script_path.stem,
                success=False,
                output='',
                error=f'TIMEOUT after {timeout}s',
                duration=duration,
                timestamp=timestamp
            )
            
        except Exception as e:
            duration = time.time() - start
            print(f"💥 EXCEPTION: {str(e)}")
            return TestResult(
                name=script_path.stem,
                success=False,
                output='',
                error=f'Exception: {str(e)}',
                duration=duration,
                timestamp=timestamp
            )
    
    def run_all_examples(self, examples: List[str]) -> Dict:
        """Run all examples and collect results"""
        self.start_time = time.time()
        
        print("="*70)
        print("🎯 UNIFIED ATTRIBUTION FRAMEWORK - ENHANCED TEST SUITE")
        print("="*70)
        print(f"Testing {len(examples)} domain examples...")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Python: {sys.version.split()[0]}")
        print("="*70)
        
        for example_file in examples:
            script_path = self.examples_dir / example_file
            
            if not script_path.exists():
                print(f"\n⚠️  WARNING: {example_file} not found, skipping...")
                self.results.append(TestResult(
                    name=Path(example_file).stem,
                    success=False,
                    output='',
                    error='File not found',
                    duration=0.0,
                    timestamp=datetime.now().isoformat()
                ))
                continue
            
            result = self.run_example(script_path)
            self.results.append(result)
        
        return self.generate_summary()
    
    def generate_summary(self) -> Dict:
        """Generate comprehensive summary statistics"""
        total_duration = time.time() - self.start_time
        
        successes = sum(1 for r in self.results if r.success)
        failures = len(self.results) - successes
        
        # Calculate statistics
        durations = [r.duration for r in self.results if r.success]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'total_tests': len(self.results),
            'successes': successes,
            'failures': failures,
            'success_rate': (successes / len(self.results) * 100) if self.results else 0,
            'total_duration': total_duration,
            'avg_duration': avg_duration,
            'results': self.results
        }
    
    def print_summary(self, summary: Dict):
        """Print formatted summary report"""
        print("\n" + "="*70)
        print("📊 FINAL SUMMARY REPORT")
        print("="*70)
        
        print(f"\n📈 Overall Statistics:")
        print(f"   Total Examples: {summary['total_tests']}")
        print(f"   ✅ Successes: {summary['successes']}")
        print(f"   ❌ Failures: {summary['failures']}")
        print(f"   📊 Success Rate: {summary['success_rate']:.1f}%")
        print(f"   ⏱️  Total Time: {summary['total_duration']:.2f}s")
        print(f"   ⚡ Average Time: {summary['avg_duration']:.2f}s per test")
        
        # Detailed results table
        print(f"\n📋 Detailed Results:")
        print(f"{'Domain':<35} {'Status':<12} {'Time (s)':<12}")
        print("-"*70)
        
        for result in self.results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"{result.name:<35} {status:<12} {result.duration:<12.2f}")
        
        # Failed tests details
        failed_tests = [r for r in self.results if not r.success]
        if failed_tests:
            print(f"\n❌ Failed Tests Details:")
            print("-"*70)
            for result in failed_tests:
                print(f"\n📛 {result.name}:")
                error_lines = result.error.split('\n')[:5]  # First 5 lines
                for line in error_lines:
                    if line.strip():
                        print(f"   {line}")
                if len(result.error.split('\n')) > 5:
                    print(f"   ... (truncated)")
        
        # Final status
        print("\n" + "="*70)
        if summary['failures'] == 0:
            print("🎉 ALL TESTS PASSED! Framework is ready for deployment!")
        else:
            print(f"⚠️  {summary['failures']} test(s) failed. See details above.")
        print("="*70)
    
    def export_json_report(self, filepath: str = "test_report.json"):
        """Export results to JSON for programmatic access"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'successes': sum(1 for r in self.results if r.success),
            'failures': sum(1 for r in self.results if not r.success),
            'results': [
                {
                    'name': r.name,
                    'success': r.success,
                    'duration': r.duration,
                    'timestamp': r.timestamp,
                    'error': r.error if not r.success else None
                }
                for r in self.results
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 JSON report exported to: {filepath}")


def main():
    # Define all domain examples
    examples = [
        "mathematics.py",
        "marketing_attribution.py",
        "physics_quantum.py",
        "physics_classical.py",
        "economics_macro.py",
        "art_aesthetics.py",
        "psychology_cognition.py",
        "biology_genetics.py",
        "chemistry_reactions.py",
        "medicine_clinical.py",
        "linguistics_meaning.py"
    ]
    
    # Create runner and execute
    runner = EnhancedTestRunner(examples_dir="examples")
    summary = runner.run_all_examples(examples)
    
    # Print summary
    runner.print_summary(summary)
    
    # Export JSON report
    runner.export_json_report("test_report.json")
    
    # Return exit code
    return 0 if summary['failures'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())