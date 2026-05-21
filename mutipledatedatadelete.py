import os
import pandas as pd
from datetime import datetime

def convert_bytes(num):
    """Convert bytes to GB."""
    gb_size = num / (1024.0 ** 3)
    return round(gb_size, 2)


def delete_files_for_date_range_csv(
    csv_path,
    start_date,
    end_date,
    start_time_str,
    end_time_str
):

    folder_name = "/home/vmukti/blobdrive/live-record"

    # Read CSV
    try:
        device_data = pd.read_csv(csv_path)

    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return

    # Convert dates
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Convert times
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()

    output_records = []

    for index, row in device_data.iterrows():

        device_id = str(row['deviceid']).strip()

        sub_folder_path = os.path.join(folder_name, device_id)

        if not os.path.exists(sub_folder_path):
            print(f"⚠️ Folder not found for Device ID: {device_id}")
            continue

        deleted_size = 0
        deleted_count = 0

        print(f"\n🔍 Checking Device: {device_id}")

        for file_name in os.listdir(sub_folder_path):

            if file_name.endswith(".flv"):

                try:
                    # Example filename:
                    # 2026-04-16-05-45-SSAM-XXXXX.flv

                    parts = file_name.split("-")

                    # Extract date
                    file_date_str = "-".join(parts[0:3])

                    # Extract time
                    file_time_str = ":".join(parts[3:5])

                    # Convert
                    file_date = datetime.strptime(
                        file_date_str,
                        "%Y-%m-%d"
                    ).date()

                    file_time = datetime.strptime(
                        file_time_str,
                        "%H:%M"
                    ).time()

                    # Match Date Range + Time Range
                    if (
                        start_date_obj <= file_date <= end_date_obj
                        and start_time <= file_time <= end_time
                    ):

                        file_path = os.path.join(
                            sub_folder_path,
                            file_name
                        )

                        # Get file size
                        file_size = os.path.getsize(file_path)

                        # Delete file
                        os.remove(file_path)

                        deleted_size += file_size
                        deleted_count += 1

                        print(f"🗑 Deleted: {file_name}")

                except Exception as e:
                    print(f"❌ Error processing file '{file_name}': {e}")

        deleted_size_gb = convert_bytes(deleted_size)

        print(
            f"✅ Device: {device_id} | "
            f"Deleted Files: {deleted_count} | "
            f"Deleted Size: {deleted_size_gb} GB"
        )

        output_records.append({
            "deviceid": device_id,
            "start_date": start_date,
            "end_date": end_date,
            "deleted_files_count": deleted_count,
            "deleted_size_gb": deleted_size_gb
        })

    # Save Output CSV
    output_folder = "/home/vmukti/Scripts/delete"

    os.makedirs(output_folder, exist_ok=True)

    base_name = os.path.splitext(
        os.path.basename(csv_path)
    )[0]

    output_csv_path = os.path.join(
        output_folder,
        f"{base_name}_{start_date}_to_{end_date}_Deleted_Report.csv"
    )

    output_df = pd.DataFrame(output_records)

    output_df.to_csv(output_csv_path, index=False)

    print(f"\n💾 Output CSV Saved: {output_csv_path}")


if __name__ == "__main__":

    # Input CSV Path
    csv_path = input("Enter CSV file path: ").strip()

    # Date Range
    start_date = "2026-04-21"
    end_date = "2026-04-28"

    # Time Range
    start_time_str = "00:00"
    end_time_str = "23:59"

    delete_files_for_date_range_csv(
        csv_path,
        start_date,
        end_date,
        start_time_str,
        end_time_str
    )
