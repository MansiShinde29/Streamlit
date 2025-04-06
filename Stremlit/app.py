import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Employment Dataset Cleaning 💅")

# Load datasets
raw_df = pd.read_csv(r"C:\Users\Admin\Desktop\Stremlit\Messy_Employment_India_Dataset.csv")
cleaned_df = pd.read_csv(r"C:\Users\Admin\Desktop\Stremlit\cleaned_Dataset.csv")

# Sidebar
st.sidebar.title("🧽 Data Views")
view_option = st.sidebar.radio("Choose your flavor:", ["Side by Side", "Messy Only", "Cleaned Only"])

# Main Title
st.title("💼 Employment Data Cleaning Showcase")
st.subheader("✨ Before & After Transformation with Visual Flair 😎")

# View options
if view_option == "Side by Side":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 😵 Messy Data")
        st.dataframe(raw_df.head(20))

    with col2:
        st.markdown("### 😎 Cleaned Data")
        st.dataframe(cleaned_df.head(20))

elif view_option == "Messy Only":
    st.markdown("### 😵 Messy Dataset")
    st.dataframe(raw_df)

elif view_option == "Cleaned Only":
    st.markdown("### 😎 Cleaned Dataset")
    st.dataframe(cleaned_df)

    # Visualization section
    st.markdown("## 📊 Cleaned Data Visualizations")

    # 🎓 Donut chart - Education
    st.markdown("### 🎓 Education Distribution")
    edu_counts = cleaned_df['Education'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(edu_counts, labels=edu_counts.index, startangle=90, counterclock=False,
            wedgeprops={'width':0.4}, autopct='%1.1f%%')
    ax1.axis('equal')
    st.pyplot(fig1)

    # 🏭 Bar chart - Top Industries
    st.markdown("### 🏭 Top 10 Industries")
    industry_counts = cleaned_df['Industry'].value_counts().head(10)
    st.bar_chart(industry_counts)

    # 📊 Add sidebar to switch between visuals
vis_option = st.sidebar.selectbox(
    "Choose Visualization",
    [
        "None",
        "Salary by Industry",
        "AI Risk Impact",
        "Employment Comparison",
        "Salary by Age & Company",
        "Location-wise Employment"
    ]
)

st.markdown("## 📊 Visual Insights")
if vis_option == "Education Donut":
    st.pyplot(plot_education_donut(cleaned_df)) # type: ignore

elif vis_option == "Top Industries":
    def plot_industry_bar(df):
        top_industries = df['Industry'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_industries.values, y=top_industries.index, ax=ax)
        ax.set_title("Top 10 Industries by Count 📊")
        return fig
    st.pyplot(plot_industry_bar(cleaned_df))

def plot_salary_by_industry(df):
    if "Industry" in df.columns and "Monthly Salary (INR)" in df.columns:
        salary_industry = (
            df.groupby("Industry")["Monthly Salary (INR)"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=salary_industry.values, y=salary_industry.index, palette="coolwarm", ax=ax)
        ax.set_title("💸 Average Monthly Salary by Industry", fontsize=14)
        ax.set_xlabel("Salary (INR)")
        ax.set_ylabel("Industry")
        return fig
    else:
        st.error("❌ Couldn't find 'Industry' or 'Monthly Salary (INR)' column in your data. Clean your damn mess 😤")
        return None
    
if vis_option == "Salary by Industry":
    st.pyplot(plot_salary_by_industry(cleaned_df))

def plot_ai_risk(df):
    if "AI Risk" in df.columns:
        risk_counts = df["AI Risk"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2"))
        ax.set_title("🤖 AI Risk Impact on Employment")
        return fig
    return None

if vis_option == "AI Risk Impact":
    fig = plot_ai_risk(cleaned_df)
    if fig: st.pyplot(fig)
    else: st.warning("No 'AI Risk' column found, babe 😓")

def plot_employment_comparison(df):
    if "Status" in df.columns:
        status_counts = df["Status"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=status_counts.index, y=status_counts.values, palette="coolwarm", ax=ax)
        ax.set_title("👥 Employment vs Unemployment")
        ax.set_ylabel("Count")
        return fig
    return None

if vis_option == "Employment Comparison":
    fig = plot_employment_comparison(cleaned_df)
    if fig: st.pyplot(fig)
    else: st.warning("No 'Employment Status' column found.")

def plot_age_salary_by_company(df):
    # Make sure columns are clean
    df.columns = df.columns.str.strip()

    # If you already have an 'Age Group' column, use it
    if "Age Group" in df.columns and "Industry" in df.columns and "Monthly Salary (INR)" in df.columns:
        grouped = (
            df.groupby(["Industry", "Age Group"])["Monthly Salary (INR)"]
            .mean()
            .reset_index()
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(
            data=grouped,
            x="Industry",
            y="Monthly Salary (INR)",
            hue="Age Group",
            palette="Spectral",
            ax=ax
        )
        ax.set_title("👶👴 Age Group vs Salary per Company")
        ax.set_ylabel("Average Salary (INR)")
        ax.set_xlabel("Industry")
        ax.tick_params(axis='x', rotation=45)
        return fig

    else:
        st.error("💀 One or more required columns are missing: 'Age Group', 'Industry', or 'Monthly Salary (INR)'")
        return None


if vis_option == "Salary by Age & Company":
    fig = plot_age_salary_by_company(cleaned_df)
    if fig: st.pyplot(fig)
    else: st.warning("Missing 'Age' or 'Company' columns 😤")

    import matplotlib.pyplot as plt
import seaborn as sns

def plot_location_employment(df):
    if "Location" in df.columns:
        loc_counts = df["Location"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=loc_counts.values, y=loc_counts.index, palette="mako", ax=ax)
        ax.set_title("🌍 Top 10 Locations by Employment")
        ax.set_xlabel("Number of Employees")
        return fig
    return None
if vis_option == "Location-wise Employment":
    fig = plot_location_employment(cleaned_df)
    if fig:
        st.pyplot(fig)
    else:
        st.warning("No 'Location' column found in dataset.")



   


# Download buttons
st.markdown("### 📥 Download CSVs")
col3, col4 = st.columns(2)
with col3:
    st.download_button("⬇ Download Messy Data", data=raw_df.to_csv(index=False), file_name="Messy_Employment_India_Dataset.csv", mime="text/csv")
with col4:
    st.download_button("⬇ Download Cleaned Data", data=cleaned_df.to_csv(index=False), file_name="cleaned_Dataset.csv", mime="text/csv")
