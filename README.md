# Usage

```
usage: snapshot_modifier.py [-h] [-g GROUP_MAPPING_FILE]
                            [-u USER_MAPPING_FILE]
                            [-r RESOLUTION_MAPPING_FILE]
                            snapshot_zips [snapshot_zips ...]

positional arguments:
  snapshot_zips         One or more CMJ Snapshot .zip files containing values
                        to be mapped

optional arguments:
  -h, --help            show this help message and exit
  -g GROUP_MAPPING_FILE, --group_mapping_file GROUP_MAPPING_FILE
                        CSV file containing mapping instructions for group
                        names
  -u USER_MAPPING_FILE, --user_mapping_file USER_MAPPING_FILE
                        CSV file containing mapping instructions for user
                        names
  -r RESOLUTION_MAPPING_FILE, --resolution_mapping_file RESOLUTION_MAPPING_FILE
                        CSV file containing mapping instructions for
                        resolutions

```
This application expects a directory containing CMJ snapshots and one or more mapping files. 

All zips in the directory will be unarchived, the XMLs scanned and requested mappings made.

Finally, the files will be rearchived and output to the `modified_zips` directory
## Maping File Format
The program expects mapping files with the following format
```
old_name,new_name
TEST,test
...
```
