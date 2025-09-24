import pandas as pd
import plotly.express as px
import streamlit as st
import glob

def load_dashboard():
    """
    This function encapsulates the entire dashboard page, including data loading,
    filtering, and visualization. It's called by your main app.py.
    """

    st.title("🎓 JoSAA Analysis Dashboard")
    st.markdown("---")

    # Load the data using a cached function for better performance
    @st.cache_data
    def get_data():
        """Loads and combines all 'allrounds.csv' files from the './all data/' directory."""
        # Use glob to find all combined CSV files
        all_files = glob.glob("./all data/*allrounds.csv")
        
        if not all_files:
            # Display a persistent error if no data files are found
            st.error("FATAL: No data files found in the './all data/' directory. Please check the folder name and path.")
            return pd.DataFrame()  # Return an empty DataFrame to prevent the app from crashing

        # Load and combine all yearly data into a single DataFrame
        df_list = [pd.read_csv(file) for file in all_files]
        df = pd.concat(df_list, ignore_index=True)
        return df

    # --- Load Data ---
    df = get_data()

    # --- Main App Logic ---
    # Only proceed if the initial data loading was successful and the DataFrame is not empty
    if not df.empty:
        st.sidebar.header("Please Filter Here:")

        # --- Sidebar Filters ---
        # The filters are now cascading: choices in one filter update the options in the next.
        
        # 1. Year Filter
        selected_years = st.sidebar.multiselect(
            "Select Year:",
            options=sorted(df["year"].unique(), reverse=True),
            default=sorted(df["year"].unique(), reverse=True)
        )
        
        # Filter dataframe based on selected years for subsequent filters
        df_filtered_by_year = df[df['year'].isin(selected_years)]

        # 2. College Filter
        selected_colleges = st.sidebar.multiselect(
            "Select College:",
            options=sorted(df_filtered_by_year['College'].unique())
        )
        
        # Filter further by college for the branch filter
        if selected_colleges:
            df_filtered_by_college = df_filtered_by_year[df_filtered_by_year['College'].isin(selected_colleges)]
        else:
            df_filtered_by_college = df_filtered_by_year

        # 3. Branch Filter
        selected_branches = st.sidebar.multiselect(
            "Select Branch:",
            options=sorted(df_filtered_by_college['Branch'].unique())
        )

        # 4. Other Filters
        selected_quota = st.sidebar.multiselect("Select Quota:", options=df["Quota"].unique(), default=["AI"])
        selected_caste = st.sidebar.multiselect("Select Caste:", options=df["Caste"].unique(), default=["OPEN"])
        selected_gender = st.sidebar.multiselect("Select Gender:", options=df["Gender"].unique(), default=["Gender-Neutral"])
        
        # --- Filtering Logic ---
        # Start with the year-filtered data and apply subsequent filters
        df_selection = df_filtered_by_year.copy()

        if selected_colleges:
            df_selection = df_selection[df_selection['College'].isin(selected_colleges)]
        if selected_branches:
            df_selection = df_selection[df_selection['Branch'].isin(selected_branches)]
        if selected_quota:
            df_selection = df_selection[df_selection['Quota'].isin(selected_quota)]
        if selected_caste:
            df_selection = df_selection[df_selection['Caste'].isin(selected_caste)]
        if selected_gender:
            df_selection = df_selection[df_selection['Gender'].isin(selected_gender)]

        # --- Display Results ---
        st.header("Filtered Results")

        # Check if any data remains after filtering
        if df_selection.empty:
            st.warning("No data available for the selected filters. Please broaden your search.")
        else:
            # --- KPIs Section (Using st.metric for a cleaner look) ---
            st.subheader("Key Performance Indicators")
            
            avg_opening_rank = int(round(df_selection["Opening Rank"].mean(), 0))
            avg_closing_rank = int(round(df_selection["Closing Rank"].mean(), 0))
            best_opening_rank = int(df_selection["Opening Rank"].min())
            max_closing_rank = int(df_selection["Closing Rank"].max())

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric(label="Avg. Opening Rank", value=f"{avg_opening_rank:,}")
            kpi2.metric(label="Avg. Closing Rank", value=f"{avg_closing_rank:,}")
            kpi3.metric(label="Best Opening Rank", value=f"{best_opening_rank:,}")
            kpi4.metric(label="Max. Closing Rank", value=f"{max_closing_rank:,}")

            st.markdown("---")

            # --- Charts Section ---
            st.subheader("Visualizations")
            
            # Group data for charts
            rank_by_college = df_selection.groupby("College")[["Opening Rank", "Closing Rank"]].mean().sort_values("Closing Rank").reset_index()

            # Create a single, more informative bar chart
            fig = px.bar(
                rank_by_college,
                x="College",
                y=["Opening Rank", "Closing Rank"],
                title="<b>Average Opening & Closing Ranks by College</b>",
                template="plotly_white",
                barmode='group', # Puts bars side-by-side for easy comparison
                labels={"value": "Average Rank", "variable": "Rank Type"}
            )
            fig.update_layout(xaxis_title="College", yaxis_title="Average Rank", xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            # --- Data Table Section ---
            st.subheader("Detailed Data View")
            st.dataframe(df_selection)