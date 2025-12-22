#!/bin/bash
echo 'Compiling master overview...'
pdflatex -interaction=nonstopmode master_overview.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode master_overview.tex > /dev/null 2>&1
echo '  ✓ master_overview.pdf'

echo 'Compiling category reports...'
pdflatex -interaction=nonstopmode category_healthcare.tex > /dev/null 2>&1
echo '  ✓ category_healthcare.pdf'
pdflatex -interaction=nonstopmode category_environment.tex > /dev/null 2>&1
echo '  ✓ category_environment.pdf'
pdflatex -interaction=nonstopmode category_energy.tex > /dev/null 2>&1
echo '  ✓ category_energy.pdf'
pdflatex -interaction=nonstopmode category_resources.tex > /dev/null 2>&1
echo '  ✓ category_resources.pdf'
pdflatex -interaction=nonstopmode category_space.tex > /dev/null 2>&1
echo '  ✓ category_space.pdf'
pdflatex -interaction=nonstopmode category_earth_science.tex > /dev/null 2>&1
echo '  ✓ category_earth_science.pdf'
pdflatex -interaction=nonstopmode category_food_security.tex > /dev/null 2>&1
echo '  ✓ category_food_security.pdf'
pdflatex -interaction=nonstopmode category_technology.tex > /dev/null 2>&1
echo '  ✓ category_technology.pdf'

echo 'Compiling top 10 detailed reports...'
pdflatex -interaction=nonstopmode climate-resilient_agriculture.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode climate-resilient_agriculture.tex > /dev/null 2>&1
echo '  [1/10] ✓ climate-resilient_agriculture.pdf'
pdflatex -interaction=nonstopmode mars_colonization_viability.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode mars_colonization_viability.tex > /dev/null 2>&1
echo '  [2/10] ✓ mars_colonization_viability.pdf'
pdflatex -interaction=nonstopmode carbon_capture_optimization.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode carbon_capture_optimization.tex > /dev/null 2>&1
echo '  [3/10] ✓ carbon_capture_optimization.pdf'
pdflatex -interaction=nonstopmode pandemic_early_warning_system.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode pandemic_early_warning_system.tex > /dev/null 2>&1
echo '  [4/10] ✓ pandemic_early_warning_system.pdf'
pdflatex -interaction=nonstopmode mental_health_crisis_intervention.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode mental_health_crisis_intervention.tex > /dev/null 2>&1
echo '  [5/10] ✓ mental_health_crisis_intervention.pdf'
pdflatex -interaction=nonstopmode volcano_eruption_prediction.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode volcano_eruption_prediction.tex > /dev/null 2>&1
echo '  [6/10] ✓ volcano_eruption_prediction.pdf'
pdflatex -interaction=nonstopmode fusion_energy_breakthrough.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode fusion_energy_breakthrough.tex > /dev/null 2>&1
echo '  [7/10] ✓ fusion_energy_breakthrough.pdf'
pdflatex -interaction=nonstopmode earthquake_early_warning_system.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode earthquake_early_warning_system.tex > /dev/null 2>&1
echo '  [8/10] ✓ earthquake_early_warning_system.pdf'
pdflatex -interaction=nonstopmode ocean_acidification_reversal.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode ocean_acidification_reversal.tex > /dev/null 2>&1
echo '  [9/10] ✓ ocean_acidification_reversal.pdf'
pdflatex -interaction=nonstopmode vertical_farming_at_scale.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode vertical_farming_at_scale.tex > /dev/null 2>&1
echo '  [10/10] ✓ vertical_farming_at_scale.pdf'

rm -f *.aux *.log *.out
echo '
Done! Generated PDFs:'
ls -lh *.pdf
