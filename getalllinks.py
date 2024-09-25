import requests
from bs4 import BeautifulSoup

def get_filtered_links(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags and filter the href attributes
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/typer'):
                # Replace /typer with the full URL
                full_link = f'https://typersi.com{href}'
                links.append(full_link)

        return links

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

# Example usage
if __name__ == "__main__":
    url = 'https://typersi.com/ranking.html'  # Target URL
    filtered_links = get_filtered_links(url)
    for link in filtered_links:
        print(link)
