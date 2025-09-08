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
import numpy as np
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
        
        # Set up the plotting style with better spacing
        plt.style.use('default')
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Strands Agent Performance Dashboard', fontsize=18, fontweight='bold', y=0.98)
        
        # Adjust spacing between subplots
        plt.subplots_adjust(hspace=0.35, wspace=0.25, top=0.92, bottom=0.08)
        
        # 1. Execution Time Distribution
        axes[0, 0].hist(df['execution_time'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Query Execution Time Distribution', fontsize=12, fontweight='bold', pad=15)
        axes[0, 0].set_xlabel('Execution Time (seconds)', fontsize=10)
        axes[0, 0].set_ylabel('Number of Queries', fontsize=10)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Add summary stats
        mean_time = df['execution_time'].mean()
        axes[0, 0].axvline(mean_time, color='red', linestyle='--', alpha=0.8, label=f'Mean: {mean_time:.2f}s')
        axes[0, 0].legend()
        
        # 2. Token Usage Over Time
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df_sorted = df.sort_values('timestamp')
        axes[0, 1].plot(range(len(df_sorted)), df_sorted['total_tokens'], marker='o', 
                       color='green', linewidth=2, markersize=6)
        axes[0, 1].set_title('Token Usage Progression', fontsize=12, fontweight='bold', pad=15)
        axes[0, 1].set_xlabel('Query Sequence', fontsize=10)
        axes[0, 1].set_ylabel('Total Tokens Used', fontsize=10)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add average line
        avg_tokens = df_sorted['total_tokens'].mean()
        axes[0, 1].axhline(avg_tokens, color='red', linestyle='--', alpha=0.8, label=f'Average: {avg_tokens:.0f}')
        axes[0, 1].legend()
        
        # 3. Reasoning Cycles Analysis
        cycle_counts = df['cycle_count'].value_counts().sort_index()
        bars = axes[0, 2].bar(cycle_counts.index, cycle_counts.values, color='orange', alpha=0.7, edgecolor='black')
        axes[0, 2].set_title('Agent Reasoning Cycles', fontsize=12, fontweight='bold', pad=15)
        axes[0, 2].set_xlabel('Number of Reasoning Cycles', fontsize=10)
        axes[0, 2].set_ylabel('Query Count', fontsize=10)
        axes[0, 2].grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[0, 2].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        # 4. Tool Usage Analysis
        all_tools = []
        for tools in df['tools_used']:
            all_tools.extend(tools)
        
        if all_tools:
            tool_counts = pd.Series(all_tools).value_counts()
            bars = axes[1, 0].bar(range(len(tool_counts)), tool_counts.values, 
                                 color='purple', alpha=0.7, edgecolor='black')
            axes[1, 0].set_title('Tool Usage Frequency', fontsize=12, fontweight='bold', pad=15)
            axes[1, 0].set_xlabel('Tools', fontsize=10)
            axes[1, 0].set_ylabel('Times Used', fontsize=10)
            axes[1, 0].set_xticks(range(len(tool_counts)))
            axes[1, 0].set_xticklabels(tool_counts.index, rotation=45, ha='right')
            axes[1, 0].grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                               f'{int(height)}', ha='center', va='bottom', fontsize=9)
        else:
            axes[1, 0].text(0.5, 0.5, 'No tool usage data available', 
                           ha='center', va='center', transform=axes[1, 0].transAxes, fontsize=12)
            axes[1, 0].set_title('Tool Usage Frequency', fontsize=12, fontweight='bold', pad=15)
        
        # 5. Performance by Query Type
        if 'test_name' in df.columns:
            # Group similar test types
            df['category'] = df['test_name'].apply(lambda x: 
                'Mathematical' if 'calculation' in x.lower() or 'math' in x.lower() else
                'Time-based' if 'time' in x.lower() else
                'Conversational' if 'greeting' in x.lower() or 'hello' in x.lower() else
                'Complex' if 'multi' in x.lower() or 'complex' in x.lower() else
                'Other'
            )
            category_perf = df.groupby('category')['execution_time'].mean()
            bars = axes[1, 1].bar(range(len(category_perf)), category_perf.values, 
                                 color='red', alpha=0.7, edgecolor='black')
            axes[1, 1].set_title('Avg Response Time by Query Type', fontsize=12, fontweight='bold', pad=15)
            axes[1, 1].set_xlabel('Query Category', fontsize=10)
            axes[1, 1].set_ylabel('Avg Execution Time (s)', fontsize=10)
            axes[1, 1].set_xticks(range(len(category_perf)))
            axes[1, 1].set_xticklabels(category_perf.index, rotation=45, ha='right')
            axes[1, 1].grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.05,
                               f'{height:.2f}s', ha='center', va='bottom', fontsize=9)
        else:
            axes[1, 1].text(0.5, 0.5, 'No category data available', 
                           ha='center', va='center', transform=axes[1, 1].transAxes, fontsize=12)
            axes[1, 1].set_title('Avg Response Time by Query Type', fontsize=12, fontweight='bold', pad=15)
        
        # 6. Token Efficiency Analysis
        df['token_efficiency'] = df['total_tokens'] / df['execution_time']
        scatter = axes[1, 2].scatter(df['total_tokens'], df['execution_time'], 
                                   c=df['token_efficiency'], cmap='viridis', alpha=0.7, s=60)
        axes[1, 2].set_title('Token Usage vs Response Time', fontsize=12, fontweight='bold', pad=15)
        axes[1, 2].set_xlabel('Total Tokens Used', fontsize=10)
        axes[1, 2].set_ylabel('Execution Time (s)', fontsize=10)
        axes[1, 2].grid(True, alpha=0.3)
        
        # Add colorbar with proper positioning
        cbar = plt.colorbar(scatter, ax=axes[1, 2], shrink=0.8)
        cbar.set_label('Processing Speed\n(Tokens/Second)', fontsize=9)
        
        # Save with high quality
        plt.savefig('performance_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()  # Close to free memory
        
        print("✅ Performance dashboard saved as 'performance_dashboard.png'")
    
    def generate_evaluation_dashboard(self):
        """Generate evaluation metrics dashboard."""
        if not self.evaluation_data:
            print("⚠️  No evaluation data available for dashboard")
            return
        
        print("📋 Generating evaluation dashboard...")
        
        df = pd.DataFrame(self.evaluation_data)
        
        # Set up the plotting style with better spacing
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Agent Evaluation Dashboard', fontsize=18, fontweight='bold', y=0.95)
        
        # Adjust spacing between subplots
        plt.subplots_adjust(hspace=0.3, wspace=0.25, top=0.88, bottom=0.08)
        
        # 1. Tool Accuracy by Category
        if 'category' in df.columns and 'tool_accuracy' in df.columns:
            accuracy_by_category = df.groupby('category')['tool_accuracy'].mean()
            bars = axes[0, 0].bar(range(len(accuracy_by_category)), accuracy_by_category.values, 
                                 color='lightgreen', alpha=0.8, edgecolor='black')
            axes[0, 0].set_title('Tool Selection Accuracy by Category', fontsize=12, fontweight='bold', pad=15)
            axes[0, 0].set_xlabel('Test Category', fontsize=10)
            axes[0, 0].set_ylabel('Accuracy Score (0-1)', fontsize=10)
            axes[0, 0].set_ylim(0, 1.1)
            axes[0, 0].set_xticks(range(len(accuracy_by_category)))
            axes[0, 0].set_xticklabels(accuracy_by_category.index, rotation=45, ha='right')
            axes[0, 0].grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                               f'{height:.1%}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        else:
            axes[0, 0].text(0.5, 0.5, 'No tool accuracy data available', 
                           ha='center', va='center', transform=axes[0, 0].transAxes, fontsize=12)
            axes[0, 0].set_title('Tool Selection Accuracy by Category', fontsize=12, fontweight='bold', pad=15)
        
        # 2. Performance Score Distribution
        if 'performance_score' in df.columns:
            axes[0, 1].hist(df['performance_score'], bins=10, alpha=0.7, 
                           color='lightblue', edgecolor='black')
            axes[0, 1].set_title('Performance Score Distribution', fontsize=12, fontweight='bold', pad=15)
            axes[0, 1].set_xlabel('Performance Score (1-10)', fontsize=10)
            axes[0, 1].set_ylabel('Number of Tests', fontsize=10)
            axes[0, 1].grid(True, alpha=0.3, axis='y')
            
            # Add mean line
            mean_score = df['performance_score'].mean()
            axes[0, 1].axvline(mean_score, color='red', linestyle='--', alpha=0.8, 
                              label=f'Mean: {mean_score:.1f}', linewidth=2)
            axes[0, 1].legend()
        else:
            axes[0, 1].text(0.5, 0.5, 'No performance score data available', 
                           ha='center', va='center', transform=axes[0, 1].transAxes, fontsize=12)
            axes[0, 1].set_title('Performance Score Distribution', fontsize=12, fontweight='bold', pad=15)
        
        # 3. Execution Time vs Performance Correlation
        if 'execution_time' in df.columns and 'performance_score' in df.columns:
            scatter = axes[1, 0].scatter(df['execution_time'], df['performance_score'], 
                                       alpha=0.7, color='orange', s=60, edgecolors='black')
            axes[1, 0].set_title('Response Time vs Performance Score', fontsize=12, fontweight='bold', pad=15)
            axes[1, 0].set_xlabel('Execution Time (seconds)', fontsize=10)
            axes[1, 0].set_ylabel('Performance Score (1-10)', fontsize=10)
            axes[1, 0].grid(True, alpha=0.3)
            
            # Add trend line
            z = np.polyfit(df['execution_time'], df['performance_score'], 1)
            p = np.poly1d(z)
            axes[1, 0].plot(df['execution_time'], p(df['execution_time']), "r--", alpha=0.8, linewidth=2)
            
            # Calculate correlation
            correlation = df['execution_time'].corr(df['performance_score'])
            axes[1, 0].text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                           transform=axes[1, 0].transAxes, fontsize=10, 
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        else:
            axes[1, 0].text(0.5, 0.5, 'No time vs performance data available', 
                           ha='center', va='center', transform=axes[1, 0].transAxes, fontsize=12)
            axes[1, 0].set_title('Response Time vs Performance Score', fontsize=12, fontweight='bold', pad=15)
        
        # 4. Test Category Distribution
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            colors = plt.cm.Set3(np.linspace(0, 1, len(category_counts)))
            wedges, texts, autotexts = axes[1, 1].pie(category_counts.values, 
                                                     labels=category_counts.index, 
                                                     autopct='%1.1f%%', 
                                                     startangle=90,
                                                     colors=colors,
                                                     explode=[0.05] * len(category_counts))
            axes[1, 1].set_title('Test Distribution by Category', fontsize=12, fontweight='bold', pad=15)
            
            # Improve text readability
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        else:
            axes[1, 1].text(0.5, 0.5, 'No category distribution data available', 
                           ha='center', va='center', transform=axes[1, 1].transAxes, fontsize=12)
            axes[1, 1].set_title('Test Distribution by Category', fontsize=12, fontweight='bold', pad=15)
        
        # Save with high quality
        plt.savefig('evaluation_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()  # Close to free memory
        
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
        
        # Set up the plotting style with better spacing
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('AgentCore Session Analysis Dashboard', fontsize=18, fontweight='bold', y=0.95)
        
        # Adjust spacing between subplots
        plt.subplots_adjust(hspace=0.3, wspace=0.25, top=0.88, bottom=0.08)
        
        # 1. Session Success Rates
        session_labels = [f"Session {i+1}" for i in range(len(df))]
        bars = axes[0, 0].bar(range(len(df)), df['success_rate'], alpha=0.7, 
                             color='green', edgecolor='black')
        axes[0, 0].set_title('Success Rate by Session', fontsize=12, fontweight='bold', pad=15)
        axes[0, 0].set_xlabel('Session', fontsize=10)
        axes[0, 0].set_ylabel('Success Rate (0-1)', fontsize=10)
        axes[0, 0].set_ylim(0, 1.1)
        axes[0, 0].set_xticks(range(len(df)))
        axes[0, 0].set_xticklabels(session_labels, rotation=45, ha='right')
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                           f'{height:.1%}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 2. Average Duration Trends
        axes[0, 1].plot(range(len(df)), df['avg_duration'], marker='o', color='blue', 
                       linewidth=2, markersize=8, markerfacecolor='lightblue', markeredgecolor='blue')
        axes[0, 1].set_title('Average Query Duration Trends', fontsize=12, fontweight='bold', pad=15)
        axes[0, 1].set_xlabel('Session', fontsize=10)
        axes[0, 1].set_ylabel('Avg Duration (seconds)', fontsize=10)
        axes[0, 1].set_xticks(range(len(df)))
        axes[0, 1].set_xticklabels(session_labels, rotation=45, ha='right')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add average line
        overall_avg = df['avg_duration'].mean()
        axes[0, 1].axhline(overall_avg, color='red', linestyle='--', alpha=0.8, 
                          label=f'Overall Avg: {overall_avg:.2f}s', linewidth=2)
        axes[0, 1].legend()
        
        # 3. Token Usage per Session
        bars = axes[1, 0].bar(range(len(df)), df['total_tokens'], alpha=0.7, 
                             color='purple', edgecolor='black')
        axes[1, 0].set_title('Token Usage by Session', fontsize=12, fontweight='bold', pad=15)
        axes[1, 0].set_xlabel('Session', fontsize=10)
        axes[1, 0].set_ylabel('Total Tokens Used', fontsize=10)
        axes[1, 0].set_xticks(range(len(df)))
        axes[1, 0].set_xticklabels(session_labels, rotation=45, ha='right')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + max(df['total_tokens'])*0.01,
                           f'{int(height):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 4. Queries per Session
        bars = axes[1, 1].bar(range(len(df)), df['total_queries'], alpha=0.7, 
                             color='orange', edgecolor='black')
        axes[1, 1].set_title('Number of Queries by Session', fontsize=12, fontweight='bold', pad=15)
        axes[1, 1].set_xlabel('Session', fontsize=10)
        axes[1, 1].set_ylabel('Query Count', fontsize=10)
        axes[1, 1].set_xticks(range(len(df)))
        axes[1, 1].set_xticklabels(session_labels, rotation=45, ha='right')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Save with high quality
        plt.savefig('session_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()  # Close to free memory
        
        print("✅ Session analysis saved as 'session_analysis.png'")
    
    def generate_correlation_analysis(self):
        """Generate correlation analysis between metrics."""
        if not self.metrics_data:
            print("⚠️  No metrics data available for correlation analysis")
            return
        
        print("📊 Generating correlation analysis...")
        
        # Prepare metrics for correlation
        correlation_data = []
        for metric in self.metrics_data:
            correlation_data.append({
                'execution_time': metric.get('execution_time', 0),
                'total_tokens': metric.get('total_tokens', 0),
                'cycle_count': metric.get('cycle_count', 0),
                'tools_count': len(metric.get('tools_used', [])),
                'success_rate': 1.0  # Assuming successful if recorded
            })
        
        if len(correlation_data) < 2:
            print("⚠️  Insufficient data for correlation analysis (need at least 2 records)")
            return
        
        df = pd.DataFrame(correlation_data)
        
        # Calculate correlation matrix
        correlation_matrix = df.corr()
        
        # Set up the figure with better spacing
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Metric Correlation Analysis', fontsize=18, fontweight='bold', y=0.98)
        
        # Adjust spacing
        plt.subplots_adjust(hspace=0.2, wspace=0.3, top=0.85, bottom=0.15)
        
        # 1. Correlation Heatmap
        im = axes[0].imshow(correlation_matrix, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)
        axes[0].set_title('Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
        
        # Set ticks and labels
        tick_labels = ['Execution Time', 'Total Tokens', 'Cycle Count', 'Tools Used', 'Success Rate']
        axes[0].set_xticks(range(len(correlation_matrix.columns)))
        axes[0].set_yticks(range(len(correlation_matrix.columns)))
        axes[0].set_xticklabels(tick_labels, rotation=45, ha='right')
        axes[0].set_yticklabels(tick_labels)
        
        # Add correlation values to heatmap
        for i in range(len(correlation_matrix.columns)):
            for j in range(len(correlation_matrix.columns)):
                value = correlation_matrix.iloc[i, j]
                color = 'white' if abs(value) > 0.5 else 'black'
                axes[0].text(j, i, f'{value:.2f}', ha='center', va='center', 
                           color=color, fontsize=12, fontweight='bold')
        
        # Add colorbar with proper positioning
        cbar = plt.colorbar(im, ax=axes[0], shrink=0.8, aspect=20)
        cbar.set_label('Correlation Coefficient', rotation=270, labelpad=20, fontsize=11)
        
        # 2. Scatter Plot: Tokens vs Execution Time
        if 'total_tokens' in df.columns and 'execution_time' in df.columns:
            # Filter out zero values for better visualization
            plot_data = df[(df['total_tokens'] > 0) & (df['execution_time'] > 0)]
            
            if not plot_data.empty:
                scatter = axes[1].scatter(plot_data['total_tokens'], plot_data['execution_time'], 
                                        alpha=0.6, s=60, c='blue', edgecolors='black')
                axes[1].set_title('Tokens vs Execution Time Relationship', fontsize=14, fontweight='bold', pad=20)
                axes[1].set_xlabel('Token Count', fontsize=12)
                axes[1].set_ylabel('Execution Time (seconds)', fontsize=12)
                axes[1].grid(True, alpha=0.3)
                
                # Add trend line if we have enough data points
                if len(plot_data) > 2:
                    z = np.polyfit(plot_data['total_tokens'], plot_data['execution_time'], 1)
                    p = np.poly1d(z)
                    x_trend = np.linspace(plot_data['total_tokens'].min(), plot_data['total_tokens'].max(), 100)
                    axes[1].plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, 
                               label=f'Trend: y = {z[0]:.4f}x + {z[1]:.2f}')
                    axes[1].legend()
                
                # Add correlation coefficient as text
                corr_coef = plot_data['total_tokens'].corr(plot_data['execution_time'])
                axes[1].text(0.05, 0.95, f'Correlation: {corr_coef:.3f}', 
                           transform=axes[1].transAxes, fontsize=11, fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            else:
                axes[1].text(0.5, 0.5, 'No valid data points\nfor scatter plot', 
                           transform=axes[1].transAxes, ha='center', va='center',
                           fontsize=14, style='italic')
                axes[1].set_title('Tokens vs Execution Time Relationship', fontsize=14, fontweight='bold', pad=20)
        else:
            axes[1].text(0.5, 0.5, 'Insufficient data\nfor scatter plot', 
                       transform=axes[1].transAxes, ha='center', va='center',
                       fontsize=14, style='italic')
            axes[1].set_title('Tokens vs Execution Time Relationship', fontsize=14, fontweight='bold', pad=20)
        
        # Save with high quality
        plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()  # Close to free memory
        
        print("✅ Correlation analysis saved as 'correlation_analysis.png'")
        
        # Print key insights
        print("\n🔍 Key Correlation Insights:")
        print("=" * 40)
        for i, col1 in enumerate(correlation_matrix.columns):
            for j, col2 in enumerate(correlation_matrix.columns):
                if i < j:  # Only print upper triangle
                    corr_val = correlation_matrix.iloc[i, j]
                    if abs(corr_val) > 0.5:
                        strength = "Strong" if abs(corr_val) > 0.7 else "Moderate"
                        direction = "positive" if corr_val > 0 else "negative"
                        print(f"• {strength} {direction} correlation between {col1} and {col2}: {corr_val:.3f}")
        print("=" * 40)
    
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
        self.generate_correlation_analysis()
        
        # Generate summary report
        summary = self.generate_summary_report()
        
        print(f"\n🎉 Dashboard suite completed!")
        print("=" * 60)
        print("📊 Generated Files:")
        print("   - performance_dashboard.png")
        print("   - evaluation_dashboard.png") 
        print("   - session_analysis.png")
        print("   - correlation_analysis.png")
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
