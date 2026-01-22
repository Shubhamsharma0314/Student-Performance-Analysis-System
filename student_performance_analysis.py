"""
Student Performance Analysis System
"""

import numpy as np
import sys


# ==================== DATA LOADER MODULE ====================
class DataLoader:
    """Handles data loading and validation from CSV files."""
    
    @staticmethod
    def load_data(filename):
        try:
            student_ids = np.genfromtxt(
                filename, delimiter=',', skip_header=1, 
                usecols=0, dtype=int
            )
            sections = np.genfromtxt(
                filename, delimiter=',', skip_header=1, 
                usecols=2, dtype=str
            )
            grades = np.genfromtxt(
                filename, delimiter=',', skip_header=1, 
                usecols=range(3, 13)
            )
            return student_ids, sections, grades
        
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading data: {e}")
        return None, None, None


# ==================== STATISTICS MODULE ====================
class StatisticsCalculator:
    
    SUBJECTS = ['Math', 'Physics', 'Chemistry', 'English', 'Computer Science']
    
    @staticmethod
    def calculate_overall_stats(grades):
        """Calculate overall statistics for all grades."""
        return {
            'overall_avg': np.mean(grades),
            'overall_std': np.std(grades),
            'overall_median': np.median(grades),
            'max': np.max(grades),
            'min': np.min(grades)
        }
    
    @staticmethod
    def calculate_semester_stats(grades):
        """Calculate semester-wise statistics."""
        sem1_grades = grades[:, :5]
        sem2_grades = grades[:, 5:]
        
        sem1_avg = np.mean(sem1_grades, axis=0)
        sem2_avg = np.mean(sem2_grades, axis=0)
        
        return {
            'sem1_avg': sem1_avg,
            'sem2_avg': sem2_avg,
            'improvement': sem2_avg - sem1_avg,
            'sem1_overall': np.mean(sem1_avg),
            'sem2_overall': np.mean(sem2_avg)
        }
    
    @staticmethod
    def get_grade_distribution(grades):
        """Categorize grades into A, B, C, D, F."""
        all_grades = grades.flatten()
        total = len(all_grades)
        
        grade_ranges = [
            ('A', all_grades >= 90),
            ('B', (all_grades >= 80) & (all_grades < 90)),
            ('C', (all_grades >= 70) & (all_grades < 80)),
            ('D', (all_grades >= 60) & (all_grades < 70)),
            ('F', all_grades < 60)
        ]
        
        distribution = {}
        for grade_letter, mask in grade_ranges:
            count = np.sum(mask)
            distribution[grade_letter] = {
                'count': count,
                'percentage': (count / total) * 100
            }
        
        return distribution


