"""
QA Review UI Components
Provides interface components for quality assurance reviewers
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional


def render_qa_sample_badge(worker_name: str, sample_count: int, total_completed: int) -> None:
    """Render a badge showing QA sample information."""
    percentage = round(sample_count / total_completed * 100, 1) if total_completed > 0 else 0
    
    st.markdown(
        f"""
        <div style="
            background-color: #E8EAF6;
            border-left: 4px solid #3F51B5;
            padding: 10px 14px;
            margin: 6px 0;
            border-radius: 3px;
        ">
            <div style="font-size: 15px; font-weight: 600; color: #3F51B5;">
                🎯 QA Sample: {worker_name}
            </div>
            <div style="font-size: 13px; color: #555; margin-top: 3px;">
                {sample_count} of {total_completed} cases selected ({percentage}% sample rate)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_compliance_score_card(score_dict: Dict) -> None:
    """Render a visual compliance score card."""
    percentage = score_dict.get('percentage', 0.0)
    total_score = score_dict.get('total_score', 0.0)
    max_score = score_dict.get('max_score', 0.0)
    
    # Color coding based on score
    if percentage >= 90:
        color = "#4CAF50"  # Green
        emoji = "✅"
        status = "Excellent"
    elif percentage >= 75:
        color = "#FFC107"  # Amber
        emoji = "⚠️"
        status = "Acceptable"
    else:
        color = "#F44336"  # Red
        emoji = "❌"
        status = "Needs Improvement"
    
    st.markdown(
        f"""
        <div style="
            background-color: {color}15;
            border: 2px solid {color};
            padding: 14px;
            margin: 10px 0;
            border-radius: 6px;
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 8px;">
                {emoji}
            </div>
            <div style="font-size: 32px; font-weight: 700; color: {color}; margin-bottom: 4px;">
                {percentage}%
            </div>
            <div style="font-size: 16px; font-weight: 600; color: {color}; margin-bottom: 8px;">
                {status}
            </div>
            <div style="font-size: 14px; color: #666;">
                Score: {total_score} / {max_score} points
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_criteria_checklist(criteria_results: List[Dict]) -> None:
    """Render compliance criteria checklist with pass/fail indicators."""
    st.markdown("### Compliance Criteria Details")
    
    for criterion in criteria_results:
        passed = criterion.get('passed', False)
        category = criterion.get('category', 'Unknown')
        requirement = criterion.get('requirement', '')
        regulation = criterion.get('regulation', '')
        explanation = criterion.get('explanation', '')
        weight = criterion.get('weight', 0)
        points_earned = criterion.get('points_earned', 0)
        
        # Status icon and color
        if passed:
            icon = "✅"
            bg_color = "#E8F5E9"
            border_color = "#4CAF50"
        else:
            icon = "❌"
            bg_color = "#FFEBEE"
            border_color = "#F44336"
        
        with st.expander(f"{icon} {category} - {requirement[:60]}{'...' if len(requirement) > 60 else ''}", expanded=False):
            st.markdown(f"**Requirement:** {requirement}")
            st.markdown(f"**Regulation:** `{regulation}`")
            st.markdown(f"**Weight:** {weight} points")
            st.markdown(f"**Points Earned:** {points_earned}/{weight}")
            
            if passed:
                st.success(f"✓ **Passed:** {explanation}")
            else:
                st.error(f"✗ **Failed:** {explanation}")


def render_qa_metrics_summary(metrics: Dict) -> None:
    """Render QA metrics summary in columns."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Cases Reviewed",
            metrics.get('cases_reviewed', 0)
        )
    
    with col2:
        avg_compliance = metrics.get('avg_compliance', 0.0)
        st.metric(
            "Avg Compliance",
            f"{avg_compliance}%",
            delta=f"{avg_compliance - 75.0:+.1f}% vs 75% target" if avg_compliance > 0 else None
        )
    
    with col3:
        pass_rate = metrics.get('pass_rate', 0.0)
        st.metric(
            "Pass Rate (≥75%)",
            f"{pass_rate}%",
            delta=f"{pass_rate - 85.0:+.1f}% vs 85% target" if pass_rate > 0 else None
        )
    
    with col4:
        st.metric(
            "Workers Reviewed",
            metrics.get('workers_reviewed', 0)
        )


def render_category_breakdown_chart(criteria_breakdown: Dict) -> None:
    """Render a bar chart of compliance rates by category."""
    if not criteria_breakdown:
        st.info("No category data available yet.")
        return
    
    st.markdown("### Compliance by Category")
    
    # Create DataFrame for charting
    df = pd.DataFrame([
        {'Category': cat, 'Pass Rate %': rate}
        for cat, rate in sorted(criteria_breakdown.items(), key=lambda x: x[1], reverse=True)
    ])
    
    if not df.empty:
        st.bar_chart(df.set_index('Category'))
        
        # Also show as table
        with st.expander("View Details", expanded=False):
            st.dataframe(df, use_container_width=True, hide_index=True)


