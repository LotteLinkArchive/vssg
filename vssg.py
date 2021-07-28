#!/usr/bin/env python
import toml, mako, argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process a VSSG project.')
	parser.add_argument('project', type=str, help="The project directory containing a project.toml")
	args = parser.parse_args()
