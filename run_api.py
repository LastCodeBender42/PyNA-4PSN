from run_api_module import run_ring_api

def run(file, file_path, current_config, dir_path, progress):
    if len(file) == 0:
        self.log("No object selected", error=True)
        return

    run_ring_api(file_path, current_config, dir_path, progress)
    