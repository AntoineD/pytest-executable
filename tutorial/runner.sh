#! /usr/bin/env bash

echo Hello {{name}}
echo From {{output_path}}

cp -v input output \
	1> executable.stdout \
	2> executable.stderr
