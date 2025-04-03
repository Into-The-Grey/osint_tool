import json

class OutputManager:
    def __init__(self, config):
        self.output_file = config.get("output_file", "results.json")

    def write(self, graph):
        data = graph.get_data()
        with open(self.output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[+] Results written to {self.output_file}")
