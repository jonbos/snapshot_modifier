import argparse
import csv
import os
import shutil
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup as bs

from src.mapping import GroupMapping, UserMapping, ResolutionMapping, Mapping

OUTPUT_DIR = "../snapshots/modified_snapshots"


def _get_file_basename(zip_filepath):
    return os.path.splitext(os.path.basename(zip_filepath))[0]


def _get_zip_location(zip_filepath):
    return os.path.abspath(zip_filepath)


def _get_unzip_location(zip_filepath):
    return os.path.join(os.path.abspath(os.path.dirname(zip_filepath)), _get_file_basename(zip_filepath))


def get_snapshot_file_dict(snapshot_zips):
    return {
        _get_file_basename(zip_file): {"zip_location": _get_zip_location(zip_file),
                                       "unzip_location": _get_unzip_location(zip_file)}
        for zip_file in snapshot_zips}


def unzip_snapshots(snapshot_dict):
    for _, zip_dict in snapshot_dict.items():
        with zipfile.ZipFile(zip_dict["zip_location"], "r") as zip_ref:
            zip_ref.extractall(zip_dict["unzip_location"])


def get_xml_files_from_snapshot_directories(snapshot_dict):
    xmls = []
    for _, snap_info in snapshot_dict.items():
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
    soup = bs(path.read_text(), 'xml')

    for mapping_function in mapping_list:
        mapping_function.apply(soup)

    path.write_text(soup.prettify())


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


def remove_unzipped_directories(snapshot_dict):
    for snapshot_name, snapshot_info in snapshot_dict.items():
        shutil.rmtree(snapshot_info["unzip_location"])


def create_group_mappings(group_mapping_file) -> list[Mapping]:
    group_reader = csv.DictReader(group_mapping_file) if group_mapping_file is not None else []
    return [GroupMapping(row) for row in group_reader]


def create_user_mappings(user_mapping_file) -> list[Mapping]:
    user_reader = csv.DictReader(user_mapping_file) if user_mapping_file is not None else []
    return [UserMapping(row) for row in user_reader]


def create_resolution_mappings(resolution_mapping_file) -> list[Mapping]:
    resolution_reader = csv.DictReader(resolution_mapping_file) if resolution_mapping_file is not None else []
    return [ResolutionMapping(row) for row in resolution_reader]


def create_mapping_list(parsed_args) -> list[Mapping]:
    return create_group_mappings(parsed_args.group_mapping_file) \
           + create_user_mappings(parsed_args.user_mapping_file) \
           + create_resolution_mappings(parsed_args.resolution_mapping_file)


def modify_snapshots(parsed_args):
    snapshot_dict = get_snapshot_file_dict(parsed_args.snapshot_zips)
    mapping_list = create_mapping_list(parsed_args)
    unzip_snapshots(snapshot_dict)
    xml_files = get_xml_files_from_snapshot_directories(snapshot_dict)
    update_xmls(xml_files, mapping_list)
    rezip_directories(snapshot_dict)
    remove_unzipped_directories(snapshot_dict)


def initialize_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_zips", nargs="+",
                        help="Path to directory containing the snapshots to be modified")
    parser.add_argument("-g", "--group_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for group names")
    parser.add_argument("-u", "--user_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for user names")
    parser.add_argument("-r", "--resolution_mapping_file", type=argparse.FileType('r'), default=None,
                        help="CSV file containing mapping instructions for resolutions")
    return parser.parse_args(
        "-g ../mapping_files/group_mapping.csv -u ../mapping_files/user_mapping.csv ../snapshots/test_snapshots/kmj.zip".split())


if __name__ == '__main__':
    args = initialize_args()
    modify_snapshots(args)
