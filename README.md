# Barebones Luigi Workflow

This is a minimal Luigi workflow example that runs in Docker, demonstrating task dependencies including external file dependencies and the use of WrapperTask.

## Setup

1. Build and run the workflow:
```bash
docker compose up --build
```

This will create three files:
- `data/external_file.txt`: Created by the SetupTask
- `data/first_output.txt`: Output from the first task
- `data/final_output.txt`: Output from the second task that depends on both other tasks

## Project Structure

- `luigi_workflow.py`: Contains the main workflow tasks
- `requirements.txt`: Lists the Python dependencies
- `Dockerfile`: Defines the container environment
- `docker-compose.yml`: Orchestrates the container setup

## Task Dependencies

The workflow consists of five tasks:
1. `SetupTask`: Creates the data directory and external file
2. `FirstTask`: Creates an initial output file (depends on SetupTask)
3. `ExternalFileTask`: Represents a dependency on the external file
4. `SecondTask`: Depends on both `FirstTask` and the external file
5. `WorkflowWrapper`: A wrapper task that groups all tasks together

## ExternalTask

The `ExternalFileTask` uses Luigi's built-in `ExternalTask` class, which:
- Doesn't create or modify files
- Only checks if the specified file exists
- Fails if the file doesn't exist
- Is useful for depending on files created outside the workflow

## WrapperTask

The `WorkflowWrapper` uses Luigi's built-in `WrapperTask` class, which:
- Doesn't produce any output itself
- Serves as a container for other tasks
- Ensures all required tasks are run
- Provides a clean entry point for the workflow

## Using luigi.build

The workflow uses `luigi.build` instead of `luigi.run` to execute tasks. This provides:
- More control over task execution
- Ability to get build status
- Detailed execution summary
- Control over number of workers
- Better integration with Python code 