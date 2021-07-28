import argparse
import csv
import os
import pathlib
import re
import zipfile
from pathlib import Path

OUTPUT_DIR = "modified_zips"


def get_snapshot_file_dict(snapshot_directory):
    zips_in_dir = filter(lambda file: file.split('.')[-1].lower() == "zip", os.listdir(snapshot_directory))
    snapshot_dict = {}
    for zip in zips_in_dir:
        base_name = os.path.splitext(zip)[0]
        zip_dict = {
            "zip_location": os.path.join(os.path.abspath(snapshot_directory), zip),
            "unzip_location": os.path.join(os.path.abspath(snapshot_directory), base_name)
        }
        snapshot_dict[base_name] = zip_dict
    return snapshot_dict


def unzip_snapshots(snapshot_dict):
    for zip_name, zip_dict in snapshot_dict.items():
        with zipfile.ZipFile(zip_dict["zip_location"], "r") as zip_ref:
            zip_ref.extractall(zip_dict["unzip_location"])


def get_xml_files_from_snapshot_directories(snapshot_dict):
    xmls = []
    for snap_name, snap_info in snapshot_dict.items():
        xmls += [os.path.join(snap_info["unzip_location"], file) for file in os.listdir(snap_info["unzip_location"]) if
                 file.endswith(".xml")]
    return xmls


def create_output_dir():
    try:
        os.mkdir(OUTPUT_DIR)
    except FileExistsError as e:
        pass


def update_xml_file(xml_file, group_mapping_file, user_mapping_file):
    group_reader = csv.DictReader(group_mapping_file) if group_mapping_file is not None else []
    user_reader = csv.DictReader(user_mapping_file) if user_mapping_file is not None else []

    for row in list(group_reader):
        path = Path(xml_file)
        find = f'<groups nativeId="{row["old_name"]}" name="{row["old_name"]}"/>'
        replace = f'<groups nativeId="{row["new_name"]}" name="{row["new_name"]}"/>'
        text = path.read_text()
        text = text.replace(find, replace)
        path.write_text(text)
    for row in list(user_reader):
        path = Path(xml_file)
        find = f'<users nativeId="{row["old_username"]}" name="{row["old_username"]}"'
        replace = f'<users nativeId="{row["new_username"]}" name="{row["new_username"]}"'
        text = path.read_text()
        text = re.sub(
            f'<users nativeId="{row["old_username"]}" name="{row["old_username"]}" fullName="(.*?)" email="(.*?)"/>',
            r'<users nativeId="%s" name="%s" fullName="\1" email="\2"/>' % (row["new_username"], row["new_username"]),
            text)
        path.write_text(text)


def update_xmls(xml_files, group_mapping_file, user_mapping_file):
    for xml_file in xml_files:
        update_xml_file(xml_file, group_mapping_file, user_mapping_file)


def rezip_directories(snapshot_dict):
    create_output_dir()
    for snap, zip_info in snapshot_dict.items():
        files_to_zip = map(lambda file: os.path.join(zip_info["unzip_location"], file),
                           os.listdir(zip_info["unzip_location"]))
        zip_name = f'{snap}_modified.zip'
        with zipfile.ZipFile(os.path.join(OUTPUT_DIR, zip_name), "w") as zip_out:
            for file in files_to_zip:
                zip_out.write(file, os.path.basename(file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir", type=pathlib.Path,
                        help="Path to directory containing the snapshots to be modified")
    parser.add_argument("-g", "--group_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for group names")
    parser.add_argument("-u", "--user_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for user names")

    # args = parser.parse_args(['-g', './group_mapping.csv', '-u', './user_mapping.csv', "./test_snapshots"])
    args = parser.parse_args(['-h'])

    snapshot_dict = get_snapshot_file_dict(args.snapshot_dir)
    unzip_snapshots(snapshot_dict)
    xml_files = get_xml_files_from_snapshot_directories(snapshot_dict)
    update_xmls(xml_files, user_mapping_file=args.user_mapping_file, group_mapping_file=args.group_mapping_file)
    rezip_directories(snapshot_dict)
