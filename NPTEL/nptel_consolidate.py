import os
import pandas as pd

directory_path = "/home/safi/sanjay/NPTEL/scraped_content"

consolidated_data = {}

for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory_path, filename)
        
        df = pd.read_csv(file_path)
        
        for index, row in df.iterrows():
            course_name = row["Course Name"]
            pdf_number = row["PDF Number"]
            
            if course_name not in consolidated_data:
                consolidated_data[course_name] = []
            
            course_name_without_extension = os.path.splitext(filename)[0]
            course_name_without_prefix = course_name_without_extension.replace("nptel_", "").capitalize()
            consolidated_data[course_name].append((course_name_without_prefix, pdf_number))

# Create a DataFrame from the consolidated_data dictionary
consolidated_df = pd.DataFrame([
    {"Course Name": course_name, **dict(values)}
    for course_name, values in consolidated_data.items()
])

# Normalize the "Course Name" column to lowercase
consolidated_df["Course Name"] = consolidated_df["Course Name"].str.lower()

# Group by "Course Name" and aggregate the values
consolidated_df = consolidated_df.groupby("Course Name").agg(lambda x: ', '.join(x.dropna().astype(str)) if pd.notna(x.iloc[0]) else '').reset_index()

consolidated_df.sort_values(by="Course Name", inplace=True)

consolidated_df.to_csv("/home/safi/sanjay/NPTEL/nptel_final_1.csv", index=False)

print("Consolidated PDF file created successfully.")
