def kpis_from_df(df):
    return {
        "days": df["date"].nunique(),
        "hours": float(df["duration_hours"].sum()),
        "meetings_pct": float(df[df["activity_type"]=="Calendar"]["duration_hours"].sum() / max(1, df["duration_hours"].sum()))
    }
