#!/usr/bin/env python3
import argparse
from injection import injection
from PageRetriever import PageRetriever
from ParseEngine import ParseEngine
from ResultPresenter import ResultPresenter

# Init injection
injection["page_retriever"] = PageRetriever(injection)
injection["parse_engine"] = ParseEngine(injection)

def parseArgs():
	cliParse = argparse.ArgumentParser()
	cliParse.add_argument("words", nargs="+")
	args = cliParse.parse_args()

	injection["cli_words"] = args.words

def main():
	parseArgs()
	presenter = ResultPresenter(injection)

	for word in injection["cli_words"]:
		presenter.define(word)

if __name__ == "__main__":
	main()