def render_common_issues_list(issues: List[str]) -> None:
    """Render list of most common compliance issues."""
    if not issues:
        st.success("✅ No common compliance issues identified!")
        return
    
    st.markdown("### Top Compliance Issues")
    st.warning(
        "**These issues appeared most frequently in QA reviews:**\n\n" +
        "\n".join(f"{i+1}. {issue}" for i, issue in enumerate(issues[:5]))
    )


def render_qa_review_form(
    row_data: pd.Series,
    report_source: str,
    compliance_score: Dict,
    reviewer_name: str,
) -> Optional[str]:
    """
    Render QA review form and return reviewer notes if submitted.
    
    Returns reviewer_notes if form submitted, None otherwise.
    """
    st.markdown("---")
    st.markdown("### QA Reviewer Notes")
    
    # Show case details
    with st.expander("📄 Case Details", expanded=True):
        case_id = row_data.get('Case Number', row_data.get('Case Row ID', 'Unknown'))
        st.markdown(f"**Case Number:** {case_id}")
        
        if 'Action Taken/Status' in row_data:
            st.markdown(f"**Action Taken:** {row_data.get('Action Taken/Status', 'N/A')}")
        
        if 'Results of Review' in row_data:
            st.markdown(f"**Results:** {row_data.get('Results of Review', 'N/A')}")
        
        if 'Comment' in row_data:
            st.markdown(f"**Worker Comment:** {row_data.get('Comment', 'N/A')}")
    
    # Reviewer notes input
    reviewer_notes = st.text_area(
        "Reviewer Notes & Recommendations:",
        placeholder="Enter observations, coaching points, or corrective actions needed...",
        height=120,
        key=f"qa_notes_{case_id}"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("💾 Save QA Review", type="primary"):
            if not reviewer_notes.strip():
                st.warning("Please enter reviewer notes before saving.")
            else:
                return reviewer_notes
    
    with col2:
        st.caption("Save this review to record compliance score and notes.")
    
    return None


def render_worker_qa_dashboard(worker_name: str, worker_metrics: Dict) -> None:
    """Render QA dashboard for a specific worker."""
    st.markdown(f"### QA Performance: {worker_name}")
    
    if worker_metrics['cases_reviewed'] == 0:
        st.info(f"No QA reviews completed yet for {worker_name}.")
        return
    
    # Metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cases Reviewed", worker_metrics['cases_reviewed'])
    
    with col2:
        avg = worker_metrics['avg_compliance']
        color = "🟢" if avg >= 90 else "🟡" if avg >= 75 else "🔴"
        st.metric(f"{color} Avg Compliance", f"{avg}%")
    
    with col3:
        pass_rate = worker_metrics['pass_rate']
        color = "🟢" if pass_rate >= 85 else "🟡" if pass_rate >= 70 else "🔴"
        st.metric(f"{color} Pass Rate", f"{pass_rate}%")
    
    # Guidance based on performance
    avg = worker_metrics['avg_compliance']
    if avg >= 90:
        st.success("✅ **Excellent Performance** - Consistently meets Ohio compliance standards.")
    elif avg >= 75:
        st.warning("⚠️ **Acceptable Performance** - Meets minimum standards but has room for improvement.")
    else:
        st.error("❌ **Needs Coaching** - Below compliance threshold. Schedule training session.")


def render_report_qa_status_badge(report_id: str, qa_samples: Dict, qa_reviews_count: int) -> None:
    """Render QA status badge for a report."""
    total_samples = sum(len(indices) for indices in qa_samples.values())
    completion_pct = round(qa_reviews_count / total_samples * 100, 1) if total_samples > 0 else 0
    
    if completion_pct >= 100:
        color = "#4CAF50"
        status = "QA Complete"
        icon = "✅"
    elif completion_pct >= 50:
        color = "#FFC107"
        status = "QA In Progress"
        icon = "🔄"
    elif completion_pct > 0:
        color = "#FF9800"
        status = "QA Started"
        icon = "▶️"
    else:
        color = "#9E9E9E"
        status = "QA Pending"
        icon = "⏸️"
    
    st.markdown(
        f"""
        <div style="
            background-color: {color}20;
            border-left: 3px solid {color};
            padding: 8px 12px;
            margin: 4px 0 12px 0;
            border-radius: 3px;
            display: inline-block;
        ">
            <span style="font-size: 14px; font-weight: 600; color: {color};">
                {icon} {status}: {qa_reviews_count}/{total_samples} cases reviewed ({completion_pct}%)
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
