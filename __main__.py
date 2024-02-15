import click
from phone_book import PhoneBook

@click.group()
def main():
    pass

@main.command()
@click.option('--data-file', default='data.txt', help='Path to the data file.')
def run(data_file):
    pb = PhoneBook(data_file)
    pb.run()

if __name__ == "__main__":
    main()