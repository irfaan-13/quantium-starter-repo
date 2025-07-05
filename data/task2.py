import pandas as pd
import os

# Use raw string for Windows path or forward slashes
data_folder = r"C:\Users\george\Downloads\quantium-starter-repo\data"

csv_files = ["daily_sales_data_0.csv", "daily_sales_data_1.csv", "daily_sales_data_2.csv"]

processed_dfs = []

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    print(f"Reading file: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Initial rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")

    # Normalize product column for matching
    df['product'] = df['product'].astype(str).str.strip().str.lower()
    print(f"Unique products: {df['product'].unique()}")

    filtered_df = df[df['product'] == 'pink morsel']
    print(f"Rows after filtering Pink Morsels: {len(filtered_df)}")

    if filtered_df.empty:
        print(f"No Pink Morsels found in {file}, skipping.")
        continue

    filtered_df['Sales'] = filtered_df['quantity'] * filtered_df['price']
    filtered_df = filtered_df[['Sales', 'date', 'region']]
    filtered_df.columns = ['Sales', 'Date', 'Region']

    processed_dfs.append(filtered_df)

if processed_dfs:
    combined_df = pd.concat(processed_dfs, ignore_index=True)
    output_file = "formatted_sales.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")
else:
    print("No data to save. No Pink Morsels found in any file.")