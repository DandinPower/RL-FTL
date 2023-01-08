from python.model.agent import Agent
from python.libs.graph import Graph

def main():
    agent = Agent()
    agent.Train()
    
    #graph = Graph()
    #graph.ReadFromCsv('python/history/duplicate_distribution.csv')
    #graph.Draw('python/history/duplicate_distribution.png')

if __name__ == "__main__":
    main()