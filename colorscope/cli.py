#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ColorScope-CLI - Main CLI Entry Point
轻量级终端颜色对比度检查与可访问性分析引擎

A lightweight terminal color contrast checker with WCAG 2.1 compliance,
color blindness simulation, and intelligent suggestions.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from colorscope import __version__, __description__
from colorscope.contrast import ContrastChecker, Color, ContrastResult, WCAGLevel
from colorscope.colorblind import ColorBlindnessSimulator, ColorBlindnessType
from colorscope.suggestions import ColorSuggester
from colorscope.report import ReportGenerator


# Initialize console
if RICH_AVAILABLE:
    console = Console()
else:
    # Fallback to basic output
    class FallbackConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = FallbackConsole()


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog="colorscope",
        description="🎨 ColorScope-CLI - Lightweight Terminal Color Contrast & Accessibility Analysis Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check contrast between two colors
  colorscope check "#FFFFFF" "#000000"
  
  # Check with detailed output
  colorscope check "#FF5733" "#FFFFFF" --detailed
  
  # Simulate color blindness
  colorscope simulate "#FF5733" --type deuteranopia
  
  # Get suggestions for improving contrast
  colorscope suggest "#FF5733" "#FFFFFF" --level aa
  
  # Batch check from JSON file
  colorscope batch colors.json --output report.md
  
  # Interactive mode
  colorscope interactive
        """,
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Check command
    check_parser = subparsers.add_parser(
        "check",
        help="Check contrast ratio between two colors",
        description="Check contrast ratio between foreground and background colors",
    )
    check_parser.add_argument(
        "foreground",
        help="Foreground color (hex, e.g., #FFFFFF)",
    )
    check_parser.add_argument(
        "background",
        help="Background color (hex, e.g., #000000)",
    )
    check_parser.add_argument(
        "--detailed", "-d",
        action="store_true",
        help="Show detailed output with suggestions",
    )
    check_parser.add_argument(
        "--level", "-l",
        choices=["aa", "aaa"],
        default="aa",
        help="WCAG level to check (default: aa)",
    )
    
    # Simulate command
    sim_parser = subparsers.add_parser(
        "simulate",
        help="Simulate color blindness",
        description="Simulate how colors appear to users with color vision deficiency",
    )
    sim_parser.add_argument(
        "color",
        help="Color to simulate (hex, e.g., #FF5733)",
    )
    sim_parser.add_argument(
        "--type", "-t",
        choices=["protanopia", "deuteranopia", "tritanopia", "achromatopsia",
                 "protanomaly", "deuteranomaly", "tritanomaly", "all"],
        default="all",
        help="Type of color blindness to simulate (default: all)",
    )
    
    # Suggest command
    suggest_parser = subparsers.add_parser(
        "suggest",
        help="Get suggestions for improving contrast",
        description="Get intelligent suggestions for adjusting colors to meet WCAG requirements",
    )
    suggest_parser.add_argument(
        "foreground",
        help="Foreground color (hex, e.g., #FF5733)",
    )
    suggest_parser.add_argument(
        "background",
        help="Background color (hex, e.g., #FFFFFF)",
    )
    suggest_parser.add_argument(
        "--level", "-l",
        choices=["aa", "aaa"],
        default="aa",
        help="Target WCAG level (default: aa)",
    )
    suggest_parser.add_argument(
        "--adjust",
        choices=["foreground", "background", "both"],
        default="foreground",
        help="Which color to adjust (default: foreground)",
    )
    
    # Batch command
    batch_parser = subparsers.add_parser(
        "batch",
        help="Batch check colors from file",
        description="Check multiple color pairs from a JSON or YAML file",
    )
    batch_parser.add_argument(
        "input",
        help="Input file (JSON or YAML)",
    )
    batch_parser.add_argument(
        "--output", "-o",
        help="Output file path",
    )
    batch_parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown", "html", "text"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    
    # Interactive command
    subparsers.add_parser(
        "interactive",
        help="Start interactive mode",
        description="Start interactive TUI mode for color analysis",
    )
    
    return parser


def cmd_check(args):
    """Handle check command"""
    checker = ContrastChecker()
    
    try:
        fg = Color.from_hex(args.foreground)
        bg = Color.from_hex(args.background)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
    
    result = checker.check(fg, bg)
    
    if RICH_AVAILABLE:
        # Create result table
        table = Table(title="🎨 Contrast Check Result", show_header=True, header_style="bold cyan")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Foreground", f"[{fg.to_hex()} on default]  {fg.to_hex()}  [/]")
        table.add_row("Background", f"[{bg.to_hex()} on default]  {bg.to_hex()}  [/]")
        table.add_row("Contrast Ratio", f"[bold]{result.ratio:.2f}:1[/]")
        
        # WCAG compliance
        aa_status = "[green]✅ PASS[/]" if result.aa_normal else "[red]❌ FAIL[/]"
        aaa_status = "[green]✅ PASS[/]" if result.aaa_normal else "[red]❌ FAIL[/]"
        
        table.add_row("WCAG AA (4.5:1)", aa_status)
        table.add_row("WCAG AAA (7:1)", aaa_status)
        table.add_row("Overall Level", f"[bold]{result.wcag_level.value.upper()}[/]")
        
        console.print(table)
        
        # Detailed output
        if args.detailed:
            console.print("\n")
            suggester = ColorSuggester()
            target_level = WCAGLevel.AAA if args.level == "aaa" else WCAGLevel.AA
            
            if not result.is_accessible(target_level):
                suggestions = suggester.suggest_foreground(fg, bg, target_level)
                
                if suggestions:
                    sug_table = Table(title="💡 Suggestions", show_header=True)
                    sug_table.add_column("Original", style="red")
                    sug_table.add_column("Suggested", style="green")
                    sug_table.add_column("New Ratio", style="yellow")
                    sug_table.add_column("Adjustment", style="white")
                    
                    for sug in suggestions[:3]:
                        sug_table.add_row(
                            sug.original.to_hex(),
                            sug.suggested.to_hex(),
                            f"{sug.new_ratio:.2f}:1",
                            sug.adjustment,
                        )
                    
                    console.print(sug_table)
    else:
        # Fallback output
        print(f"Foreground: {fg.to_hex()}")
        print(f"Background: {bg.to_hex()}")
        print(f"Contrast Ratio: {result.ratio:.2f}:1")
        print(f"WCAG AA: {'PASS' if result.aa_normal else 'FAIL'}")
        print(f"WCAG AAA: {'PASS' if result.aaa_normal else 'FAIL'}")
    
    return 0 if result.is_accessible(WCAGLevel.AA) else 1


def cmd_simulate(args):
    """Handle simulate command"""
    simulator = ColorBlindnessSimulator()
    
    try:
        color = Color.from_hex(args.color)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
    
    if RICH_AVAILABLE:
        table = Table(title=f"👁️ Color Blindness Simulation for {color.to_hex()}", show_header=True)
        table.add_column("Type", style="cyan")
        table.add_column("Original", style="white")
        table.add_column("Simulated", style="white")
        table.add_column("Description", style="dim")
        
        if args.type == "all":
            types_to_simulate = list(ColorBlindnessType)
        else:
            types_to_simulate = [ColorBlindnessType(args.type)]
        
        for blindness_type in types_to_simulate:
            result = simulator.simulate(color, blindness_type)
            table.add_row(
                blindness_type.value.title(),
                f"[{result.original.to_hex()}]  {result.original.to_hex()}  [/]",
                f"[{result.simulated.to_hex()}]  {result.simulated.to_hex()}  [/]",
                result.description[:40] + "..." if len(result.description) > 40 else result.description,
            )
        
        console.print(table)
    else:
        print(f"Color Blindness Simulation for {color.to_hex()}")
        if args.type == "all":
            types_to_simulate = list(ColorBlindnessType)
        else:
            types_to_simulate = [ColorBlindnessType(args.type)]
        
        for blindness_type in types_to_simulate:
            result = simulator.simulate(color, blindness_type)
            print(f"{blindness_type.value}: {result.original.to_hex()} → {result.simulated.to_hex()}")
    
    return 0


def cmd_suggest(args):
    """Handle suggest command"""
    suggester = ColorSuggester()
    checker = ContrastChecker()
    
    try:
        fg = Color.from_hex(args.foreground)
        bg = Color.from_hex(args.background)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
    
    target_level = WCAGLevel.AAA if args.level == "aaa" else WCAGLevel.AA
    
    if RICH_AVAILABLE:
        console.print(Panel(
            f"Analyzing color pair: [bold]{fg.to_hex()}[/] on [bold]{bg.to_hex()}[/]",
            title="💡 Color Suggestion",
            border_style="cyan",
        ))
        
        current = checker.check(fg, bg)
        console.print(f"Current ratio: [bold]{current.ratio:.2f}:1[/] ({current.wcag_level.value})")
        
        if args.adjust == "foreground":
            suggestions = suggester.suggest_foreground(fg, bg, target_level)
            title = "Foreground Suggestions"
        elif args.adjust == "background":
            suggestions = suggester.suggest_background(fg, bg, target_level)
            title = "Background Suggestions"
        else:
            suggestions = suggester.suggest_both(fg, bg, target_level)
            title = "Combined Suggestions"
        
        if suggestions:
            table = Table(title=title, show_header=True)
            table.add_column("Original", style="red")
            table.add_column("Suggested", style="green")
            table.add_column("New Ratio", style="yellow")
            table.add_column("WCAG Level", style="cyan")
            
            for sug in suggestions[:5]:
                if hasattr(sug, '__iter__') and not isinstance(sug, str):
                    # Combined suggestion
                    fg_sug, bg_sug = sug
                    table.add_row(
                        f"FG: {fg_sug.original.to_hex()}",
                        f"FG: {fg_sug.suggested.to_hex()}",
                        f"{fg_sug.new_ratio:.2f}:1",
                        fg_sug.wcag_level.value,
                    )
                else:
                    table.add_row(
                        sug.original.to_hex(),
                        sug.suggested.to_hex(),
                        f"{sug.new_ratio:.2f}:1",
                        sug.wcag_level.value,
                    )
            
            console.print(table)
    else:
        current = checker.check(fg, bg)
        print(f"Current ratio: {current.ratio:.2f}:1")
        
        if args.adjust == "foreground":
            suggestions = suggester.suggest_foreground(fg, bg, target_level)
        else:
            suggestions = suggester.suggest_background(fg, bg, target_level)
        
        for sug in suggestions[:3]:
            print(f"Suggestion: {sug.original.to_hex()} → {sug.suggested.to_hex()}")
            print(f"  New ratio: {sug.new_ratio:.2f}:1")
    
    return 0


def cmd_batch(args):
    """Handle batch command"""
    input_path = Path(args.input)
    
    if not input_path.exists():
        console.print(f"[red]Error:[/red] File not found: {args.input}")
        return 1
    
    # Read input file
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            if input_path.suffix in [".json"]:
                data = json.load(f)
            else:
                console.print("[red]Error:[/red] Only JSON files are supported in this version")
                return 1
    except Exception as e:
        console.print(f"[red]Error reading file:[/red] {e}")
        return 1
    
    # Parse color pairs
    color_pairs = []
    if isinstance(data, list):
        for item in data:
            if "foreground" in item and "background" in item:
                color_pairs.append((item["foreground"], item["background"]))
    elif isinstance(data, dict) and "colors" in data:
        for item in data["colors"]:
            if "foreground" in item and "background" in item:
                color_pairs.append((item["foreground"], item["background"]))
    
    if not color_pairs:
        console.print("[red]Error:[/red] No valid color pairs found in input file")
        return 1
    
    # Check all pairs
    checker = ContrastChecker()
    results = []
    
    if RICH_AVAILABLE:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Checking colors...", total=len(color_pairs))
            
            for fg_hex, bg_hex in color_pairs:
                try:
                    fg = Color.from_hex(fg_hex)
                    bg = Color.from_hex(bg_hex)
                    result = checker.check(fg, bg)
                    results.append(result)
                except ValueError:
                    pass
                progress.advance(task)
    else:
        for fg_hex, bg_hex in color_pairs:
            try:
                fg = Color.from_hex(fg_hex)
                bg = Color.from_hex(bg_hex)
                result = checker.check(fg, bg)
                results.append(result)
            except ValueError:
                pass
    
    # Generate report
    generator = ReportGenerator()
    
    if args.format == "json":
        content = generator.generate_json(results)
    elif args.format == "markdown":
        content = generator.generate_markdown(results)
    elif args.format == "html":
        content = generator.generate_html(results)
    else:
        content = generator.generate_text(results)
    
    # Output
    if args.output:
        output_path = generator.save_report(content, args.output, args.format)
        console.print(f"[green]✓[/] Report saved to: {output_path}")
    else:
        print(content)
    
    return 0


def cmd_interactive(args):
    """Handle interactive mode"""
    if not RICH_AVAILABLE:
        console.print("[red]Error:[/red] Interactive mode requires the 'rich' library")
        console.print("Install with: pip install rich")
        return 1
    
    console.print(Panel(
        "[bold cyan]ColorScope Interactive Mode[/]\n\n"
        "Analyze colors for accessibility compliance\n"
        "Type 'help' for commands, 'quit' to exit",
        title="🎨 ColorScope-CLI",
        border_style="cyan",
    ))
    
    checker = ContrastChecker()
    simulator = ColorBlindnessSimulator()
    suggester = ColorSuggester()
    
    while True:
        try:
            command = Prompt.ask("\n[bold cyan]colorscope[/]", default="help")
            
            if command.lower() in ["quit", "exit", "q"]:
                console.print("[yellow]Goodbye![/]")
                break
            
            elif command.lower() == "help":
                console.print("""
