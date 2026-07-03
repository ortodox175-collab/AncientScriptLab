from tools.validation_report import ValidationReport


report = ValidationReport(

    experiment="M6.4 Validation of Normalization Methods",

    method="Min-Max",

)

report.add("Distance Stability", "PASS")

report.add("Feature Contribution", "WARNING")

report.add("Outlier Sensitivity", "PASS")

report.add("Small Corpus Behaviour", "WARNING")

report.add("Large Corpus Behaviour", "PASS")

report.add("Numerical Stability", "PASS")

report.add("Scientific Interpretability", "PASS")

report.add("Reproducibility", "PASS")

report.print()

