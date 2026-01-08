"""CLI Tool for Training Data Curation"""
import click
from pathlib import Path

from src.infrastructure.training.data_curator import DataCurator


@click.group()
def cli():
    """Cerberus AI Training Data Curator"""
    pass


@cli.command()
@click.option("--date", help="Filter by date (YYYY-MM-DD)")
def stats(date):
    """Show dataset statistics"""
    curator = DataCurator()
    examples = curator.load_examples(date)
    examples = curator.apply_feedback(examples)
    
    stats = curator.get_statistics(examples)
    
    click.echo(f"\n📊 Dataset Statistics\n")
    click.echo(f"Total Examples: {stats['total_examples']}")
    click.echo(f"High Quality: {stats['high_quality_examples']} ({stats['quality_rate']:.1%})")
    click.echo(f"Avg Complexity: {stats['avg_complexity']:.1f}/10")
    
    if stats['languages']:
        click.echo(f"\n🔤 Languages:")
        for lang, count in sorted(stats['languages'].items(), key=lambda x: -x[1]):
            click.echo(f"  {lang}: {count}")
    
    if stats['frameworks']:
        click.echo(f"\n🛠️  Frameworks:")
        for fw, count in sorted(stats['frameworks'].items(), key=lambda x: -x[1]):
            click.echo(f"  {fw}: {count}")


@cli.command()
@click.option("--date", help="Filter by date (YYYY-MM-DD)")
@click.option("--output", default="training_data.jsonl", help="Output filename")
def export(date, output):
    """Export curated training data"""
    curator = DataCurator()
    examples = curator.load_examples(date)
    examples = curator.apply_feedback(examples)
    examples = curator.filter_high_quality(examples)
    
    output_file = curator.export_for_training(examples, output)
    
    click.echo(f"✅ Exported {len(examples)} examples to {output_file}")


@cli.command()
def progress():
    """Show progress towards 50k examples goal"""
    curator = DataCurator()
    examples = curator.load_examples()
    examples = curator.apply_feedback(examples)
    high_quality = curator.filter_high_quality(examples)
    
    total = len(examples)
    quality_count = len(high_quality)
    goal = 50000
    
    click.echo(f"\n🎯 Progress to 50k Examples Goal\n")
    click.echo(f"Total Collected: {total:,}")
    click.echo(f"High Quality: {quality_count:,}")
    click.echo(f"Goal: {goal:,}")
    click.echo(f"Progress: {quality_count/goal:.1%}")
    click.echo(f"Remaining: {goal - quality_count:,}")


if __name__ == "__main__":
    cli()
