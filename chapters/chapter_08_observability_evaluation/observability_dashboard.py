#!/usr/bin/env python3
"""
Observability Dashboard Generator

This utility creates visualization dashboards and reports from
Strands agent observability data for monitoring and analysis.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Any
import glob
import os


class ObservabilityDashboard:
    """Generate dashboards and reports from observability data."""
    
    def __init__(self, data_directory: str = "."):
        """Initialize dashboard generator."""
        self.data_directory = data_directory
        self.metrics_data = []
        self.evaluation_data = []
        self.session_data = []
        
    def load_data(self):
        """Load all observability data files."""
        print("📊 Loading observability data...")
        
        # Load metrics reports
        metrics_files = glob.glob(os.path.join(self.data_directory, "metrics_report_*.json"))
        for file in metrics_files:
            with open(file, 'r') as f:
                data = json.load(f)
                self.metrics_data.extend(data)
        
        # Load evaluation reports
        eval_files = glob.glob(os.path.join(self.data_directory, "evaluation_report_*.json"))
        for file in eval_files:
            with open(file, 'r') as f:
                data = json.load(f)
                self.evaluation_data.extend(data)
        
        # Load session data
        session_files = glob.glob(os.path.join(self.data_directory, "agentcore_session_*.json"))
        for file in session_files:
            with open(file, 'r') as f:
                data = json.load(f)
                self.session_data.append(data)
        
        print(f"   📈 Loaded {len(self.metrics_data)} metrics records")
        print(f"   📋 Loaded {len(self.evaluation_data)} evaluation records")
        print(f"   🔗 Loaded {len(self.session_data)} session records")
    
    def generate_performance_dashboard(self):
        """Generate performance metrics dashboard."""
        if not self.metrics_data:
            print("⚠️  No metrics data available for dashboard")
            return
        
        print("📊 Generating performance dashboard...")
        
        # Create DataFrame
        df = pd.DataFrame(self.metrics_data)
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Strands Agent Performance Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Execution Time Distribution
        axes[0, 0].hist(df['execution_time'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Execution Time Distribution')
        axes[0, 0].set_xlabel('Execution Time (seconds)')
        axes[0, 0].set_ylabel('Frequency')
        
        # 2. Token Usage Over Time
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df_sorted = df.sort_values('timestamp')
        axes[0, 1].plot(range(len(df_sorted)), df_sorted['total_tokens'], marker='o', color='green')
        axes[0, 1].set_title('Token Usage Over Time')
        axes[0, 1].set_xlabel('Query Sequence')
        axes[0, 1].set_ylabel('Total Tokens')
        
        # 3. Cycle Count Analysis
        cycle_counts = df['cycle_count'].value_counts().sort_index()
        axes[0, 2].bar(cycle_counts.index, cycle_counts.values, color='orange', alpha=0.7)
        axes[0, 2].set_title('Reasoning Cycles Distribution')
        axes[0, 2].set_xlabel('Number of Cycles')
        axes[0, 2].set_ylabel('Frequency')
        
        # 4. Tool Usage Frequency
        all_tools = []
        for tools in df['tools_used']:
            all_tools.extend(tools)
        tool_counts = pd.Series(all_tools).value_counts()
        if not tool_counts.empty:
            axes[1, 0].bar(tool_counts.index, tool_counts.values, color='purple', alpha=0.7)
            axes[1, 0].set_title('Tool Usage Frequency')
            axes[1, 0].set_xlabel('Tools')
            axes[1, 0].set_ylabel('Usage Count')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 5. Performance by Category
        if 'category' in df.columns:
            category_perf = df.groupby('category')['execution_time'].mean()
            axes[1, 1].bar(category_perf.index, category_perf.values, color='red', alpha=0.7)
            axes[1, 1].set_title('Average Execution Time by Category')
            axes[1, 1].set_xlabel('Category')
            axes[1, 1].set_ylabel('Avg Execution Time (s)')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        # 6. Token Efficiency (Tokens per Second)
        df['token_efficiency'] = df['total_tokens'] / df['execution_time']
        axes[1, 2].scatter(df['total_tokens'], df['execution_time'], 
                          c=df['token_efficiency'], cmap='viridis', alpha=0.7)
        axes[1, 2].set_title('Token Usage vs Execution Time')
        axes[1, 2].set_xlabel('Total Tokens')
        axes[1, 2].set_ylabel('Execution Time (s)')
        cbar = plt.colorbar(axes[1, 2].collections[0], ax=axes[1, 2])
        cbar.set_label('Tokens/Second')
        
        plt.tight_layout()
        plt.savefig('performance_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Performance dashboard saved as 'performance_dashboard.png'")
    
    def generate_evaluation_dashboard(self):
        """Generate evaluation metrics dashboard."""
        if not self.evaluation_data:
            print("⚠️  No evaluation data available for dashboard")
            return
        
        print("📋 Generating evaluation dashboard...")
        
        df = pd.DataFrame(self.evaluation_data)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Agent Evaluation Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Tool Accuracy by Category
        accuracy_by_category = df.groupby('category')['tool_accuracy'].mean()
        axes[0, 0].bar(accuracy_by_category.index, accuracy_by_category.values, 
                       color='lightgreen', alpha=0.8)
        axes[0, 0].set_title('Tool Selection Accuracy by Category')
        axes[0, 0].set_xlabel('Category')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].set_ylim(0, 1)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Performance Score Distribution
        axes[0, 1].hist(df['performance_score'], bins=15, alpha=0.7, 
                       color='lightblue', edgecolor='black')
        axes[0, 1].set_title('Performance Score Distribution')
        axes[0, 1].set_xlabel('Performance Score (1-10)')
        axes[0, 1].set_ylabel('Frequency')
        
        # 3. Execution Time vs Performance
        axes[1, 0].scatter(df['execution_time'], df['performance_score'], 
                          alpha=0.7, color='orange')
        axes[1, 0].set_title('Execution Time vs Performance Score')
        axes[1, 0].set_xlabel('Execution Time (s)')
        axes[1, 0].set_ylabel('Performance Score')
        
        # 4. Success Rate by Test Category
        success_by_category = df.groupby('category').size()
        axes[1, 1].pie(success_by_category.values, labels=success_by_category.index, 
                       autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Test Distribution by Category')
        
        plt.tight_layout()
        plt.savefig('evaluation_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Evaluation dashboard saved as 'evaluation_dashboard.png'")
    
    def generate_session_analysis(self):
        """Generate session-based analysis."""
        if not self.session_data:
            print("⚠️  No session data available for analysis")
            return
        
        print("🔗 Generating session analysis...")
        
        # Prepare session metrics
        session_metrics = []
        for session in self.session_data:
            metrics = {
                'session_id': session['session_id'],
                'total_queries': session['total_queries'],
                'success_rate': session['successful_queries'] / session['total_queries'] if session['total_queries'] > 0 else 0,
                'avg_duration': session['total_duration'] / session['successful_queries'] if session['successful_queries'] > 0 else 0,
                'total_tokens': session['total_tokens'],
                'timestamp': session['timestamp']
            }
            session_metrics.append(metrics)
        
        df = pd.DataFrame(session_metrics)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Session Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Session Success Rates
        axes[0, 0].bar(range(len(df)), df['success_rate'], alpha=0.7, color='green')
        axes[0, 0].set_title('Success Rate by Session')
        axes[0, 0].set_xlabel('Session Index')
        axes[0, 0].set_ylabel('Success Rate')
        axes[0, 0].set_ylim(0, 1)
        
        # 2. Average Duration Trends
        axes[0, 1].plot(range(len(df)), df['avg_duration'], marker='o', color='blue')
        axes[0, 1].set_title('Average Query Duration Trends')
        axes[0, 1].set_xlabel('Session Index')
        axes[0, 1].set_ylabel('Avg Duration (s)')
        
        # 3. Token Usage per Session
        axes[1, 0].bar(range(len(df)), df['total_tokens'], alpha=0.7, color='purple')
        axes[1, 0].set_title('Token Usage by Session')
        axes[1, 0].set_xlabel('Session Index')
        axes[1, 0].set_ylabel('Total Tokens')
        
        # 4. Queries per Session
        axes[1, 1].bar(range(len(df)), df['total_queries'], alpha=0.7, color='orange')
        axes[1, 1].set_title('Number of Queries by Session')
        axes[1, 1].set_xlabel('Session Index')
        axes[1, 1].set_ylabel('Query Count')
        
        plt.tight_layout()
        plt.savefig('session_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Session analysis saved as 'session_analysis.png'")
    
    def generate_summary_report(self):
        """Generate comprehensive summary report."""
        print("📄 Generating summary report...")
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "data_summary": {
                "metrics_records": len(self.metrics_data),
                "evaluation_records": len(self.evaluation_data),
                "session_records": len(self.session_data)
            }
        }
        
        # Metrics summary
        if self.metrics_data:
            df_metrics = pd.DataFrame(self.metrics_data)
            report["metrics_summary"] = {
                "total_execution_time": float(df_metrics['execution_time'].sum()),
                "average_execution_time": float(df_metrics['execution_time'].mean()),
                "total_tokens": int(df_metrics['total_tokens'].sum()),
                "average_tokens": float(df_metrics['total_tokens'].mean()),
                "total_queries": len(df_metrics),
                "average_cycles": float(df_metrics['cycle_count'].mean()),
                "tool_usage_stats": {}
            }
            
            # Tool usage statistics
            all_tools = []
            for tools in df_metrics['tools_used']:
                all_tools.extend(tools)
            tool_counts = pd.Series(all_tools).value_counts()
            report["metrics_summary"]["tool_usage_stats"] = tool_counts.to_dict()
        
        # Evaluation summary
        if self.evaluation_data:
            df_eval = pd.DataFrame(self.evaluation_data)
            report["evaluation_summary"] = {
                "average_tool_accuracy": float(df_eval['tool_accuracy'].mean()),
                "average_performance_score": float(df_eval['performance_score'].mean()),
                "total_tests": len(df_eval),
                "category_breakdown": df_eval['category'].value_counts().to_dict()
            }
        
        # Session summary
        if self.session_data:
            total_queries = sum(s['total_queries'] for s in self.session_data)
            total_successful = sum(s['successful_queries'] for s in self.session_data)
            total_duration = sum(s['total_duration'] for s in self.session_data)
            
            report["session_summary"] = {
                "total_sessions": len(self.session_data),
                "total_queries": total_queries,
                "overall_success_rate": total_successful / total_queries if total_queries > 0 else 0,
                "total_session_duration": total_duration,
                "average_session_duration": total_duration / len(self.session_data)
            }
        
        # Save report
        with open('observability_summary_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Summary report saved as 'observability_summary_report.json'")
        return report
    
    def generate_all_dashboards(self):
        """Generate all dashboards and reports."""
        print("🚀 GENERATING COMPLETE OBSERVABILITY DASHBOARD SUITE")
        print("=" * 60)
        
        self.load_data()
        
        if not any([self.metrics_data, self.evaluation_data, self.session_data]):
            print("⚠️  No observability data found. Please run the observability examples first.")
            return
        
        # Generate all visualizations
        self.generate_performance_dashboard()
        self.generate_evaluation_dashboard()
        self.generate_session_analysis()
        
        # Generate summary report
        summary = self.generate_summary_report()
        
        print(f"\n🎉 Dashboard suite completed!")
        print("=" * 60)
        print("📊 Generated Files:")
        print("   - performance_dashboard.png")
        print("   - evaluation_dashboard.png") 
        print("   - session_analysis.png")
        print("   - observability_summary_report.json")
        
        if summary:
            print(f"\n📈 Quick Stats:")
            if "metrics_summary" in summary:
                ms = summary["metrics_summary"]
                print(f"   Total Queries: {ms['total_queries']}")
                print(f"   Total Tokens: {ms['total_tokens']:,}")
                print(f"   Avg Execution Time: {ms['average_execution_time']:.2f}s")
            
            if "evaluation_summary" in summary:
                es = summary["evaluation_summary"]
                print(f"   Avg Tool Accuracy: {es['average_tool_accuracy']:.1%}")
                print(f"   Avg Performance Score: {es['average_performance_score']:.1f}/10")
            
            if "session_summary" in summary:
                ss = summary["session_summary"]
                print(f"   Total Sessions: {ss['total_sessions']}")
                print(f"   Overall Success Rate: {ss['overall_success_rate']:.1%}")


def main():
    """Generate observability dashboards."""
    dashboard = ObservabilityDashboard()
    dashboard.generate_all_dashboards()


if __name__ == "__main__":
    main()
