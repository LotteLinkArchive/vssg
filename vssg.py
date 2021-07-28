#!/usr/bin/env python
import toml, tempfile, argparse, os, colorama, time, pathlib, shutil
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

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
	parser.add_argument(
		'--clear',
		action = 'store_true',
		help = 'Clear output directory before writing')
	args = parser.parse_args()

	config = toml.load(os.path.join(args.project, 'project.toml'))

	if not os.path.isdir(args.outdir):
		os.mkdir(args.outdir)
	elif args.clear:
		for path in pathlib.Path(args.outdir).glob("**/*"):
			if path.is_file():
				path.unlink()
			elif path.is_dir():
				shutil.rmtree(path)
		
	def log(*targs, **kwargs):
		try:
			kwargs['force']
		except KeyError:
			kwargs['force'] = False
		
		if args.quiet == False or kwargs['force'] == True:
			targs = list(targs)
			targs[0] = (
				f"[\x1b[2m{str(time.time()).ljust(20, '0')}\x1b[0m] "
				+ targs[0])
			del kwargs['force']
			print(*targs, **kwargs)
		
	log(f"Processing target \"{config['general']['name']}\" at "
		+ f"\"{os.path.abspath(args.project)}\"...")
		
	out = pathlib.Path(args.outdir)
	selector = lambda: pathlib.Path(args.project).glob('**/*')
	count = 0
	for i in selector():
		count += 1
	log(f"Collected {count} files")
	
	tmpdir = tempfile.mkdtemp()
	
	log(f"Initialized temporary directory \"f{tmpdir}\"")
	
	makol = TemplateLookup(
		directories=[args.project],
		output_encoding='utf-8',
		encoding_errors='replace',
		module_directory=tmpdir)
	
	countg = 0
	for i in selector():
		countg += 1
		rel = i.relative_to(pathlib.Path(args.project))
		log(f"[\x1b[32m{countg}/{count}\x1b[0m] Processing \"{rel}\"")
		
		outp = out / rel
		if i.is_dir():
			if not outp.is_dir():
				os.mkdir(outp)
		else:
			if (str(rel) == 'project.toml'
				or rel.suffix in config['files']['project_page_ex']):
				continue
			elif rel.suffix == config['files']['project_page_ext']:
				outp = outp.with_suffix(
					config['files']['project_page_out'])
				
				try:
					open(outp, 'w').write(
						makol.get_template(
							str(rel)).render_unicode(**config))
				except:
					log(
						"\x1b[31mMako template error detected, abort!",
						force = True)
					log(
						exceptions.text_error_template().render(),
						force = True)
					break
			else:
				shutil.copy(i, outp)

	shutil.rmtree(tmpdir)
