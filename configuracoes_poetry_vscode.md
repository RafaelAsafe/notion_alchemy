# Configure vscode to poetry projects

obs: remove code runner

## virtual env

add poetry virtual env path in virtualenv paths config vscode 
poetry env activate shows the path


## configurations for debug with poetry 

add lauch config in vscode settings 

"launch": {
        "configurations": [                        
                {
                    "name": "Python Debug Test (Poetry)",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "pytest",
                    "args": ["${file}"],  
                    "console": "integratedTerminal",
                    "justMyCode": true,
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}/tests"  
                    }
                },
                {
                    "name": "Python Debug (Poetry)",
                    "type": "debugpy",
                    "request": "launch",
                    "program": "${file}",  
                    "console": "integratedTerminal",
                    "justMyCode": true,
                    "args": [],  
                    "python": "${command:python.interpreterPath}", 
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}/src" 
                    }
                }
            ]
    }