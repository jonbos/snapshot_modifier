from src.snapshot_modifier import get_snapshot_file_dict


def test_get_snapshot_file_dict_with_relative_paths_should_return_dict_with_absolute_paths():
    zips = ['../snapshots/test_snapshots/kmj.zip']
    snapshot_dict = get_snapshot_file_dict(zips)
    expected = {
        "kmj":
            {
                "zip_location": '/Users/jon/Projects/Consulting/Sony/snapshot_modifier/snapshots/test_snapshots/kmj.zip',
                "unzip_location": '/Users/jon/Projects/Consulting/Sony/snapshot_modifier/snapshots/test_snapshots/kmj'
            }
    }

    assert snapshot_dict == expected


def test_get_snapshot_file_dict_with_multiple_relative_paths_should_return_dict_with_absolute_paths():
    zips = ['../snapshots/test_snapshots/kmj.zip', '../snapshots/test_snapshots/kmj2.zip']
    snapshot_dict = get_snapshot_file_dict(zips)
    expected = {
        "kmj":
            {
                "zip_location": '/Users/jon/Projects/Consulting/Sony/snapshot_modifier/snapshots/test_snapshots/kmj.zip',
                "unzip_location": '/Users/jon/Projects/Consulting/Sony/snapshot_modifier/snapshots/test_snapshots/kmj'
            }, "kmj2":
            {
                "zip_location": '/Users/jon/Projects/Consulting/Sony/snapshot_modifier/snapshots/test_snapshots/kmj2.zip',
                "unzip_location": '/Users/jon/Projects/Consulting/Sony/snapshot_modifier/snapshots/test_snapshots/kmj2'
            },
    }

    assert snapshot_dict == expected
