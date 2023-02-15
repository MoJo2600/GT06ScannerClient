import argparse

import GT06ScannerClient
import logging

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="CLI command to run GT06ScannerClient."
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Specify alternate configuration file.",
        default="config.xml"
    )
    parser.add_argument(
        "-i",
        "--id",
        help="Scanner ID number for GPS tracker (Usually IMEI number)."
    )
    parser.add_argument(
        "-s",
        "--server_address",
        help="Hostname or IP address of GPS tracker server."
    )
    parser.add_argument(
        "-p",
        "--server_port",
        type=int,
        help="Port number for GT06 protocol of GPS tracker server."
    )
    parser.add_argument(
        "-d",
        "--update_delay",
        type=int,
        help="Delay (in seconds) between GPS tracker server updates."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        help="Print verbose status messages."
    )
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO )
    logging.debug(args)

    scanner = GT06ScannerClient.GT06ScannerClient(
        configFile=args.config,
        scannerIDIn=args.id,
        serverAddressIn=args.server_address,
        serverPortIn=args.server_port,
        updateDelayIn=args.update_delay,
    )
    try:
        scanner.connectDevices()
        scanner.runScannerClient()
    except KeyboardInterrupt:
        pass
    finally:
        scanner.disconnectDevices()
