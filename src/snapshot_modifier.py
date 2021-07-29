import argparse
import csv
import os
import pathlib
import shutil
import zipfile
from pathlib import Path

from src.mapping_functions import GroupMappingFunction, UserMappingFunction, ResolutionMappingFunction, MappingFunction

OUTPUT_DIR = "./snapshots/modified_snapshots"


def get_snapshot_file_dict(snapshot_directory):
    zips_in_dir = filter(lambda file: file.split('.')[-1].lower() == "zip", os.listdir(snapshot_directory))
    snapshot_dict = {}
    for zip_file in zips_in_dir:
        base_name = os.path.splitext(zip_file)[0]
        zip_dict = {
            "zip_location": os.path.join(os.path.abspath(snapshot_directory), zip_file),
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


def update_xml_file(xml_file, mapping_list):
    path = Path(xml_file)
    text = path.read_text()

    for mapping_function in mapping_list:
        text = mapping_function.apply(text)
    path.write_text(text)


def update_xmls(xml_files, mapping_list):
    for xml_file in xml_files:
        update_xml_file(xml_file, mapping_list)


def rezip_directories(snapshot_dict):
    create_output_dir()
    for snap, zip_info in snapshot_dict.items():
        files_to_zip = map(lambda file: os.path.join(zip_info["unzip_location"], file),
                           os.listdir(zip_info["unzip_location"]))
        zip_name = f'{snap}_modified.zip'

        with zipfile.ZipFile(os.path.join(OUTPUT_DIR, zip_name), "w") as zip_out:
            for file in files_to_zip:
                zip_out.write(file, os.path.basename(file))


def initialize_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir", type=pathlib.Path,
                        help="Path to directory containing the snapshots to be modified")
    parser.add_argument("-g", "--group_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for group names")
    parser.add_argument("-u", "--user_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for user names")
    parser.add_argument("-r", "--resolution_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for resolutions")
    return parser.parse_args("-g ./group_mapping.csv -u ./user_mapping.csv ./snapshots/test_snapshots".split())


def remove_unzipped_directories(snapshot_dict):
    for snapshot_name, snapshot_info in snapshot_dict.items():
        shutil.rmtree(snapshot_info["unzip_location"])


def create_group_mappings(group_mapping_file):
    group_reader = csv.DictReader(group_mapping_file) if group_mapping_file is not None else []
    return [GroupMappingFunction(row) for row in group_reader]


def create_user_mappings(user_mapping_file):
    user_reader = csv.DictReader(user_mapping_file) if user_mapping_file is not None else []
    return [UserMappingFunction(row) for row in user_reader]


def create_resolution_mappings(resolution_mapping_file):
    resolution_reader = csv.DictReader(resolution_mapping_file) if resolution_mapping_file is not None else []
    return [ResolutionMappingFunction(row) for row in resolution_reader]


def create_mapping_list(group_mapping_file, user_mapping_file, resolution_mapping_file) -> list[MappingFunction]:
    return create_group_mappings(group_mapping_file) \
           + create_user_mappings(user_mapping_file) \
           + create_resolution_mappings(resolution_mapping_file)


def modify_snapshots(parsed_args):
    snapshot_dict = get_snapshot_file_dict(parsed_args.snapshot_dir)
    mapping_list = create_mapping_list(group_mapping_file=parsed_args.group_mapping_file,
                                       user_mapping_file=parsed_args.user_mapping_file,
                                       resolution_mapping_file=parsed_args.resolution_mapping_file)
    unzip_snapshots(snapshot_dict)
    xml_files = get_xml_files_from_snapshot_directories(snapshot_dict)
    update_xmls(xml_files, mapping_list)
    rezip_directories(snapshot_dict)
    remove_unzipped_directories(snapshot_dict)


if __name__ == '__main__':
    args = initialize_args()
    modify_snapshots(args)
