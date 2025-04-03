import time
from utils.module_registry import get_modules_for_target
from utils.output_manager import OutputManager
from utils.graph_builder import GraphBuilder
from utils.tor_controller import TorController


class Controller:
    def __init__(self, config):
        self.config = config
        self.graph = GraphBuilder()  # Now imported from utils.graph_builder
        self.output_manager = OutputManager(config)  # from utils.output_manager
        self.tor = None
        if self.config.get("dark_web_enabled"):
            self.tor = TorController()  # from utils.tor_controller
            self.tor.start()

    def run(self, targets):
        # Use a queue for dynamic target processing
        queue = list(targets)
        processed = set()

        while queue:
            target = queue.pop(0)
            # Skip if already processed
            if target in processed:
                continue
            processed.add(target)

            # Determine which modules should process this target based on its prefix
            modules = get_modules_for_target(target)
            for module in modules:
                print(f"[+] Running {module.name} on target: {target}")
                try:
                    results = module.run(target, self.config)
                except Exception as e:
                    print(f"Error in module {module.name} for target {target}: {e}")
                    continue

                # Add results to the overall graph
                self.graph.add_results(results)

                # Dynamically add new targets discovered during scanning
                for new_target in results.get("new_targets", []):
                    if new_target not in processed:
                        print(f"[*] Discovered new target: {new_target}")
                        queue.append(new_target)

            # Optional: Sleep briefly to avoid overwhelming external services
            time.sleep(1)

        if self.tor:
            self.tor.stop()

        self.output_manager.write(self.graph)
        print("[*] Scan complete!")
        return self.graph