[bold]Available Commands:[/]
  check <fg> <bg>  - Check contrast between two colors
  simulate <color>  - Simulate color blindness
  suggest <fg> <bg> - Get improvement suggestions
  help              - Show this help message
  quit              - Exit interactive mode
                """)
            
            elif command.lower().startswith("check"):
                parts = command.split()
                if len(parts) >= 3:
                    fg_hex = parts[1]
                    bg_hex = parts[2]
                    
                    try:
                        fg = Color.from_hex(fg_hex)
                        bg = Color.from_hex(bg_hex)
                        result = checker.check(fg, bg)
                        
                        console.print(f"\n[bold]Result:[/]")
                        console.print(f"  Foreground: {fg.to_hex()}")
                        console.print(f"  Background: {bg.to_hex()}")
                        console.print(f"  Ratio: [bold]{result.ratio:.2f}:1[/]")
                        console.print(f"  AA: {'[green]PASS[/]' if result.aa_normal else '[red]FAIL[/]'}")
                        console.print(f"  AAA: {'[green]PASS[/]' if result.aaa_normal else '[red]FAIL[/]'}")
                    except ValueError as e:
                        console.print(f"[red]Error:[/red] {e}")
                else:
                    console.print("[red]Usage:[/] check <foreground> <background>")
            
            elif command.lower().startswith("simulate"):
                parts = command.split()
                if len(parts) >= 2:
                    color_hex = parts[1]
                    
                    try:
                        color = Color.from_hex(color_hex)
                        results = simulator.simulate_all(color)
                        
                        console.print(f"\n[bold]Color Blindness Simulation for {color.to_hex()}:[/]")
                        for blindness_type, result in results.items():
                            console.print(
                                f"  {blindness_type.title()}: "
                                f"{result.original.to_hex()} → {result.simulated.to_hex()}"
                            )
                    except ValueError as e:
                        console.print(f"[red]Error:[/red] {e}")
                else:
                    console.print("[red]Usage:[/] simulate <color>")
            
            elif command.lower().startswith("suggest"):
                parts = command.split()
                if len(parts) >= 3:
                    fg_hex = parts[1]
                    bg_hex = parts[2]
                    
                    try:
                        fg = Color.from_hex(fg_hex)
                        bg = Color.from_hex(bg_hex)
                        suggestions = suggester.suggest_foreground(fg, bg, WCAGLevel.AA)
                        
                        console.print(f"\n[bold]Suggestions:[/]")
                        for sug in suggestions[:3]:
                            console.print(
                                f"  {sug.original.to_hex()} → {sug.suggested.to_hex()} "
                                f"(Ratio: {sug.new_ratio:.2f}:1)"
                            )
                    except ValueError as e:
                        console.print(f"[red]Error:[/red] {e}")
                else:
                    console.print("[red]Usage:[/] suggest <foreground> <background>")
            
            else:
                console.print(f"[red]Unknown command:[/] {command}")
                console.print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/]")
            break
        except EOFError:
            break
    
    return 0


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    # Dispatch to command handlers
    commands = {
        "check": cmd_check,
        "simulate": cmd_simulate,
        "suggest": cmd_suggest,
        "batch": cmd_batch,
        "interactive": cmd_interactive,
    }
    
    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
