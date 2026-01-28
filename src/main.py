"""
CLI Entry Point
Beautiful command-line interface for the TikTok Ad Agent
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint

from .agent import TikTokAdAgent


console = Console()


def print_banner():
    """Prints welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║     🎯  TikTok AI Ad Campaign Creator  🎯           ║
║                                                      ║
║     Powered by Gemini AI                            ║
║     Created for SoluLab AI Internship Assignment             ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def main():
    """Main CLI loop"""
    
    print_banner()
    
    try:
        # Initialize agent
        with console.status("[yellow]Initializing AI agent...", spinner="dots"):
            agent = TikTokAdAgent()
        
        # Print greeting
        greeting = agent.get_greeting()
        console.print(Panel(greeting, title="[bold green]Agent[/bold green]", border_style="green"))
        
        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    console.print("\n[yellow]👋 Thanks for using TikTok Ad Creator! Goodbye![/yellow]\n")
                    break
                
                if user_input.lower() == 'help':
                    help_text = """
**Available Commands:**
  • Type naturally to create your campaign
  • `review` - See current campaign details
  • `restart` - Start over
  • `help` - Show this message
  • `exit` - Quit the program
"""
                    console.print(Panel(help_text, title="Help", border_style="yellow"))
                    continue
                
                if user_input.lower() == 'restart':
                    agent = TikTokAdAgent()
                    greeting = agent.get_greeting()
                    console.print(Panel(greeting, title="[bold green]Agent[/bold green]", border_style="green"))
                    continue
                
                if user_input.lower() == 'review':
                    if agent.state.campaign_name:
                        review = f"""
**Current Campaign Details:**

- Campaign Name: {agent.state.campaign_name or '(not set)'}
- Objective: {agent.state.objective or '(not set)'}
- Ad Text: {agent.state.ad_text or '(not set)'}
- CTA: {agent.state.cta or '(not set)'}
- Music ID: {agent.state.music_id or '(not set)'}
"""
                        console.print(Panel(review, title="Campaign Review", border_style="blue"))
                    else:
                        console.print("[yellow]No campaign data yet. Let's start creating one![/yellow]")
                    continue
                
                # Special handling for music upload
                if user_input.lower().startswith('upload '):
                    file_name = user_input[7:].strip()
                    if file_name:
                        with console.status("[yellow]Uploading music...", spinner="dots"):
                            response = agent.handle_music_upload(file_name)
                        console.print(Panel(response, title="[bold green]Agent[/bold green]", border_style="green"))
                    else:
                        console.print("[red]Please specify a file name: upload filename.mp3[/red]")
                    continue
                
                # Process message with agent
                with console.status("[yellow]Thinking...", spinner="dots"):
                    response = agent.process_message(user_input)
                
                # Display response
                console.print(Panel(response, title="[bold green]Agent[/bold green]", border_style="green"))
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Use 'exit' to quit properly.[/yellow]")
                continue
            except Exception as e:
                console.print(f"\n[red]❌ Error: {str(e)}[/red]")
                console.print("[yellow]Type 'restart' to begin again or 'exit' to quit.[/yellow]")
    
    except Exception as e:
        console.print(f"\n[red]❌ Fatal error: {str(e)}[/red]")
        console.print("[yellow]Please check your configuration and try again.[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()