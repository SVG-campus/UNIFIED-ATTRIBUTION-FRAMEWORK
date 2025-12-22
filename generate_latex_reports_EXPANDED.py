#!/usr/bin/env python3
"""
EXPANDED LaTeX Report Generator
Handles 25+ grand challenges with categorization
"""

import json
from datetime import datetime
from pathlib import Path

class ExpandedLatexReportGenerator:
    def __init__(self, report_file="grand_unified_report_EXPANDED.json"):
        self.report_file = report_file
        self.data = self._load_report()
        self.output_dir = Path("latex_reports_EXPANDED")
        self.output_dir.mkdir(exist_ok=True)

    def _load_report(self):
        try:
            with open(self.report_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.report_file} not found!")
            print("Run: python3 integrate_real_data_EXPANDED.py")
            return None

    def generate_all_reports(self):
        if not self.data:
            return

        print("="*70)
        print("📄 GENERATING EXPANDED LATEX REPORTS")
        print("="*70)

        # Generate master overview
        self.generate_master_overview()

        # Generate category summaries
        self.generate_category_reports()

        # Generate top 10 detailed reports only (to keep manageable)
        solutions = sorted(self.data.get('solutions', []), 
                          key=lambda x: x['confidence_score'], 
                          reverse=True)

        print(f"\nGenerating detailed reports for TOP 10 challenges...")
        for i, sol in enumerate(solutions[:10], 1):
            self.generate_challenge_report(sol, i)

        # Generate compilation script
        self.generate_compile_script()

        print(f"\n✅ All reports generated in: {self.output_dir}/")
        print(f"\nGenerated:")
        print(f"  • 1 master overview (all {len(self.data.get('solutions', []))} challenges)")
        print(f"  • {len(self.data.get('by_category', {}))} category summaries")
        print(f"  • 10 detailed challenge reports (top confidence scores)")
        print(f"\nTo compile: cd {self.output_dir} && bash compile_all.sh")

    def generate_master_overview(self):
        """Generate comprehensive overview with all challenges"""
        print("\nGenerating master_overview.tex...")

        sols = self.data.get('solutions', [])
        by_cat = self.data.get('by_category', {})
        sorted_sols = sorted(sols, key=lambda x: x['confidence_score'], reverse=True)

        doc = "\\documentclass[11pt,letterpaper]{article}\n"
        doc += "\\usepackage[utf8]{inputenc}\n"
        doc += "\\usepackage[margin=1in]{geometry}\n"
        doc += "\\usepackage{amsmath,hyperref,booktabs,xcolor,tcolorbox,enumitem}\n"
        doc += "\\usepackage{longtable}\n\n"
        doc += "\\title{\\textbf{\\Large Grand Unified Attribution Framework}\\\\\n"
        doc += "\\large Comprehensive Analysis of " + str(len(sols)) + " Grand Challenges}\n"
        doc += f"\\date{{{datetime.now().strftime('%B %d, %Y')}}}\n\n"
        doc += "\\begin{document}\n\\maketitle\n\n"

        # Abstract
        doc += "\\begin{abstract}\n"
        doc += f"This report presents comprehensive analysis of {len(sols)} major grand challenges "
        doc += f"across {len(by_cat)} categories using the Grand Unified Attribution Framework. "
        doc += f"Confidence scores range from {min(s['confidence_score'] for s in sols):.1%} to "
        doc += f"{max(s['confidence_score'] for s in sols):.1%}. "
        doc += "Solutions leverage cross-domain knowledge transfer, meta-learning, and universal pattern discovery.\n"
        doc += "\\end{abstract}\n\n"

        # Executive summary
        doc += "\\section{Executive Summary}\n\n"
        doc += f"Total Knowledge Nodes: {self.data.get('total_nodes', 0)}\\\n"
        doc += f"Domains Integrated: {self.data.get('total_domains', 0)}\\\n"
        doc += f"Universal Patterns: {self.data.get('total_patterns', 0)}\\\n"
        doc += f"Grand Challenges Solved: {len(sols)}\n\n"

        # By category
        doc += "\\section{Challenges by Category}\n\n"
        for category, count in sorted(by_cat.items()):
            cat_sols = [s for s in sols if s.get('category') == category]
            avg_conf = sum(s['confidence_score'] for s in cat_sols) / len(cat_sols)
            doc += f"\\subsection{{{category}}}\n"
            doc += f"Total Challenges: {count}\\\n"
            doc += f"Average Confidence: {avg_conf:.1%}\n\n"

        # Complete table of all challenges
        doc += "\\section{Complete Challenge List}\n\n"
        doc += "\\begin{longtable}{@{}clccc@{}}\n"
        doc += "\\toprule\n"
        doc += "\\textbf{Rank} & \\textbf{Challenge} & \\textbf{Category} & "
        doc += "\\textbf{Domain} & \\textbf{Confidence} \\\\ \\midrule\n"
        doc += "\\endfirsthead\n"
        doc += "\\multicolumn{5}{c}{\\tablename\\ \\thetable\\ -- continued}\\\\\n"
        doc += "\\toprule\n"
        doc += "\\textbf{Rank} & \\textbf{Challenge} & \\textbf{Category} & "
        doc += "\\textbf{Domain} & \\textbf{Confidence} \\\\ \\midrule\n"
        doc += "\\endhead\n"

        for i, sol in enumerate(sorted_sols, 1):
            challenge_short = sol['challenge'][:40] + "..." if len(sol['challenge']) > 40 else sol['challenge']
            doc += f"{i} & {challenge_short} & {sol.get('category', 'Other')} & "
            doc += f"{sol['domain'].title()} & {sol['confidence_score']:.1%} \\\\\n"

        doc += "\\bottomrule\n"
        doc += "\\caption{All " + str(len(sols)) + " grand challenges ranked by confidence}\n"
        doc += "\\end{longtable}\n\n"

        # Top 10 highlights
        doc += "\\section{Top 10 Solutions}\n\n"
        doc += "Detailed reports available for the top 10 challenges:\n\n"
        for i, sol in enumerate(sorted_sols[:10], 1):
            name = sol['challenge'].replace(' ', '_').lower()
            doc += f"\\subsection{{{sol['challenge']}}}\n"
            doc += f"Category: {sol.get('category', 'Other')}\\\n"
            doc += f"Domain: {sol['domain'].title()}\\\n"
            doc += f"Confidence: {sol['confidence_score']:.1%}\\\n"
            doc += f"Detailed Report: \\texttt{{{name}.pdf}}\n\n"

        doc += "\\section{Methodology}\n"
        doc += "All solutions generated using:\n"
        doc += "\\begin{itemize}\n"
        doc += "\\item Real data from 6 government/academic sources\n"
        doc += "\\item Graph Neural Networks for knowledge representation\n"
        doc += "\\item Meta-learning for rapid adaptation (15 steps)\n"
        doc += "\\item Cross-domain knowledge transfer\n"
        doc += "\\end{itemize}\n\n"

        doc += "\\end{document}\n"

        with open(self.output_dir / "master_overview.tex", 'w') as f:
            f.write(doc)
        print("  ✓ master_overview.tex")

    def generate_category_reports(self):
        """Generate summary report for each category"""
        print("\nGenerating category summaries...")

        by_cat = {}
        for sol in self.data.get('solutions', []):
            cat = sol.get('category', 'Other')
            if cat not in by_cat:
                by_cat[cat] = []
            by_cat[cat].append(sol)

        for category, cat_sols in by_cat.items():
            self.generate_category_report(category, cat_sols)

    def generate_category_report(self, category, solutions):
        """Generate report for a specific category"""
        filename = f"category_{category.replace(' ', '_').lower()}.tex"

        doc = "\\documentclass[11pt,letterpaper]{article}\n"
        doc += "\\usepackage[utf8]{inputenc}\n"
        doc += "\\usepackage[margin=1in]{geometry}\n"
        doc += "\\usepackage{amsmath,hyperref,booktabs,xcolor,tcolorbox,enumitem}\n\n"
        doc += f"\\title{{\\textbf{{\\Large {category} Challenges}}}}\n"
        doc += f"\\date{{{datetime.now().strftime('%B %d, %Y')}}}\n\n"
        doc += "\\begin{document}\n\\maketitle\n\n"

        avg_conf = sum(s['confidence_score'] for s in solutions) / len(solutions)

        doc += "\\section{Overview}\n"
        doc += f"Total Challenges: {len(solutions)}\\\n"
        doc += f"Average Confidence: {avg_conf:.1%}\\\n"
        doc += f"Confidence Range: {min(s['confidence_score'] for s in solutions):.1%} - "
        doc += f"{max(s['confidence_score'] for s in solutions):.1%}\n\n"

        doc += "\\section{Challenge List}\n"
        doc += "\\begin{enumerate}\n"
        sorted_sols = sorted(solutions, key=lambda x: x['confidence_score'], reverse=True)
        for sol in sorted_sols:
            doc += f"\\item \\textbf{{{sol['challenge']}}} ({sol['confidence_score']:.1%})\\\n"
            doc += f"Domain: {sol['domain'].title()}\n"
        doc += "\\end{enumerate}\n\n"

        doc += "\\end{document}\n"

        with open(self.output_dir / filename, 'w') as f:
            f.write(doc)
        print(f"  ✓ {filename}")

    def generate_challenge_report(self, sol, rank):
        """Generate detailed report (same as before)"""
        name = sol['challenge'].replace(' ', '_').lower()

        doc = "\\documentclass[11pt,letterpaper]{article}\n"
        doc += "\\usepackage[utf8]{inputenc}\n"
        doc += "\\usepackage[margin=1in]{geometry}\n"
        doc += "\\usepackage{amsmath,hyperref,booktabs,xcolor,tcolorbox,enumitem}\n\n"
        doc += f"\\title{{\\textbf{{\\Large {sol['challenge']}}}}}\n"
        doc += f"\\date{{{datetime.now().strftime('%B %d, %Y')}}}\n\n"
        doc += "\\begin{document}\n\\maketitle\n\n"

        doc += "\\begin{abstract}\n"
        doc += f"Rank: #{rank} of {self.data.get('total_challenges', 0)}\\\n"
        doc += f"Category: {sol.get('category', 'Other')}\\\n"
        doc += f"Confidence: {sol['confidence_score']:.1%}\n"
        doc += "\\end{abstract}\n\n"

        doc += f"\\section{{Challenge: {sol['challenge']}}}\n"
        doc += f"Domain: {sol['domain'].title()}\\\n"
        doc += f"Category: {sol.get('category', 'Other')}\n\n"

        doc += "\\section{Solution}\n"
        doc += "Novel Approaches:\n\\begin{itemize}\n"
        for approach in sol.get('novel_approaches', []):
            doc += f"\\item {approach}\n"
        doc += "\\end{itemize}\n\n"

        doc += "\\section{Confidence Score}\n"
        doc += f"\\begin{{center}}\\Huge {sol['confidence_score']:.1%}\\end{{center}}\n\n"

        doc += "\\end{document}\n"

        with open(self.output_dir / f"{name}.tex", 'w') as f:
            f.write(doc)

    def generate_compile_script(self):
        """Generate compilation script"""
        print("\nGenerating compile_all.sh...")

        by_cat = self.data.get('by_category', {})
        solutions = sorted(self.data.get('solutions', []), 
                          key=lambda x: x['confidence_score'], 
                          reverse=True)

        script = "#!/bin/bash\n"
        script += "echo 'Compiling master overview...'\n"
        script += "pdflatex -interaction=nonstopmode master_overview.tex > /dev/null 2>&1\n"
        script += "pdflatex -interaction=nonstopmode master_overview.tex > /dev/null 2>&1\n"
        script += "echo '  ✓ master_overview.pdf'\n\n"

        script += "echo 'Compiling category reports...'\n"
        for category in by_cat.keys():
            filename = f"category_{category.replace(' ', '_').lower()}"
            script += f"pdflatex -interaction=nonstopmode {filename}.tex > /dev/null 2>&1\n"
            script += f"echo '  ✓ {filename}.pdf'\n"
        script += "\n"

        script += "echo 'Compiling top 10 detailed reports...'\n"
        for i, sol in enumerate(solutions[:10], 1):
            name = sol['challenge'].replace(' ', '_').lower()
            script += f"pdflatex -interaction=nonstopmode {name}.tex > /dev/null 2>&1\n"
            script += f"pdflatex -interaction=nonstopmode {name}.tex > /dev/null 2>&1\n"
            script += f"echo '  [{i}/10] ✓ {name}.pdf'\n"

        script += "\nrm -f *.aux *.log *.out\n"
        script += "echo '\nDone! Generated PDFs:'\n"
        script += "ls -lh *.pdf\n"

        path = self.output_dir / "compile_all.sh"
        with open(path, 'w') as f:
            f.write(script)

        import os
        os.chmod(path, 0o755)
        print("  ✓ compile_all.sh")

if __name__ == "__main__":
    gen = ExpandedLatexReportGenerator()
    gen.generate_all_reports()