# ==================== STUDENT ANALYZER MODULE ====================
class StudentAnalyzer:
    """Analyzes individual and group student performance."""
    
    @staticmethod
    def rank_students(student_ids, grades, top_n=10):
        """Rank students by total performance."""
        student_averages = np.mean(grades, axis=1)
        ranked_indices = np.argsort(student_averages)[::-1]
        
        top_indices = ranked_indices[:top_n]
        bottom_indices = ranked_indices[-top_n:]
        
        return {
            'averages': student_averages,
            'top_students': {
                'ids': student_ids[top_indices],
                'scores': student_averages[top_indices]
            },
            'bottom_students': {
                'ids': student_ids[bottom_indices],
                'scores': student_averages[bottom_indices]
            }
        }
    
    @staticmethod
    def identify_at_risk(student_ids, grades, threshold=50):
        """Identify students performing below threshold."""
        student_averages = np.mean(grades, axis=1)
        at_risk_mask = student_averages < threshold
        
        at_risk_grades = grades[at_risk_mask]
        weakest_subjects = np.argmin(at_risk_grades, axis=1) if at_risk_grades.size > 0 else np.array([])
        
        return {
            'count': np.sum(at_risk_mask),
            'ids': student_ids[at_risk_mask],
            'averages': student_averages[at_risk_mask],
            'weakest_subject_idx': weakest_subjects,
            'weakest_scores': np.min(at_risk_grades, axis=1) if at_risk_grades.size > 0 else np.array([])
        }
    
    @staticmethod
    def track_improvement(student_ids, grades, threshold=10):
        """Track students with significant improvement or decline."""
        sem1_avg = np.mean(grades[:, :5], axis=1)
        sem2_avg = np.mean(grades[:, 5:], axis=1)
        improvement_delta = sem2_avg - sem1_avg
        
        improved_mask = improvement_delta > threshold
        declined_mask = improvement_delta < -threshold
        
        return {
            'improved': {
                'count': np.sum(improved_mask),
                'ids': student_ids[improved_mask],
                'delta': improvement_delta[improved_mask]
            },
            'declined': {
                'count': np.sum(declined_mask),
                'ids': student_ids[declined_mask],
                'delta': improvement_delta[declined_mask]
            },
            'all_deltas': improvement_delta
        }
    
    @staticmethod
    def analyze_sections(sections, grades):
        """Compare performance across different sections."""
        unique_sections = np.unique(sections)
        section_stats = {}
        
        for section in unique_sections:
            section_mask = sections == section
            section_grades = grades[section_mask]
            
            section_stats[section] = {
                'count': np.sum(section_mask),
                'avg': np.mean(section_grades),
                'std': np.std(section_grades),
                'median': np.median(section_grades),
                'min': np.min(section_grades),
                'max': np.max(section_grades)
            }
        
        return section_stats


# ==================== REPORT GENERATOR MODULE ====================
class ReportGenerator:
    
    @staticmethod
    def generate_console_report(all_stats):
        """Generate a formatted console report."""
        lines = []
        lines.append("=" * 70)
        lines.append("STUDENT PERFORMANCE ANALYSIS REPORT".center(70))
        lines.append("=" * 70)
        
        # Overall Statistics
        overall = all_stats['overall']
        lines.append(f"\n{'OVERALL STATISTICS':^70}")
        lines.append("-" * 70)
        lines.append(f"Average Score:        {overall['overall_avg']:.2f}")
        lines.append(f"Median Score:         {overall['overall_median']:.2f}")
        lines.append(f"Standard Deviation:   {overall['overall_std']:.2f}")
        lines.append(f"Highest Score:        {overall['max']:.2f}")
        lines.append(f"Lowest Score:         {overall['min']:.2f}")
        
        # Semester Comparison
        semester = all_stats['semester']
        lines.append(f"\n{'SEMESTER COMPARISON':^70}")
        lines.append("-" * 70)
        lines.append(f"Semester 1 Average:   {semester['sem1_overall']:.2f}")
        lines.append(f"Semester 2 Average:   {semester['sem2_overall']:.2f}")
        lines.append(f"Overall Improvement:  {semester['sem2_overall'] - semester['sem1_overall']:+.2f}")
        
        # Subject-wise Performance
        lines.append(f"\n{'SUBJECT-WISE PERFORMANCE':^70}")
        lines.append("-" * 70)
        lines.append(f"{'Subject':<20} {'Sem 1':>10} {'Sem 2':>10} {'Change':>10}")
        lines.append("-" * 70)
        for i, subject in enumerate(StatisticsCalculator.SUBJECTS):
            lines.append(
                f"{subject:<20} "
                f"{semester['sem1_avg'][i]:>10.1f} "
                f"{semester['sem2_avg'][i]:>10.1f} "
                f"{semester['improvement'][i]:>+10.1f}"
            )
        
        # Grade Distribution
        distribution = all_stats['distribution']
        lines.append(f"\n{'GRADE DISTRIBUTION':^70}")
        lines.append("-" * 70)
        lines.append(f"{'Grade':<10} {'Count':>15} {'Percentage':>15}")
        lines.append("-" * 70)
        for grade in ['A', 'B', 'C', 'D', 'F']:
            lines.append(
                f"{grade:<10} "
                f"{distribution[grade]['count']:>15} "
                f"{distribution[grade]['percentage']:>14.1f}%"
            )
        
        # At-Risk Students
        at_risk = all_stats['at_risk']
        lines.append(f"\n{'AT-RISK STUDENTS':^70}")
        lines.append("-" * 70)
        lines.append(f"Total At-Risk Students: {at_risk['count']}")
        if at_risk['count'] > 0:
            lines.append(f"\n{'ID':<10} {'Average':>10} {'Weakest Subject':>20} {'Score':>10}")
            lines.append("-" * 70)
            for i in range(min(10, at_risk['count'])):
                subject_idx = at_risk['weakest_subject_idx'][i]
                subject_name = StatisticsCalculator.SUBJECTS[subject_idx % 5]
                lines.append(
                    f"{at_risk['ids'][i]:<10} "
                    f"{at_risk['averages'][i]:>10.1f} "
                    f"{subject_name:>20} "
                    f"{at_risk['weakest_scores'][i]:>10.1f}"
                )
        
        # Top Performers
        rankings = all_stats['rankings']
        lines.append(f"\n{'TOP 10 STUDENTS':^70}")
        lines.append("-" * 70)
        lines.append(f"{'Rank':<10} {'ID':<15} {'Average':>15}")
        lines.append("-" * 70)
        for i, (sid, score) in enumerate(zip(rankings['top_students']['ids'], 
                                             rankings['top_students']['scores']), 1):
            lines.append(f"{i:<10} {sid:<15} {score:>15.2f}")
        
        # Section Analysis
        sections = all_stats['sections']
        lines.append(f"\n{'SECTION-WISE ANALYSIS':^70}")
        lines.append("-" * 70)
        lines.append(f"{'Section':<10} {'Students':>10} {'Average':>12} {'Std Dev':>12} {'Median':>12}")
        lines.append("-" * 70)
        for section, stats in sorted(sections.items()):
            lines.append(
                f"{section:<10} "
                f"{stats['count']:>10} "
                f"{stats['avg']:>12.2f} "
                f"{stats['std']:>12.2f} "
                f"{stats['median']:>12.2f}"
            )
        
        lines.append("\n" + "=" * 70)
        return '\n'.join(lines)
    
    @staticmethod
    def save_report(report, filename='students_analysis_report.txt'):
        try:
            with open(filename, 'w') as f:
                f.write(report)
            print(f"\nReport saved to '{filename}'")
        except Exception as e:
            print(f"Error saving report: {e}")


