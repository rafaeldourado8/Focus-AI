#!/usr/bin/env python3
"""
Cerberus AI CLI Tool

Simple command-line interface for Cerberus AI
"""

import sys
from cerberus_ai import CerberusAI
import os

def main():
    api_key = os.getenv("CERBERUS_API_KEY")
    if not api_key:
        print("Error: CERBERUS_API_KEY not set")
        sys.exit(1)
    
    cerberus = CerberusAI(api_key=api_key)
    
    if len(sys.argv) < 2:
        print("Usage: cerberus <command> [args]")
        print("\nCommands:")
        print("  chat <message>       - Chat with Cerberus AI")
        print("  debug <file>         - Debug code file")
        print("  analyze <file>       - Analyze code file")
        print("  models               - List available models")
        print("  usage                - Show usage statistics")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "chat":
        message = " ".join(sys.argv[2:])
        response = cerberus.chat_completion([
            {"role": "user", "content": message}
        ])
        print(response["choices"][0]["message"]["content"])
    
    elif command == "debug":
        file_path = sys.argv[2]
        with open(file_path, 'r') as f:
            code = f.read()
        
        error = input("Enter error message: ")
        language = file_path.split('.')[-1]
        
        response = cerberus.debug_code(error, code, language)
        print(response["debug_info"])
    
    elif command == "analyze":
        file_path = sys.argv[2]
        with open(file_path, 'r') as f:
            code = f.read()
        
        language = file_path.split('.')[-1]
        response = cerberus.analyze_code(code, language)
        print(response["analysis"])
    
    elif command == "models":
        models = cerberus.list_models()
        for model in models["models"]:
            print(f"\n{model['name']} ({model['id']})")
            print(f"  {model['description']}")
            print(f"  Cost: ${model['cost_per_1k_tokens']}/1K tokens")
    
    elif command == "usage":
        usage = cerberus.get_usage()
        print(f"Plan: {usage['plan']}")
        print(f"Total requests: {usage['total_requests']}")
        print(f"Rate limit: {usage['rate_limit']} req/min")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
