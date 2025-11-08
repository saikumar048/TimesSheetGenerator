import pandas as pd

def aggregate_data(calendar_data, mail_data, git_data):
    df = pd.DataFrame(calendar_data + mail_data + git_data)
    df.sort_values(by="start_time", inplace=True)
    return df