# ==================== MAIN EXECUTION ====================
def main():
    print("Student Performance Analysis System")
    print("=" * 50)
    
    # Load data
    student_ids, sections, grades = DataLoader.load_data('student_data.csv')
    
    if grades is None:
        print("Failed to load data. Exiting.")
        sys.exit(1)
    
    
    # Run analyses
    overall_stats = StatisticsCalculator.calculate_overall_stats(grades)
    
    semester_stats = StatisticsCalculator.calculate_semester_stats(grades)
    
    rankings = StudentAnalyzer.rank_students(student_ids, grades)

    at_risk = StudentAnalyzer.identify_at_risk(student_ids, grades)
    
    
    section_stats = StudentAnalyzer.analyze_sections(sections, grades)
    distribution = StatisticsCalculator.get_grade_distribution(grades)
    improvements = StudentAnalyzer.track_improvement(student_ids, grades)
    
    # Compile all statistics
    all_stats = {
        'overall': overall_stats,
        'semester': semester_stats,
        'rankings': rankings,
        'at_risk': at_risk,
        'sections': section_stats,
        'distribution': distribution,
        'improvements': improvements
    }
    
    # Generate and display report
    report = ReportGenerator.generate_console_report(all_stats)
    print(report)
    
    # Save report
    ReportGenerator.save_report(report)
    
    # Additional insights
    print(f"\nKey Insights:")
    print(f"- {improvements['improved']['count']} students improved significantly")
    print(f"- {improvements['declined']['count']} students declined significantly")
    print(f"- {at_risk['count']} students need additional support")


if __name__ == "__main__":
    main()