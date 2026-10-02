import streamlit as st
import pandas as pd
from app.ai.ai_query import ask_database

def run_ai_question(question: str, page_name: str, active_filters: dict = None):
    """Run the existing AI database workflow with active filters awareness and display the result."""
    with st.spinner("Analyzing your marketing data..."):
        try:
            result = ask_database(
                question=question,
                page_name=page_name,
                active_filters=active_filters,
            )

            st.markdown("### 💡 AI Insight")

            # Display active filters applied to the query
            if active_filters:
                filter_parts = []
                if active_filters.get("start_date") and active_filters.get("end_date"):
                    s_d = pd.to_datetime(active_filters["start_date"]).strftime("%b %d, %Y")
                    e_d = pd.to_datetime(active_filters["end_date"]).strftime("%b %d, %Y")
                    filter_parts.append(f"**Date:** {s_d} – {e_d}")
                if active_filters.get("selected_channels"):
                    filter_parts.append(f"**Channels:** {', '.join(active_filters['selected_channels'])}")
                if active_filters.get("selected_campaigns"):
                    filter_parts.append(f"**Campaigns:** {len(active_filters['selected_campaigns'])} selected")

                if filter_parts:
                    st.info("🎯 **Active filters applied to this analysis:**\n\n" + " • ".join(filter_parts))

            # Display structured insight
            st.markdown(result["insight"])

            with st.expander("🔍 View Generated SQL", expanded=False):
                st.code(
                    result["sql"],
                    language="sql",
                )

            with st.expander("📊 View Database Result", expanded=False):
                if result["data"] is not None and not result["data"].empty:
                    st.dataframe(
                        result["data"],
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.caption("Query returned zero rows matching criteria.")

        except Exception as e:
            # User friendly error without exposing raw tracebacks
            st.error("AI analysis is temporarily unavailable or encountered a query constraint.")
            st.caption(f"Details: {str(e)}")

def render_ai_assistant(page_name: str, active_filters: dict = None):
    st.divider()

    st.markdown(
        """
        <div class="section-header-enhanced">
            <span class="section-icon">🤖</span>
            <span class="section-title">AI Marketing Intelligence</span>
            <span class="section-line"></span>
            <span class="section-badge" style="background: rgba(168, 85, 247, 0.15); border-color: rgba(168, 85, 247, 0.4); color: #C084FC;">GROQ AI</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption(f"Ask natural language questions about {page_name}. Active dashboard filters are automatically passed to the AI.")

    # Show active filters banner above question box
    if active_filters:
        filter_pills = []
        if active_filters.get("start_date") and active_filters.get("end_date"):
            s_d = pd.to_datetime(active_filters["start_date"]).strftime("%b %d, %Y")
            e_d = pd.to_datetime(active_filters["end_date"]).strftime("%b %d, %Y")
            filter_pills.append(f"📅 Date: {s_d} – {e_d}")
        if active_filters.get("selected_channels"):
            filter_pills.append(f"🏷️ Channels: {', '.join(active_filters['selected_channels'])}")
        
        if filter_pills:
            st.markdown(
                '<div style="background: linear-gradient(135deg, rgba(24, 34, 52, 0.9) 0%, rgba(17, 24, 39, 0.9) 100%); border: 1px solid rgba(56, 189, 248, 0.35); box-shadow: 0 0 12px rgba(56, 189, 248, 0.15); border-radius: 8px; padding: 7px 14px; margin-bottom: 12px; font-size: 0.8rem; color: #94a3b8;">'
                + ' &nbsp;|&nbsp; '.join(filter_pills)
                + '</div>',
                unsafe_allow_html=True
            )

    # Quick Questions
    st.markdown("**💡 Quick Questions**")
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🏆 Highest ROAS Campaign",
            key=f"quick_roas_{page_name}",
            use_container_width=True,
        ):
            run_ai_question(
                "Which campaign delivered the highest ROAS?",
                page_name,
                active_filters=active_filters,
            )

    with col2:
        if st.button(
            "🔎 Top Performing Keywords / Channels",
            key=f"quick_keywords_{page_name}",
            use_container_width=True,
        ):
            run_ai_question(
                "Which channels or keywords generated the most conversions?",
                page_name,
                active_filters=active_filters,
            )

    # Custom Question
    question = st.text_input(
        "Ask your marketing question",
        placeholder="Example: Which campaign delivered the highest ROAS?",
        key=f"ai_question_{page_name}",
    )

    if st.button(
        "Ask AI",
        key=f"ai_button_{page_name}",
        type="primary",
        use_container_width=True,
    ):
        if not question.strip():
            st.warning("Please enter a question or select a quick question.")
            return

        run_ai_question(
            question,
            page_name,
            active_filters=active_filters,
        )