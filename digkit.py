import argparse
from scripts import bundleid_lookup, apple_warrant, sqlite_queries, hash_algorithms

def main():
    #parser
    parser = argparse.ArgumentParser(prog="digkit", description="digkit (Digital Forensics Toolkit): A collection of digital forensics tools and scripts.")
    subparsers = parser.add_subparsers(dest="tool", required=True)


    # lookup subparser
    lookup = subparsers.add_parser("lookup", help="identifier lookup utilities", description="Look up information associated with application and device identifiers.")
    lookup_sub = lookup.add_subparsers(dest="action", required=True)

    # bundleid
    bundleid = lookup_sub.add_parser("bundleid", help="ios/android bundle id lookup", description="Identifies application names from bundle IDs across app stores.")
    bundleid.add_argument("-s", "--store", dest="store", choices=["apple", "google", "galaxy"], required=True, help="specify which app store to search")
    bundleid.add_argument("bundle_id", help="bundle/package identifier (eg. com.toyopagroup.picaboo)")

    # iccid
    # add tool that verifies ICCID information 

    # imei
    # add tool that verifies IMEI information


    #parse subparser
    parse = subparsers.add_parser("parse", help="artifact parsing utilities", description="Collect, process, and parse information from various data sources.")
    parse_sub = parse.add_subparsers(dest="action", required=True)

    #warrant
    warrant = parse_sub.add_parser("warrant", help="apple warrant preparation tools", description="Tools used for preparing Apple warrant return data.")
    warrant_sub = warrant.add_subparsers(dest="warrant_action", required=True)
    
    download = warrant_sub.add_parser("download", help="download apple warrant return data", description="Downloads all .gpg files from an Apple-supplied .csv file.")
    download.add_argument("-i", "--input", dest="input_csv", metavar="INPUT_CSV", required=True, help="path to apple-supplied .csv file")
    download.add_argument("-o", "--output", dest="output_dir", metavar="OUTPUT_DIR", required=True, help="output directory for downloaded .gpg files")
    
    decrypt = warrant_sub.add_parser("decrypt", help="decrypt apple warrant return data", description="Decrypts all downloaded .gpg files from within a single diretory.")
    decrypt.add_argument("-i", "--input", dest="input_dir", metavar="INPUT_DIR", required=True, help="input directory that contains .gpg files")
    decrypt.add_argument("-o", "--output", dest="output_dir", metavar="OUTPUT_DIR", required=True, help="output directory for decrypted files")
    decrypt.add_argument("-p", "--passphrase", dest="passphrase", metavar="'PASSPHRASE'", required=True, help="apple-supplied passphrase for encrypted files (encapsulate with single quotes)")

    #database
    database = parse_sub.add_parser("database", help="artifact parsers for databases", description="Parses notable artifacts from a selection of supported databases.", formatter_class=argparse.RawTextHelpFormatter)
    database.add_argument("-d", "--database", dest="database", choices=["dwbcommon", "notestore"], required=True,
        help=(
            "specify which database parser to run:\n"
            "  dwbcommon - decodes usage events from dwbCommon.db (console, csv, or html)\n"
            "  notestore - extracts Apple secure note hashes (in hashcat format) from NoteStore.sqlite (console or txt)"
    ))
    database.add_argument("-i", "--input", dest="input_file", metavar="INPUT_FILE", required=True, help="path to input database file")
    database.add_argument("-o", "--output", dest="output_dir", metavar="OUTPUT_DIR", required=False, help="optional output directory for parsed data file")
    database.add_argument("-f", "--format", dest="output_format", choices=["console", "csv", "html", "txt"], required=False, help="output format of parsed data")


    #hash subparser
    hash = subparsers.add_parser("hash", help="file hashing utilities", description="Apply common hashing algorithms to files.")

    hash.add_argument("-a", "--algorithm", dest="algorithm", choices=["md5", "sha1", "sha256"], required=True, help="specify which hash algorithm to use")
    hash.add_argument("-i", "--input", dest="input_file", metavar="INPUT_FILE", required=True, help="path to input file to hash")
    hash.add_argument("-o", "--output", dest="output_dir", metavar="OUTPUT_DIR", required=False, help="path to save hash result")


    #dispatch
    args = parser.parse_args()

    if args.tool == "lookup":
        if args.action == "bundleid":
            if args.store == "apple":
                print(bundleid_lookup.get_apple_store_name(args.bundle_id))
            elif args.store == "google":
                print(bundleid_lookup.get_google_play_name(args.bundle_id))
            elif args.store == "galaxy":
                print(bundleid_lookup.get_galaxy_store_name(args.bundle_id))
    elif args.tool == "parse":
        if args.action == "warrant":
            if args.warrant_action == "download":
                apple_warrant.download_files_from_csv(args.input_csv, args.output_dir)
            elif args.warrant_action == "decrypt":
                apple_warrant.decrypt_gpg_files_in_directory(args.input_dir, args.output_dir, args.passphrase)
        elif args.action == "database":
            if args.database == "notestore":
                output_format = args.output_format or "console"
            else:
                output_format = args.output_format or "csv"
            sqlite_queries.run_sql_by_label(args.database, args.input_file, output_format, args.output_dir)
    elif args.tool == "hash":
        hash_algorithms.calculate_file_hash(args.input_file, args.algorithm, args.output_dir)