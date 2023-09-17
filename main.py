#!/usr/bin/env python3
from typing import Optional, Any
import argparse
import os
from PyPapertrail.Archive import Archive
from PyPapertrail.Archives import Archives
from apiKey import API_KEY
from configFile import ConfigFile, ConfigFileError
import common
from prettyPrint import print_coloured, print_error, print_warning
from colours import Colours
from spinner import Spinner, STYLE_ARC


def callback(archive: Archive, bytes_downloaded: int, argument: Spinner) -> None:
    print_coloured(" Downloading: ", fg_colour=Colours.fg.green, end='')
    argument.print(end='\r')
    return


def main() -> None:
    log_archives = Archives(api_key=API_KEY)
    for archive in log_archives:
        file_path = os.path.join(common.SETTINGS['output_dir'], archive.file_name)
        print_coloured("Archive date/time: ", fg_colour=Colours.fg.green, end='')
        print(archive.formatted_start_time)
        print_coloured("Archive path: ", fg_colour=Colours.fg.green, end='')
        print(file_path, end=' ')
        print_coloured("File Size: ", fg_colour=Colours.fg.green, end='')
        print(str(archive.file_size))
        if os.path.exists(file_path):
            if common.SETTINGS['mode'] == common.Modes.UPDATE:
                size_on_disk: int = os.path.getsize(file_path)
                print_coloured("Existing file size: ", fg_colour=Colours.fg.green, end='')
                print(str(size_on_disk))
                if size_on_disk == archive.file_size:
                    print_coloured("File size consistent, skipping.", fg_colour=Colours.fg.orange)
                    continue
                print_coloured("File size inconsistent, re-downloading.", fg_colour=Colours.fg.orange)
        spinner = Spinner(style_name=STYLE_ARC)
        print_coloured(" Downloading: ", fg_colour=Colours.fg.green, end='')
        spinner.print(increment_step=False, end='\r')
        archive.download(common.SETTINGS['output_dir'],
                         overwrite=True,
                         callback=callback,
                         argument=spinner,
                         chunk_size=1024)
        spinner.complete = True
        print_coloured(" Downloading: ", fg_colour=Colours.fg.green, end='')
        spinner.print(end='\n')
    return


if __name__ == '__main__':
    print_coloured("+++ Log Downloader +++",
                   fg_colour=Colours.fg.blue,
                   underline=True)
    # Command line arguments:
    parser = argparse.ArgumentParser(description="Download Papertrail log files.")
    # Config file arguments:
    parser.add_argument("-c", "--config",
                        help="Location of the config file.",
                        type=str)
    parser.add_argument('-w', '--write_config',
                        help="Write the config file with the given options and exit.",
                        action='store_true')
    # Output arguments:
    parser.add_argument('-d', '--destination',
                        help="Destination of log files.",
                        type=str)
    write_args = parser.add_mutually_exclusive_group()
    write_args.add_argument("-o", "--overwrite",
                            help="Overwrite existing files.",
                            action='store_true')
    write_args.add_argument("-u", "--update",
                            help="Update the directory, overwrite only if size is not equal to expected size.",
                            action='store_true')
    args = parser.parse_args()
    # Parse args.config, and create Config file:
    try:
        config_file = ConfigFile("PapertrailLogDownloader", args.config, do_load=True)
    except ConfigFileError:
        error: str = "Error loading config file."
        print_error(error)
        exit(10)
    # Parse Destination option:
    if args.destination is not None:
        if os.path.isdir(args.destination):
            common.SETTINGS['output_dir'] = args.destination
        else:
            error: str = "Specified destination doesn't exist or isn't a directory."
            print_error(error)
            exit(11)
    # Parse Operating mode:
    if args.overwrite:
        common.SETTINGS['mode'] = common.Modes.OVERWRITE
    elif args.update:
        common.SETTINGS['mode'] = common.Modes.UPDATE
    # Parse writing config now that all options are set:
    if args.write_config:
        try:
            print_coloured("Writing config.", fg_colour=Colours.fg.green)
            config_file.save()
            print_coloured("Complete.", fg_colour=Colours.fg.green)
        except ConfigFileError:
            error: str = "Error saving config file."
            print_error(error)
            exit(12)
        exit(0)
    # Download some logs:
    main()
    exit(0)
