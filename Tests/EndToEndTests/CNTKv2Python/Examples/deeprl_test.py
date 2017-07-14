import os
import platform
import shelve
import shutil
import subprocess

import pytest

def test_deeprl():
    #if platform.system() != 'Linux':
    #    pytest.skip('test only runs on Linux (Gym Atari dependency)')

    test_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.join(test_dir, '..', '..', '..', '..', 'Examples',
                              'ReinforcementLearning', 'deeprl', 'scripts')
    script_file = os.path.join(script_dir, 'run.py')
    config_file = os.path.join(script_dir, 'config_examples', 'qlearning.cfg')

    subprocess.call([
        'python', script_file, '--env=CartPole-v0', '--max_steps=5000',
        '--agent_config=' + config_file, '--eval_period=1000',
        '--eval_steps=20000'
    ])

    assert os.path.exists(
        os.path.join(test_dir, 'output', 'output.params')) == True

    wks = shelve.open(os.path.join(test_dir, 'output', 'output.wks'))
    rewards = wks['reward_history']
    assert len(rewards) >= 4 and len(rewards) <= 5
    assert max(rewards) >= 160

    shutil.rmtree(os.path.join(test_dir, 'output'))
