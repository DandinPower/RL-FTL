from python.model.agent import Agent, InferenceAgent

def main():
    agent = Agent()
    agent.Train()
    inferenceAgent = InferenceAgent()
    inferenceAgent.Inference()

if __name__ == "__main__":
    main()