# Student-Performance-Analysis-System
A comprehensive Python-based system for analyzing student academic performance across multiple subjects and semesters. This tool provides detailed statistical insights, identifies at-risk students, tracks improvements, and generates formatted reports.
<br>
### Core Analysis Capabilities -
- Overall Statistics: Mean, median, standard deviation, min/max scores
- Semester Comparison: Track performance changes between semesters
- Subject-wise Analysis: Individual subject performance across 5 core subjects
- Grade Distribution: A-F grading system with counts and percentages
- Student Rankings: Identify top and bottom performers
- At-Risk Identification: Flag students performing below threshold
- Improvement Tracking: Detect significant improvements or declines
- Section Analysis: Compare performance across different class sections
 <br>
#### DataLoader
Loads and validates student data from CSV files.
#### StatisticsCalculator

- calculate_overall_stats(): Overall performance metrics
- calculate_semester_stats(): Semester-wise comparison
- get_grade_distribution(): A-F grade categorization

#### StudentAnalyzer

- rank_students(): Rank by overall performance
- identify_at_risk(): Flag low-performing students
- track_improvement(): Monitor semester-to-semester changes
- analyze_sections(): Section-level comparisons

#### ReportGenerator

- generate_console_report(): Formatted text report
- save_report(): Export to file
