import os
import pandas as pd
from datetime import datetime

def convert_bytes(num):
    """Convert bytes to GB."""
    gb_size = num / (1024.0 ** 3)
    return round(gb_size, 2)

def delete_files_for_date_csv(csv_path, selected_date, start_time_str, end_time_str):

    folder_name = "/home/vmukti/blobdrive/live-record"

    # Read CSV
    try:
        device_data = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return

    # Time conversion
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()

    output_records = []

    for index, row in device_data.iterrows():

        device_id = str(row['deviceid'])
        sub_folder_path = os.path.join(folder_name, device_id)

        if not os.path.exists(sub_folder_path):
            print(f"⚠️ Folder not found for Device ID: {device_id}")
            continue

        deleted_size = 0
        deleted_count = 0

        for file_name in os.listdir(sub_folder_path):

            if file_name.endswith(".flv"):

                try:
                    # Example:
                    # 2026-04-14-05-45-SSAM-XXXXX.flv

                    parts = file_name.split("-")

                    file_date_str = "-".join(parts[0:3])
                    file_time_str = ":".join(parts[3:5])

                    file_time = datetime.strptime(file_time_str, "%H:%M").time()

                    # Match date & time
                    if (
                        file_date_str == selected_date
                        and start_time <= file_time <= end_time
                    ):

                        file_path = os.path.join(sub_folder_path, file_name)

                        # File size before delete
                        file_size = os.path.getsize(file_path)

                        # Delete file
                        os.remove(file_path)

                        deleted_size += file_size
                        deleted_count += 1

                        print(f"🗑 Deleted: {file_name}")

                except Exception as e:
                    print(f"❌ Error processing file {file_name}: {e}")

        deleted_size_gb = convert_bytes(deleted_size)

        print(
            f"✅ Device: {device_id} | "
            f"Deleted Files: {deleted_count} | "
            f"Deleted Size: {deleted_size_gb} GB"
        )

        output_records.append({
            "deviceid": device_id,
            "deleted_date": selected_date,
            "deleted_files_count": deleted_count,
            "deleted_size_gb": deleted_size_gb
        })

    # Output CSV
    output_folder = "/home/vmukti/Scripts/delete"
    os.makedirs(output_folder, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(csv_path))[0]

    output_csv_path = os.path.join(
        output_folder,
        f"{base_name}_{selected_date}_Deleted_Report.csv"
    )

    output_df = pd.DataFrame(output_records)

    output_df.to_csv(output_csv_path, index=False)

    print(f"\n💾 Output CSV Saved: {output_csv_path}")


if __name__ == "__main__":

    # INPUT CSV
    csv_path = input("Enter CSV file path: ").strip()

    # DATE TO DELETE
    selected_date = "2026-04-17"

    # TIME RANGE
    start_time_str = "00:00"
    end_time_str = "23:59"

    delete_files_for_date_csv(
        csv_path,
        selected_date,
        start_time_str,
        end_time_str
    )

