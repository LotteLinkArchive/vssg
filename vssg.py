#!/usr/bin/env python
import toml, mako, argparse, os, colorama, time

if __name__ == '__main__':
	colorama.init(autoreset = True)
	
	parser = argparse.ArgumentParser(
		description = 'Process a VSSG project.')
	parser.add_argument(
		'project',
		type = str,
		help = 'The project directory containing a project.toml')
	parser.add_argument(
		'outdir',
		type = str,
		help = 'The directory to output the completed project to')
	parser.add_argument(
		'--quiet',
		action = 'store_true',
		help = 'Do not output any non-stderr data')
	args = parser.parse_args()

	config = toml.load(os.path.join(args.project, 'project.toml'))

	if not os.path.isdir(args.outdir):
		os.mkdir(args.outdir)
		
	def log(*targs, **kwargs):
		if args.quiet == False:
			targs = list(targs)
			targs[0] = (f"[\x1b[2m{round(time.time())}\x1b[0m] "
				+ targs[0])
			print(*targs, **kwargs)
		
	log(f"Processing target \"{config['general']['name']}\" at "
		+ f"\"{os.path.abspath(args.project)}\"...")
		
	
