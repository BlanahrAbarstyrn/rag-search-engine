#!/usr/bin/env python3

import argparse

from lib.keyword_search import (
    search_command,
    build_command,
    tf_command,
    idf_command,
    tfidf_command,)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="Build the inverted index")

    search_parser = subparsers.add_parser("tf", help="calculate term frequencies")
    search_parser.add_argument("doc_id", type=int, help="Document ID to check")
    search_parser.add_argument("term", type=str, help="Search term to find count")

    search_parser = subparsers.add_parser("idf", help="calculate inverse term frequencies")
    search_parser.add_argument("term", type=str, help="Search term to find count")

    search_parser = subparsers.add_parser("tfidf", help="calculate term frequencies")
    search_parser.add_argument("doc_id", type=int, help="Document ID to check")
    search_parser.add_argument("term", type=str, help="Search term to find count")

    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for:", args.query)
            results = search_command(args.query, n_results=5)
            for i, res in enumerate(results, 1):
                print(f"{i}. {res['title']}")
        case "build":
            build_command()
        case "tf":
            tf_command(args.doc_id, args.term)
        case "idf":
            idf_command(args.term)
        case "tfidf":
            tfidf_command(args.doc_id, args.term)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()