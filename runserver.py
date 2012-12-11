#!/usr/bin/env python
from fiveminutes import app

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='5Minutes standup app')
    parser.add_argument('--port', '-p', dest='port', default=5000, type=int,
                        help='the http port to listen on (default 5000)')
    args = parser.parse_args()

    app.run(debug=True, host='0.0.0.0', port=args.port)
