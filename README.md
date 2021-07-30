# Usage

```
positional arguments:
  snapshot_dir          Path to directory containing the snapshots to be modified

optional arguments:
  -h, --help            show this help message and exit
  -g GROUP_MAPPING_FILE, --group_mapping_file GROUP_MAPPING_FILE
                        CSV file containing mapping instructions for group names
  -u USER_MAPPING_FILE, --user_mapping_file USER_MAPPING_FILE
                        CSV file containing mapping instructions for user names
  -r RESOLUTION_MAPPING_FILE, --resolution_mapping_file RESOLUTION_MAPPING_FILE
                        CSV file containing mapping instructions for resolutions
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
