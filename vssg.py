#!/usr/bin/env python
import toml, mako, argparse, os, colorama

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process a VSSG project.')
	parser.add_argument('project', type=str, help="The project directory containing a project.toml")
	parser.add_argument('outdir', type=str, help="The directory to output the completed project to")
	args = parser.parse_args()

	config = toml.load(os.path.join(args.project, 'project.toml'))

	if not os.path.isdir(args.outdir):
		os.mkdir(args.outdir)
