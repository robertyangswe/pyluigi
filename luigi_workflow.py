import luigi
import os

class SetupTask(luigi.Task):
    """
    Task to set up the environment and create the external file.
    """
    def output(self):
        return luigi.LocalTarget('data/external_file.txt')

    def run(self):
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Create the external file
        with self.output().open('w') as f:
            f.write('This is an external file')

class ExternalFileTask(luigi.ExternalTask):
    """
    A task that represents an external file dependency.
    This task doesn't create the file - it just checks if it exists.
    """
    def output(self):
        return luigi.LocalTarget('data/external_file.txt')

class FirstTask(luigi.Task):
    """
    First task that creates an initial file.
    """
    def requires(self):
        return SetupTask()

    def output(self):
        return luigi.LocalTarget('data/first_output.txt')

    def run(self):
        with self.output().open('w') as f:
            f.write('First task completed!')

class SecondTask(luigi.Task):
    """
    Second task that depends on FirstTask and an external file.
    """
    def requires(self):
        return {
            'first': FirstTask(),
            'setup': SetupTask(),
            'external': ExternalFileTask()
        }

    def output(self):
        return luigi.LocalTarget('data/final_output.txt')

    def run(self):
        # Read the output from both tasks
        with self.input()['first'].open('r') as f:
            first_output = f.read()
        
        with self.input()['external'].open('r') as f:
            external_output = f.read()
        
        # Create the final output
        with self.output().open('w') as f:
            f.write(f'Second task completed!\nFirst task said: {first_output}\nExternal file said: {external_output}')

class WorkflowWrapper(luigi.WrapperTask):
    """
    A wrapper task that groups all the tasks in the workflow.
    This task doesn't produce any output itself but ensures all tasks are run.
    """
    def requires(self):
        return SecondTask()

if __name__ == '__main__':
    # Use luigi.build with the wrapper task
    success = luigi.build(
        [WorkflowWrapper()],  # List of tasks to run
        local_scheduler=True,  # Use local scheduler
        workers=1,  # Number of workers
        detailed_summary=True  # Get detailed summary
    )
    
    # Print the build status
    print(f"Build {'succeeded' if success else 'failed'}")