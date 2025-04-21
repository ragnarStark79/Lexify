from enhancer import get_text_enhancer
from database import get_db_handler
import config
import argparse
import time # Although time is used in enhancer, importing here is good practice if used directly

def run_cli():
    enhancer = get_text_enhancer()
    db = get_db_handler()

    if not enhancer.model:
        print("Exiting application due to model loading failure.")
        return

    print("\nSimple Text Enhancer")
    print("Enter text to enhance (or type 'quit' to exit):")

    while True:
        try:
            input_text = input("> ")
            if input_text.lower() == 'quit':
                break
            if not input_text:
                continue

            # Unpack the result tuple
            enhanced_text, duration = enhancer.enhance_text(input_text)

            # Print enhanced text and duration
            print(f"Enhanced: {enhanced_text}")
            if duration is not None:
                print(f"(Took {duration:.2f} seconds)") # Format duration

            # Log the interaction to MongoDB
            # In a real app, you'd collect feedback here (e.g., was this helpful? Y/N)
            user_feedback = None # Placeholder for actual feedback mechanism
            db.log_interaction(
                original_text=input_text,
                enhanced_text=enhanced_text,
                model_name=enhancer.model_name,
                user_feedback=user_feedback
            )

        except EOFError: # Handle Ctrl+D
             break
        except KeyboardInterrupt: # Handle Ctrl+C
             break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Clean up
    db.close_connection()
    print("\nExiting.")

def main():
    parser = argparse.ArgumentParser(description='Text Enhancer AI')
    parser.add_argument('--web', action='store_true', help='Run the web interface instead of CLI')
    parser.add_argument('--port', type=int, default=5000, help='Port for web interface (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Run web server in debug mode')
    
    args = parser.parse_args()
    
    if args.web:
        # Import only when needed to avoid unnecessary dependencies in CLI mode
        from webapp import run_webapp
        print(f"Starting web interface on port {args.port}...")
        print("Open your browser and navigate to http://localhost:5000/")
        run_webapp(debug=args.debug, port=args.port)
    else:
        run_cli()

if __name__ == "__main__":
    main()

