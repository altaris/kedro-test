"""
Debugging entrypoint. The `.vscode/launch.json` should look something like

    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Pipeline: training",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": false,
                "env": {
                    "CUDA_VISIBLE_DEVICES": "",
                    "KEDRO_PIPELINE": "training",
                }
            }
            {
                "name": "Pipeline: preprocessing",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": false,
                "env": {
                    "CUDA_VISIBLE_DEVICES": "",
                    "KEDRO_PIPELINE": "preprocessing",
                }
            }
        ]
    }
"""

# pylint: disable=import-error,wrong-import-position

import sys

sys.path.append("src")

import os

from kedro_test.__main__ import main

if __name__ == "__main__":
    if "KEDRO_PIPELINE" in os.environ:
        main(["--pipeline", os.environ["KEDRO_PIPELINE"]])
    elif "KEDRO_NODES" in os.environ:
        main(["--nodes", os.environ["KEDRO_NODES"]])
    else:
        main()
