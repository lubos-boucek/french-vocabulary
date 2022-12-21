#!/usr/bin/env python3
import argparse
from injection import injection
from PageRetriever import PageRetriever
from ParseEngine import ParseEngine
from DataLoader import DataLoader
from ResultPresenter import ResultPresenter

def parseArgs():
	cliParse = argparse.ArgumentParser()
	cliParse.add_argument("words", nargs="+")
	
	for key in injection.keys():
		if isinstance(injection[key], str):
			cliParse.add_argument("--" + key, dest=key)

	args = cliParse.parse_args()

	injection["cli_words"] = args.words
	
	for key in injection.keys():
		if isinstance(injection[key], str) and getattr(args, key):
			injection[key] = getattr(args, key)

	print(injection)

def initInjection():
	# Init injection
	injection["page_retriever"] = PageRetriever(injection)
	injection["parse_engine"] = ParseEngine(injection)
	injection["data_loader"] = DataLoader(injection)

def main():
	parseArgs()
	initInjection()

	presenter = ResultPresenter(injection)

	for word in injection["cli_words"]:
		presenter.define(word)

if __name__ == "__main__":
	main()
