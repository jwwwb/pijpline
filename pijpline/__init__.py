#!/usr/bin/env python3
from typing import Any, Iterable, Mapping

import os
import uuid
import yaml

def load(file: str) -> Mapping[str, Any]:
    """Load a yaml file path into a dictionary."""
    with open(file, 'r') as infile:
        body = yaml.load(infile)
    return body

def split(body: Mapping[str, Any], branch: str) -> Iterable[Mapping[str, Any]]:
    """Extract the specified branch from the body and split it into steps."""
    def branches_for(key: str) -> Iterable[str]:
        if key.startswith('{') and key.endswith('}'):
            return tuple(key[1:-1].split(','))
        else:
            return (key, )
    branches = body['pipelines'].get('branches', {})
    keys = tuple(branches.keys())
    branch_keys = [branches_for(k) for k in keys]
    idx = next((i for i, keys in enumerate(branch_keys) if branch in keys), -1)
    key = '' if idx < 0 else keys[idx]
    steps = (s['step'] for s
             in branches.get(key, body['pipelines']['default']))
    return [dict(step, image=step.get('image', body['image']))
            for step in steps]

def run(step: Mapping[str, Any], environment: Mapping[str, str]) -> None:
    """Execute a step, providing the env variables to the container."""
    print('# Step:', step['name'])
    img = uuid.uuid4()
    command = '#!/bin/sh\n' + '&&\\\n'.join(step['script'])
    dockerfile = (
        [f'FROM {step["image"]}', 'COPY . /root']
        + [f'ENV {key}={value}' for key, value in environment.items()]
        + ['WORKDIR /root', f'RUN chmod +x {img}.sh', f'CMD ./{img}.sh']
    )
    with open(f'{img}.sh', 'w') as outfile:
        outfile.write(command)
    with open(f'DF{img}', 'w') as outfile:
        outfile.write('\n'.join(dockerfile))
    # TODO: don't use os.system lol
    os.system(f'docker build . -f DF{img} -t {img} && docker run {img}')
    os.remove(f'DF{img}')
    os.remove(f'{img}.sh')

def main(file: str, branch: str, environment: Mapping[str, str]) -> None:
    """Load a pipeline file and execute it using the provided env variables."""
    body = load(file)
    steps = split(body, branch)
    for step in steps:
        run(step, environment=environment)
