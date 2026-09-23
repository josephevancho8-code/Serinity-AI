import sys
from serinity.core.agent import SerinityAgent

def main():
    agent = SerinityAgent()
    print("Serinity Agent CLI initialized. Type 'exit' or 'quit' to quit.")
    
    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Exiting...")
                break

            response = agent.process_message(user_input)
            print(f"Agent > {response}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
